import "../styles/Table.css";

function Table({ columns, rows, empty = "No data." }) {
  return (
    <div className="table">
        <table>
            <thead>
                <tr>{columns.map(c => <th key={c.key || c.header}>{c.header}</th>)}</tr>
            </thead>
            <tbody>
                {rows.length === 0 ? (
                    <tr><td colSpan={columns.length} className="table__empty">{empty}</td></tr>
                ) : rows.map((r, idx) => (
                    <tr key={r.id || r.key || idx}>
                        {columns.map(c => <td key={c.key || c.header}>{c.render ? c.render(r) : r[c.accessor]}</td>)}
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
  );
}

export default Table;