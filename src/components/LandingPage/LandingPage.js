import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Navbar, Nav, Fade } from 'react-bootstrap'
import { BrowserRouter as Router, Switch, Route, Link, NavLink } from 'react-router-dom'
import { UrlBase } from '../config'
import './landingpage-css.css'
import Login from '../Auth/Login'
import Register from '../Auth/Register'

export function LandingNav() {

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
                <Nav.Link>
                  <NavLink to="/login">test</NavLink>
                </Nav.Link>
                <Nav.Link>
                  <NavLink to="/register">test2</NavLink>
                </Nav.Link>
            </Navbar.Collapse>
          ) : ( 

            <Navbar.Collapse className='justify-content-end' id="basic-navbar-nav">
                <Nav.Link>
                  <NavLink to="/login">Login</NavLink>
                </Nav.Link>
                <Nav.Link>
                  <NavLink to="/register">Register</NavLink>
                </Nav.Link>
            </Navbar.Collapse>
          )}
      </Navbar>
    </div>
  );
};

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
