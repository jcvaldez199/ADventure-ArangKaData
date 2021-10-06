import React, { Component } from 'react';
import { Redirect } from 'react-router-dom'
import Navbar from "./Navbar/Navbar";
import Login from './Auth/Login'
import Register from './Auth/Register'
import PrivateRoute, { AdminRoute } from './Utils/PrivateRoute'
import Approval from './Admin/Approval'
import { Home } from './Home/Home'
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom'

function MainApp() {
  return (
    <Router>
      <div>
        <Switch>
          <Route exact path='/'>
            {localStorage.getItem('logged_in') ? <Redirect to="/main" /> : <Redirect to="/login" /> }
          </Route>
          <Route path='/login' component={Login} />
          <Route path='/register' component={Register} />
          <PrivateRoute path='/main' component={Navbar} />
          <AdminRoute path='/admin' component={Approval} />
        </Switch>
      </div>
    </Router> 

  );
}

export default MainApp;
