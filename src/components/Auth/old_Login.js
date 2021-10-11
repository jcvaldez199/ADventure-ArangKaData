import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Fade } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'
import { UrlBase } from '../config'

// Move these to a config file
const loginUrl = UrlBase.concat("/auth/login")

function Login() {
  const [username, setUsername] = useState(null);
  const [password, setPassword] = useState(null);
  const history = useHistory();
  const redirectpath = '/main';

  function postCred() {
    axios.post(loginUrl, 
    {
      username: username,
      password: password
    })
    .then((response) => {
      console.log(response.data.access_token);
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('logged_in', true);
      history.push(redirectpath);
    })
    .catch(error => {
      console.error("error",error);
    });
  }

  return (
    <div>
      <Fade appear={true} in={true}>
        <div>
          <h1>Sign In</h1>
          <input type="text" placeholder="username" value={username} onChange={(event) => setUsername(event.target.value)} />
          <input type="password" placeholder="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          <Button onClick={postCred}> Login </Button>
        </div>
      </Fade>
    </div>
  );

};

export default Login;
