import React, { useState, useEffect } from 'react'
import { Redirect, Route } from 'react-router-dom'
import axios from 'axios'
import { UrlBase } from '../config'

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

export default PrivateRoute
