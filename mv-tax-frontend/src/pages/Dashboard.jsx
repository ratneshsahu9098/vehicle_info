import {
    useEffect,
    useState
} from "react";


import axios from "axios";

import { CSVLink }
    from "react-csv";

function Dashboard() {

    
    const [historyData,
setHistoryData] =
useState([]);

const [showHistory,
setShowHistory] =
useState(false);

    const [vehicles, setVehicles] =
        useState([]);

    const [editingId,
        setEditingId] =
        useState(null);

    const [search,
        setSearch] =
        useState("");

    const [vehicleNumber,
        setVehicleNumber] =
        useState("");

    const [expiryDate,
        setExpiryDate] =
        useState("");

    const [phone,
        setPhone] =
        useState("");

    const [owner,
        setOwner] =
        useState("");
    useEffect(() => {

        fetchVehicles();

    }, []);

    const fetchVehicles = async () => {

        try {

            const token =
                localStorage.getItem("token");

            const response = await axios.get(

                "http://127.0.0.1:5000/api/vehicles",

                {
                    headers: {

                        Authorization:
                            `Bearer ${token}`
                    }
                }
            );

            setVehicles(response.data);

        } catch (error) {

            console.log(error);
        }
    };

    const today = new Date();

    const expired = vehicles.filter(
        (v) => {

            if (!v.expiry_date)
                return false;

            const expiry =
                new Date(v.expiry_date);

            return expiry < today;
        }
    );

    const expiring = vehicles.filter(
        (v) => {

            if (!v.expiry_date)
                return false;

            const expiry =
                new Date(v.expiry_date);

            const diff =
                (expiry - today) /
                (1000 * 60 * 60 * 24);

            return diff >= 0 &&
                diff <= 7;
        }
    );

    const active = vehicles.filter(
        (v) => {

            if (!v.expiry_date)
                return false;

            const expiry =
                new Date(v.expiry_date);

            const diff =
                (expiry - today) /
                (1000 * 60 * 60 * 24);

            return diff > 7;
        }
    );
    const addVehicle = async () => {

        try {

            const token =
                localStorage.getItem("token");

            await axios.post(

                "http://127.0.0.1:5000/api/add_vehicle",

                {

                    vehicle_number:
                        vehicleNumber,

                    expiry_date:
                        expiryDate,

                    phone,

                    owner
                },

                {
                    headers: {

                        Authorization:
                            `Bearer ${token}`
                    }
                }
            );

            fetchVehicles();

            setVehicleNumber("");
            setExpiryDate("");
            setPhone("");
            setOwner("");

        } catch (error) {

            console.log(error);
        }
    };

    const deleteVehicle = async (id) => {

        try {

            const token =
                localStorage.getItem("token");

            await axios.delete(

                `http://127.0.0.1:5000/api/delete_vehicle/${id}`,

                {
                    headers: {

                        Authorization:
                            `Bearer ${token}`
                    }
                }
            );

            fetchVehicles();

        } catch (error) {

            console.log(error);
        }
    };

    const startEdit = (vehicle) => {

        setEditingId(vehicle.id);

        setVehicleNumber(
            vehicle.vehicle_number
        );

        setExpiryDate(
            vehicle.expiry_date
        );

        setPhone(vehicle.phone);

        setOwner(vehicle.owner);
    };
    const updateVehicle = async () => {

        try {

            const token =
                localStorage.getItem("token");

            await axios.put(

                `http://127.0.0.1:5000/api/update_vehicle/${editingId}`,

                {

                    vehicle_number:
                        vehicleNumber,

                    expiry_date:
                        expiryDate,

                    phone,

                    owner
                },

                {
                    headers: {

                        Authorization:
                            `Bearer ${token}`
                    }
                }
            );

            setEditingId(null);

            setVehicleNumber("");
            setExpiryDate("");
            setPhone("");
            setOwner("");

            fetchVehicles();

        } catch (error) {

            console.log(error);
        }
    };

    const filteredVehicles =
        vehicles.filter((vehicle) => {

            return (

                vehicle.vehicle_number
                    .toLowerCase()
                    .includes(
                        search.toLowerCase()
                    )

                ||

                vehicle.owner
                    .toLowerCase()
                    .includes(
                        search.toLowerCase()
                    )
            );
        });

    const sendWhatsApp = (vehicle) => {

        const message = `

🚗 MV Tax Reminder

Hello ${vehicle.owner},

Vehicle:
${vehicle.vehicle_number}

Tax expiry:
${vehicle.expiry_date}

Please renew soon.

`;

        const url =

            `https://wa.me/91${vehicle.phone}?text=${encodeURIComponent(message)}`;

        window.open(url, "_blank");
    };

    const viewHistory = async (id) => {

  try {

    const token =
      localStorage.getItem("token");

    const response =
      await axios.get(

        `http://127.0.0.1:5000/api/vehicle_history/${id}`,

        {
          headers: {

            Authorization:
              `Bearer ${token}`
          }
        }
      );

    console.log(
      response.data
    );

    setHistoryData(
      response.data
    );

    setShowHistory(true);

  } catch (error) {

    console.log(error);
  }
};

    return (

        <div>

            {/* NAVBAR */}

            <div className="navbar">

                <h2>
                    🚗 MV Tax Dashboard
                </h2>

                <button

                    className="logout-btn"

                    onClick={() => {

                        localStorage.removeItem(
                            "token"
                        );

                        window.location.href =
                            "/";
                    }}
                >

                    Logout

                </button>
                <CSVLink

                    data={vehicles}

                    filename={"vehicles.csv"}

                    style={{

                        background: "blue",

                        color: "white",

                        padding: "10px",

                        marginLeft: "10px",

                        textDecoration: "none",

                        borderRadius: "5px"
                    }}
                >

                    Export CSV

                </CSVLink>

            </div>
            <div
                className="table-container"
                style={{ marginBottom: "20px" }}
            >

                <h2>Add Vehicle</h2>

                <input
                    type="text"
                    placeholder="Vehicle Number"
                    value={vehicleNumber}
                    onChange={(e) =>
                        setVehicleNumber(e.target.value)
                    }
                />

                <input
                    type="date"
                    value={expiryDate}
                    onChange={(e) =>
                        setExpiryDate(e.target.value)
                    }
                />

                <input
                    type="text"
                    placeholder="Phone"
                    value={phone}
                    onChange={(e) =>
                        setPhone(e.target.value)
                    }
                />

                <input
                    type="text"
                    placeholder="Owner"
                    value={owner}
                    onChange={(e) =>
                        setOwner(e.target.value)
                    }
                />

                {

                    editingId ? (

                        <button
                            onClick={updateVehicle}
                        >

                            Update Vehicle

                        </button>

                    ) : (

                        <button
                            onClick={addVehicle}
                        >

                            Add Vehicle

                        </button>
                    )
                }

            </div>

            <div className="container">
                <input

                    type="text"

                    placeholder=
                    "Search vehicle or owner"

                    value={search}

                    onChange={(e) =>
                        setSearch(e.target.value)
                    }

                />

                {/* ANALYTICS */}

                <div className="cards">

                    <div className="card blue">

                        {vehicles.length}

                        <br />

                        Total Vehicles

                    </div>

                    <div className="card red">

                        {expired.length}

                        <br />

                        Expired

                    </div>

                    <div className="card orange">

                        {expiring.length}

                        <br />

                        Expiring

                    </div>

                    <div className="card green">

                        {active.length}

                        <br />

                        Active

                    </div>

                </div>

                {/* TABLE */}

                <div className="table-container">

                    <h2>
                        Vehicle Records
                    </h2>

                    <table>

                        <thead>



                            <tr>

                                <th>ID</th>
                                <th>Vehicle</th>
                                <th>Expiry</th>
                                <th>Phone</th>
                                <th>Owner</th>
                                <th>Status</th>
                                <th>Actions</th>

                            </tr>

                        </thead>

                        <tbody>

                            {filteredVehicles.map((vehicle) => (

                                <tr key={vehicle.id}>

                                    <td>{vehicle.id}</td>

                                    <td>
                                        {vehicle.vehicle_number}
                                    </td>

                                    <td>
                                        {vehicle.expiry_date}
                                    </td>

                                    <td>{vehicle.phone}</td>

                                    <td>{vehicle.owner}</td>
                                    <td>

                                        {

                                            (() => {

                                                const today =
                                                    new Date();

                                                const expiry =
                                                    new Date(
                                                        vehicle.expiry_date
                                                    );

                                                const diff =
                                                    (expiry - today) /
                                                    (1000 * 60 * 60 * 24);

                                                if (diff < 0) {

                                                    return (

                                                        <span
                                                            style={{
                                                                color: "red",
                                                                fontWeight: "bold"
                                                            }}
                                                        >

                                                            Expired

                                                        </span>
                                                    );
                                                }

                                                else if (diff <= 7) {

                                                    return (

                                                        <span
                                                            style={{
                                                                color: "orange",
                                                                fontWeight: "bold"
                                                            }}
                                                        >

                                                            Expiring

                                                        </span>
                                                    );
                                                }

                                                else {

                                                    return (

                                                        <span
                                                            style={{
                                                                color: "green",
                                                                fontWeight: "bold"
                                                            }}
                                                        >

                                                            Active

                                                        </span>
                                                    );
                                                }
                                            })()
                                        }

                                    </td>

                                    <td>


                                        <button

                                            onClick={() =>
                                                startEdit(vehicle)
                                            }

                                            style={{
                                                background: "orange",
                                                marginRight: "10px"
                                            }}
                                        >

                                            Edit

                                        </button>

                                        <button

                                            onClick={() =>
                                                sendWhatsApp(vehicle)
                                            }

                                            style={{
                                                background: "green",
                                                marginRight: "10px"
                                            }}
                                        >

                                            WhatsApp

                                        </button>
                                        <button

                                            onClick={() =>
                                                viewHistory(vehicle.id)
                                            }

                                            style={{
                                                background: "blue",
                                                marginRight: "10px"
                                            }}
                                        >

                                            History

                                        </button>
                                        <button

                                            onClick={() =>
                                                deleteVehicle(vehicle.id)
                                            }

                                            style={{
                                                background: "red"
                                            }}
                                        >

                                            Delete

                                        </button>

                                    </td>

                                </tr>
                            ))}

                        </tbody>

                    </table>

                </div>

            </div>
{

  showHistory && (

    <div
      style={{

        position: "fixed",

        top: 0,
        left: 0,

        width: "100%",
        height: "100%",

        background:
          "rgba(0,0,0,0.5)",

        display: "flex",

        justifyContent:
          "center",

        alignItems:
          "center"
      }}
    >

      <div
        style={{

          background: "white",

          padding: "20px",

          borderRadius: "10px",

          width: "700px"
        }}
      >

        <h2>
          Vehicle History
        </h2>

        <button

          onClick={() =>
            setShowHistory(false)
          }

          style={{
            background: "red",
            marginBottom: "20px"
          }}
        >

          Close

        </button>

        <table>

          <thead>

            <tr>

              <th>Vehicle</th>
              <th>Expiry</th>
              <th>Phone</th>
              <th>Owner</th>
              <th>Edited At</th>

            </tr>

          </thead>

          <tbody>

            {historyData.map(
              (item, index) => (

              <tr key={index}>

                <td>
                  {item.vehicle_number}
                </td>

                <td>
                  {item.expiry_date}
                </td>

                <td>
                  {item.phone}
                </td>

                <td>
                  {item.owner}
                </td>

                <td>
                  {item.edited_at}
                </td>

              </tr>
            ))}

          </tbody>

        </table>

      </div>

    </div>
  )
}
        </div>
        
    );

}


export default Dashboard;