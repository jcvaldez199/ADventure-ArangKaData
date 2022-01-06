import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Fade } from 'react-bootstrap'
import { UrlBase } from '../config'
import { useHistory } from 'react-router-dom'

// Move these to a config file
const loginUrl = UrlBase.concat("/auth/register")

function Register() {
  const [username, setUsername] = useState(null);
  const [password, setPassword] = useState(null);
  const history = useHistory();


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
    history.push('/login');
  }

  return (
    <div>
      <Fade appear={true} in={true}>
        <div>
          <h1>Register</h1>
          <input type="text" placeholder="username" value={username} onChange={(event) => setUsername(event.target.value)} />
          <input type="password" placeholder="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          <Button onClick={postCred}> Register </Button>
        </div>
      </Fade>
    </div>
  );
};

export default Register;
