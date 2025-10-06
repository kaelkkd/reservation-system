import "../styles/Card.css";

function Card({ children, header, footer }) {
    return (
        <section className="card">
            {header ? <div className="card__header">{header}</div> : null}
            <div className="card__body">{children}</div>
            {footer ? <div className="card__footer">{footer}</div> : null}
        </section>
    );
}

export default Card;