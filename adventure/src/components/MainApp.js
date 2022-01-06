import React, { Component } from 'react';
import { Redirect } from 'react-router-dom'
import Login from './Auth/Login'
import Register from './Auth/Register'
import PrivateRoute from './Utils/PrivateRoute'
import Approval from './Admin/Approval'
import { Home } from './Home/Home'
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom'
import { LandingNav, LandingMain } from './LandingPage/LandingPage'

function MainApp() {
  return (
    <Router>
      <div>
        {!localStorage.getItem('logged_in') && <LandingNav /> }
        <Switch>
          <Route exact path='/' component={LandingMain}>
            {localStorage.getItem('logged_in') && <Redirect to="/main" /> }
          </Route>
          <Route path='/login' component={Login} />
          <Route path='/register' component={Register} />
          <PrivateRoute path='/main' component={LandingNav} />
        </Switch>
      </div>
    </Router> 

  );
}

export default MainApp;
