import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Button, Navbar, Nav, Fade } from 'react-bootstrap'
import { BrowserRouter as Router, Switch, Route, Link, NavLink, useRouteMatch } from 'react-router-dom'
import './landingpage-css.css'
import { MenuItems } from '../MenuItems'

export function LandingNav() {

  let match = useRouteMatch()

  return (
    <div>
      <Navbar bg="light" expand="lg">
        <Navbar.Brand >
                  <NavLink to="/">ADventure</NavLink>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
          {localStorage.getItem('logged_in') 
          ? (
            <Navbar.Collapse className='justify-content-end' id="basic-navbar-nav">
                {MenuItems.map((item, index) => {
                    return (
                      <Nav.Link>
                        <NavLink to={`${match.url}${item.url}`}>{item.title}</NavLink>
                      </Nav.Link>
                   ) 
                })}
                <Nav.Link>
                  <Button onClick={() => {localStorage.clear();window.location.reload();}}>Logout</Button>
                </Nav.Link>
            </Navbar.Collapse>
          ) : ( 
            <LandingLoggedOut/>
          )}
      </Navbar>
      {localStorage.getItem('logged_in') &&
        <Switch>
            {MenuItems.map((item, index) => {
                return (
                    <Route path={`${match.path}${item.url}`} component={item.comp} exact={!item.url.localeCompare('') ? true : false} />
               ); 
            })}
        </Switch>
      }
    </div>
  );
};

function LandingLoggedOut() {
  return (
    <Navbar.Collapse className='justify-content-end' id="basic-navbar-nav">
        <Nav.Link>
          <NavLink to="/login">Login</NavLink>
        </Nav.Link>
        <Nav.Link>
          <NavLink to="/register">Register</NavLink>
        </Nav.Link>
        <Nav.Link>
          <NavLink to="/admin_login">Admin Login</NavLink>
        </Nav.Link>
    </Navbar.Collapse>
  );
}

export function LandingMain() {

  return (
    <div class="center">
      <Fade appear={true} in={true}>
      <div>
          <h4> Welcome to ADventure </h4>
      </div>
      </Fade>
    </div>

  );
};
