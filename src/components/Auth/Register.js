import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button } from 'react-bootstrap'

// Move these to a config file
const loginUrl = "http://localhost:3000/auth/register"

function Register() {
  const [username, setUsername] = useState(null);
  const [password, setPassword] = useState(null);

  function postCred() {
    axios.post(loginUrl, 
    {
      username: username,
      password: password
    })
    .then((response) => {
      console.log("registered");
    })
    .catch(error => {
      console.error("error",error);
    });
  }

  return (
    <div>
      <h1>Register</h1>
      <input type="text" placeholder="username" value={username} onChange={(event) => setUsername(event.target.value)} />
      <input type="password" placeholder="password" value={password} onChange={(event) => setPassword(event.target.value)} />
      <Button onClick={postCred}> Register </Button>
    </div>
  );
};

export default Register;
