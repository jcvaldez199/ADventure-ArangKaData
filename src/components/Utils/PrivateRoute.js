import React, { useState, useEffect } from 'react'
import { Redirect, Route } from 'react-router-dom'
import axios from 'axios'

const PrivateRoute = ({ component: Component, ...rest }) => {

  // Check the Token

  return (
    <Route
      {...rest}
      render={props =>
        localStorage.getItem('logged_in') ? (
          <Component {...props} />
        ) : (
          <Redirect to={{ pathname: '/login', state: { from: props.location } }} />
        )
      }
    />
  )
}

export const AdminRoute = ({ component: Component, ...rest }) => {

  // Check the Token
  const adminUrl = "http://localhost:3000/auth/checkadmin"
  const [isadmin, setAdmin] = useState(false);

  useEffect(() => {
    axios
      .get(adminUrl,
          { headers: 
            { Authorization: `Bearer ${localStorage.getItem('token')}` }
          })
      .then((response) => {
        setAdmin(response.data.isAdmin);
        console.log(isadmin)
      }).catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <Route
      {...rest}
      render={props => 
          isadmin
          ? (
          <Component {...props} />
          )
          : (
            <h1>Waiting for Admin confirmation</h1>
          )
      }
    />
  )
}

export default PrivateRoute
