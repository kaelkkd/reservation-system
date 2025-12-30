import { Link, useLocation } from "react-router-dom"
import { BsPersonCircle, BsArrowBarRight  } from "react-icons/bs";
import "../styles/Layout.css"
import React from 'react'

function Layout({ children }) {
    const { pathname } = useLocation();

    return (
        <div className="layout">
            <header className="nav">
                <div className="nav__brand">
                    <span className="brand__logo">RS</span>
                    <span className="brand__name">Reservation System</span>
                </div>
                <nav className="nav__links">
                    <Link className={pathname.startsWith("/locations") ? "active": ""} to="/locations">Locations</Link>
                    <Link className={pathname.startsWith("/reservations") ? "active": ""} to="/reservations">My reservations</Link>
                    <Link className={pathname.startsWith("/profiles/me") ? "active" : ""} to="/profiles/me">My profile</Link>
                    <Link className={pathname.startsWith("/logout") ? "active" : ""} to="/logout"><BsArrowBarRight/></Link>
                </nav>
            </header>

            <main className="content container">
                {children}
            </main>
        </div>
    );
}   

export default Layout;