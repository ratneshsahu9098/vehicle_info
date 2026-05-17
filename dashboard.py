from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from datetime import datetime

import sqlite3

app = Flask(__name__)

CORS(app)

app.secret_key = "supersecretkey"
app.config["JWT_SECRET_KEY"] = "jwt-secret-key"

jwt = JWTManager(app)

DB_FILE = "vehicles.db"

# -------------------------
# CREATE DATABASE TABLES
# -------------------------

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()

# VEHICLES TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS
vehicles (

    id INTEGER
    PRIMARY KEY AUTOINCREMENT,

    vehicle_number TEXT,

    expiry_date TEXT,

    phone TEXT,

    owner TEXT
)

""")

# HISTORY TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS
vehicle_history (

    id INTEGER
    PRIMARY KEY AUTOINCREMENT,

    vehicle_id INTEGER,

    vehicle_number TEXT,

    expiry_date TEXT,

    phone TEXT,

    owner TEXT,

    edited_at TEXT
)

""")

conn.commit()

conn.close()

# -------------------------
# VEHICLE HISTORY API
# -------------------------

@app.route(

    "/api/vehicle_history/<int:id>",

    methods=["GET"]
)

@jwt_required()

def vehicle_history_api(id):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT
        vehicle_number,
        expiry_date,
        phone,
        owner,
        edited_at

    FROM vehicle_history

    WHERE vehicle_id=?

    ORDER BY id DESC

    """, (id,))

    history = cursor.fetchall()

    conn.close()

    result = []

    for row in history:

        result.append({

            "vehicle_number": row[0],

            "expiry_date": row[1],

            "phone": row[2],

            "owner": row[3],

            "edited_at": row[4]
        })

    return jsonify(result)

# -------------------------
# ADD VEHICLE API
# -------------------------

@app.route(
    "/api/add_vehicle",
    methods=["POST"]
)

@jwt_required()

def add_vehicle_api():

    data = request.get_json()

    vehicle_number = data["vehicle_number"]

    expiry_date = data["expiry_date"]

    phone = data["phone"]

    owner = data["owner"]

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""

CREATE TABLE IF NOT EXISTS
vehicle_history (

    id INTEGER
    PRIMARY KEY AUTOINCREMENT,

    vehicle_id INTEGER,

    vehicle_number TEXT,

    expiry_date TEXT,

    phone TEXT,

    owner TEXT,

    edited_at TEXT
)

""")

    cursor.execute("""

    INSERT INTO vehicles (

        vehicle_number,
        expiry_date,
        phone,
        owner

    )

    VALUES (?, ?, ?, ?)

    """, (

        vehicle_number,
        expiry_date,
        phone,
        owner
    ))

    conn.commit()

    conn.close()

    return jsonify({

        "message":
        "Vehicle added"
    })

# -------------------------
# LOGIN
# -------------------------


@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Simple admin login
        if username == "admin" and password == "app@9098":

            session["user"] = username

            return redirect("/")

        else:
            error = "Invalid credentials"

    return render_template("login.html", error=error)




# -------------------------
# LOGOUT
# -------------------------


@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")



# -------------------------
# DELETE VEHICLE API
# -------------------------

@app.route(
    "/api/delete_vehicle/<int:id>",
    methods=["DELETE"]
)

@jwt_required()

def delete_vehicle_api(id):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM vehicles

    WHERE id=?

    """, (id,))

    conn.commit()

    conn.close()

    return jsonify({

        "message":
        "Vehicle deleted"
    })

# -------------------------
# UPDATE VEHICLE API
# -------------------------

@app.route(
    "/api/update_vehicle/<int:id>",
    methods=["PUT"]
)

@jwt_required()

def update_vehicle_api(id):

    data = request.get_json()

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    #GET OLD DATA

    # GET OLD DATA

    cursor.execute(
        "SELECT * FROM vehicles WHERE id=?",
        (id,)
    )

    old_vehicle = cursor.fetchone()

    # SAVE INTO HISTORY

    from datetime import datetime

    cursor.execute("""
        INSERT INTO vehicle_history (
            vehicle_id,
            vehicle_number,
            expiry_date,
            phone,
            owner,
            edited_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        old_vehicle[0],
        old_vehicle[1],
        old_vehicle[2],
        old_vehicle[3],
        old_vehicle[4],
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))


    cursor.execute("""

    UPDATE vehicles

    SET
      vehicle_number=?,
      expiry_date=?,
      phone=?,
      owner=?

    WHERE id=?

    """, (

        data["vehicle_number"],
        data["expiry_date"],
        data["phone"],
        data["owner"],
        id
    ))

    conn.commit()

    conn.close()

    return jsonify({

        "message":
        "Vehicle updated"
    })


# -------------------------
# HOME PAGE
# -------------------------


@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    if search:

        cursor.execute(
            """

        SELECT *
        FROM vehicles

        WHERE
            vehicle_number LIKE ?
            OR owner LIKE ?

        """,
            (f"%{search}%", f"%{search}%"),
        )

    else:

        cursor.execute(
            """
        SELECT *
        FROM vehicles
        """
        )

    vehicles = cursor.fetchall()

    # -------------------------
    # ANALYTICS
    # -------------------------

    from datetime import datetime

    today = datetime.today()

    total_vehicles = len(vehicles)

    expired_count = 0
    expiring_count = 0
    active_count = 0
    for vehicle in vehicles:

        expiry = datetime.strptime(vehicle[2], "%Y-%m-%d")

        days_left = (expiry - today).days

        if days_left < 0:

            expired_count += 1

        elif days_left <= 7:

            expiring_count += 1

        else:

            active_count += 1

    from datetime import timedelta

    current_date = today.strftime("%Y-%m-%d")

    warning_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")

    conn.close()

    return render_template(
        "index.html",
        vehicles=vehicles,
        search=search,
        total_vehicles=total_vehicles,
        expired_count=expired_count,
        expiring_count=expiring_count,
        active_count=active_count,
        current_date=current_date,
        warning_date=warning_date,
    )


# -------------------------
# EDIT PAGE
# -------------------------


@app.route("/edit/<int:id>")
def edit_page(id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT *
    FROM vehicles
    WHERE id=?
    """,
        (id,),
    )

    vehicle = cursor.fetchone()

    conn.close()

    return render_template("edit.html", vehicle=vehicle)


# -------------------------
# UPDATE
# -------------------------


@app.route("/update/<int:id>", methods=["POST"])
def update_vehicle(id):

    if "user" not in session:
        return redirect("/login")

    vehicle_number = request.form["vehicle_number"]
    expiry_date = request.form["expiry_date"]
    phone = request.form["phone"]
    owner = request.form["owner"]

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """

    UPDATE vehicles

    SET
        vehicle_number=?,
        expiry_date=?,
        phone=?,
        owner=?

    WHERE id=?

    """,
        (vehicle_number, expiry_date, phone, owner, id),
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------------
# PDF REPORT
# -------------------------


@app.route("/report")
def generate_report():

    if "user" not in session:
        return redirect("/login")

    from reportlab.platypus import (
        SimpleDocTemplate,
        Table,
        TableStyle,
        Paragraph,
        Spacer,
    )

    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet

    from flask import send_file

    import sqlite3

    pdf_file = "vehicle_report.pdf"

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT *
    FROM vehicles
    """
    )

    vehicles = cursor.fetchall()

    conn.close()

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph("MV Tax Vehicle Report", styles["Title"])

    elements.append(title)

    elements.append(Spacer(1, 20))

    data = [["ID", "Vehicle", "Expiry", "Phone", "Owner"]]

    for vehicle in vehicles:

        data.append([vehicle[0], vehicle[1], vehicle[2], vehicle[3], vehicle[4]])

    table = Table(data)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ]
        )
    )

    elements.append(table)

    doc.build(elements)

    return send_file(pdf_file, as_attachment=True)


# -------------------------
# API - GET VEHICLES
# -------------------------


@app.route("/api/vehicles", methods=["GET"])
@jwt_required()
def api_get_vehicles():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT *
    FROM vehicles
    """
    )

    vehicles = cursor.fetchall()

    conn.close()

    vehicle_list = []

    for vehicle in vehicles:

        vehicle_list.append(
            {
                "id": vehicle[0],
                "vehicle_number": vehicle[1],
                "expiry_date": vehicle[2],
                "phone": vehicle[3],
                "owner": vehicle[4],
            }
        )

    return jsonify(vehicle_list)


# -------------------------
# API - ADD VEHICLE
# -------------------------


@app.route("/api/vehicles", methods=["POST"])

# -------------------------
# API - ADD VEHICLE
# -------------------------


@app.route("/api/vehicles", methods=["POST"])
def api_add_vehicle():

    if not request.is_json:

        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()

    vehicle_number = data.get("vehicle_number")
    expiry_date = data.get("expiry_date")
    phone = data.get("phone")
    owner = data.get("owner")

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """

    INSERT INTO vehicles (
        vehicle_number,
        expiry_date,
        phone,
        owner
    )

    VALUES (?, ?, ?, ?)

    """,
        (vehicle_number, expiry_date, phone, owner),
    )

    conn.commit()

    conn.close()

    return jsonify({"message": "Vehicle added successfully"})


# API - DELETE VEHICLE
# -------------------------


@app.route("/api/vehicles/<int:id>", methods=["DELETE"])
def api_delete_vehicle(id):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """

    DELETE FROM vehicles

    WHERE id=?

    """,
        (id,),
    )

    conn.commit()

    conn.close()

    return jsonify({"message": "Vehicle deleted successfully"})


@jwt_required()
def api_get_vehicles():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT *
    FROM vehicles
    """
    )

    vehicles = cursor.fetchall()

    conn.close()

    vehicle_list = []

    for vehicle in vehicles:

        vehicle_list.append(
            {
                "id": vehicle[0],
                "vehicle_number": vehicle[1],
                "expiry_date": vehicle[2],
                "phone": vehicle[3],
                "owner": vehicle[4],
            }
        )

    return jsonify(vehicle_list)


# -------------------------
# API LOGIN
# -------------------------


@app.route("/api/login", methods=["POST"])
def api_login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin123":

        token = create_access_token(identity=username)

        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401


# -------------------------
# RUN APP
# -------------------------

if __name__ == "__main__":

    app.run(debug=True)
