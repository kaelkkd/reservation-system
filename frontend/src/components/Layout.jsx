import { Link, useLocation } from "react-router-dom"
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
                    <Link className={pathname.startsWith("/logout") ? "active" : ""} to="/logout">Logout</Link>
                </nav>
            </header>

            <main className="content container">
                {children}
            </main>
        </div>
    );
}   

export default Layout;