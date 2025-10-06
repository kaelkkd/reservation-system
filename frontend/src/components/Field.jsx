import "../styles/Form.css";

export function Field({ label, error, children }) {
  return (
    <label className={`field ${error ? "field--error" : ""}`}>
      <span className='field__label'>{label}</span>
      {children}
      {error ? <span className='field__error'>{error}</span> : null}
    </label>
  );
}

export function Input(props) {
  return <input className='input' {...props} />;
}

export function Select(props) {
  return <select className='input' {...props} />;
}
