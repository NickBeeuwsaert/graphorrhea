import { html } from "htm/preact";
import { h } from "preact";

const defaultCell = ({ children }) => children;

/**
 * @template T
 *
 * @typedef Column<T>
 * @property {string|VNode} Header
 * @property {(function(keyof T): VNode)?} render
 * @property {string} key
 *
 * @typedef Props<T>
 * @property {Column[]} columns
 * @property {T[]} rows
 * @property {function(T): void} onCellClick
 *
 * @param {Props} props
 */
export default function Table({ columns, rows, onCellClick }) {
  return html`
    <table>
      <thead>
        <tr>
          ${columns.map(({ Header }) => h(Header))}
        </tr>
      </thead>
      <tbody>
        ${rows.map((row) =>
          h(
            "tr",
            {},
            columns.map(({ key, Cell = defaultCell }) =>
              h(
                "td",
                {},
                h(
                  Cell,
                  { cell: row, onCellClick: (data) => onCellClick(data) },
                  row[key]
                )
              )
            )
          )
        )}
      </tbody>
    </table>
  `;
}
