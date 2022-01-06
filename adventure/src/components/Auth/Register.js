import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Fade } from 'react-bootstrap'
import { CustomerRegisterUrl } from '../config'
import { useHistory } from 'react-router-dom'

// Move these to a config file

function Register() {
  const history = useHistory();

  function postCred(event) {
    axios.post(CustomerRegisterUrl, 
    {
      username: event.target.elements.formUsername.value,
      password: event.target.elements.formPassword.value
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
      <div className="auth-wrapper">
        <div className="auth-inner">
           <form onSubmit={postCred}>
              <h3>Register</h3>

              <div className="form-group" >
                  <label>Username</label>
                  <input type="username" name="formUsername" className="form-control" placeholder="Enter username" />
              </div>

              <div className="form-group">
                  <label>Password</label>
                  <input type="password"  name="formPassword" className="form-control" placeholder="Enter password" />
              </div>
              <button type="submit" className="btn btn-primary btn-block">Register</button>
          </form>
        </div>
      </div>
      </Fade>
    </div>
  );
};

export default Register;
