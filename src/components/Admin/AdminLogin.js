import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Fade } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'
import { AdminLoginUrl } from '../config'
import './auth-css.css'

// Move these to a config file
function AdminLogin() {
  const history = useHistory();
  const redirectpath = '/main';

  function postCred(event) {
    event.preventDefault()
    axios.post(AdminLoginUrl, 
    {
      username: event.target.elements.formUsername.value,
      password: event.target.elements.formPassword.value
    })
    .then((response) => {
      localStorage.clear();
      localStorage.setItem('admin_token', response.data.access_token);
      localStorage.setItem('admin_logged_in', true);
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
              <h3>Admin Sign In</h3>

              <div className="form-group" >
                  <label>Username</label>
                  <input type="username" name="formUsername" className="form-control" placeholder="Enter username" />
              </div>

              <div className="form-group">
                  <label>Password</label>
                  <input type="password"  name="formPassword" className="form-control" placeholder="Enter password" />
              </div>
              <button type="submit" className="btn btn-primary btn-block">Login</button>
          </form>
        </div>
      </div>
      </Fade>
    </div>
  );

};

export default AdminLogin;
