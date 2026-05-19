import { useState } from "react";
import axios from "axios";

function Login() {

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const loginUser = async () => {

    try {

      const response = await axios.post(

        "http://127.0.0.1:5000/api/login",

        {
          username,
          password
        }
      );

      localStorage.setItem(
        "token",
        response.data.token
      );
      localStorage.setItem(
        "role",
        response.data.role
      )

      window.location.href =
        "/dashboard";

    } catch (error) {

      alert("Invalid Login");
    }
  };

  return (

    <div style={{ padding: "50px" }}>

      <h1>🔐 Login</h1>

      <input
        type="text"
        placeholder="Username"
        onChange={(e) =>
          setUsername(e.target.value)
        }
      />

      <br /><br />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <br /><br />

      <button onClick={loginUser}>
        Login
      </button>

    </div>
  );
}

export default Login;