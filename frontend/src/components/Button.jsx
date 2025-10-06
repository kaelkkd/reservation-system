import "../styles/Button.css";
import React from 'react'

function Button({ children, variant="primary", ...props}) {
    return (
        <button className={`btn btn--${variant}`} {...props}>
            {children}
        </button>
    )
}

export default Button
