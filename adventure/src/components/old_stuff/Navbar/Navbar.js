import React, { Component } from 'react';
import { MenuItems } from "./MenuItems"
import { Button } from "../Button"
import './Navbar.css'
import { BrowserRouter as Router, Switch, Route, Link, useRouteMatch, useParams } from 'react-router-dom'
import { getAdmin, removeAdmin } from '../Test/Adminify'


function Navbar() {

    let match = useRouteMatch()

    return(
        <div>
            <Nav />
            <Switch>
                {MenuItems.map((item, index) => {
                    return (
                        <Route path={`${match.path}${item.url}`} component={item.comp} exact={!item.url.localeCompare('') ? true : false} />
                        /*<Route path={`${match.path}${item.url}`} component={item.comp} exact={!item.url.localeCompare('/') ? true : false} />*/
                   ); 
                })}
            </Switch>
        </div>
    );
}

function Nav() {

    let match = useRouteMatch()

    return(
        <nav className="NavbarItems">
            <h1 className="navbar-title">ADventure</h1>
            <div className="menu-icon">
            </div>
            <ul className="nav-menu">
                {MenuItems.map((item, index) => {
                    return (
                       <Link to={`${match.url}${item.url}`}>
                            <li className={item.cName} key={index}> 
                                {item.title}
                            </li>
                       </Link>
                   ) 
                })}
            </ul>
            <Button onClick={() => {localStorage.clear();window.location.reload();}}>Logout</Button>
            <Button onClick={getAdmin}>Get Admin</Button>
            <Button onClick={removeAdmin}>Remove Admin</Button>
        </nav>
    );
}

 export default Navbar
