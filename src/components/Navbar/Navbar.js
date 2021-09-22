import React, { Component } from 'react';
import { MenuItems } from "./MenuItems"
import { Button } from "../Button"
import './Navbar.css'
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom'


class Navbar extends Component {
    state = { clicked: false }

    render() {
        return(
            <Router>
                <Nav />
                <Switch>
                    {MenuItems.map((item, index) => {
                        return (
                            <Route path={item.url} component={item.comp} exact={!item.url.localeCompare('/') ? true : false} />
                       ); 
                    })}
                </Switch>
            </Router> 
        );
    }
}

function Nav() {
    return(
        <nav className="NavbarItems">
            <h1 className="navbar-title">ADventure</h1>
            <div className="menu-icon">
            </div>
            <ul className="nav-menu">
                {MenuItems.map((item, index) => {
                    return (
                       <Link to={item.url}>
                            <li className={item.cName} key={index}> 
                                {item.title}
                            </li>
                       </Link>
                   ) 
                })}
            </ul>
            <Button>Sign Up</Button>
        </nav>
    );
}

 export default Navbar
