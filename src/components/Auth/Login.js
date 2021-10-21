import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Fade } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'
import { CustomerLoginUrl } from '../config'
import './auth-css.css'

// Move these to a config file
function Login() {
  const history = useHistory();
  const redirectpath = '/main';

  function postCred(event) {
    event.preventDefault()
    axios.post(CustomerLoginUrl, 
    {
      username: event.target.elements.formUsername.value,
      password: event.target.elements.formPassword.value
    })
    .then((response) => {
      localStorage.clear();
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('logged_in', true);
      history.push(redirectpath);
      window.location.reload();
    })
    .catch(error => {
      console.error("error",error);
    });
  }

  return (
    <div>
      <Fade appear={true} in={true}>
      <div className="auth-wrapper">
        <div className="auth-inner">
           <form onSubmit={postCred}>
              <h3>Sign In</h3>

              <div className="form-group" >
                  <label>Username</label>
                  <input type="username" name="formUsername" className="form-control" placeholder="Enter username" />
              </div>

              <div className="form-group">
                  <label>Password</label>
                  <input type="password"  name="formPassword" className="form-control" placeholder="Enter password" />
              </div>
             {/*
              <div className="form-group">
                  <div className="custom-control custom-checkbox">
                      <input type="checkbox" className="custom-control-input" id="customCheck1" />
                      <label className="custom-control-label" htmlFor="customCheck1">Remember me</label>
                  </div>
              </div>

              <p className="forgot-password text-right">
                  Forgot <a href="#">password?</a>
              </p>*/}
              <button type="submit" className="btn btn-primary btn-block">Login</button>
          </form>
        </div>
      </div>
      </Fade>
    </div>
  );

};

export default Login;
