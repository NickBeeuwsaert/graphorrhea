import { useState, useEffect } from "preact/hooks";
import { html } from "htm/preact";
import { route } from "preact-router";
import Breadcrumbs from "./breadcrumbs.js";
import Table from "./table.js";
import * as paths from "../../path.js";
import useAPI from "../../hooks/useAPI.js";
import { AuthenticationError } from "../../graphorrhea.js";

function CellItem({ onCellClick, cell, children }) {
  return html`<button onClick=${() => onCellClick(cell)}>
    ${children}${cell.type === "notebook" && "/"}
  </button>`;
}

const COLUMNS = [
  {
    Header: "name",
    Cell: CellItem,
    key: "name",
  },
  {
    Header: "Type",
    key: "type",
  },
];

/**
 * @typedef MatchDict
 * @property {string?} match
 *
 * @typedef Props
 * @property {MatchDict?} matches
 * @property {string} path
 *
 * @property {Props} props
 */
export default function Browser({ matches = {} }) {
  const api = useAPI(),
    [directoryListing, setDirectoryListing] = useState([]),
    path = `/${paths.normalize(matches.path ?? "")}`;

  const changeDirectory = (newPath) => {
    const path = `/${paths.normalize(newPath)}`;
    route(`?${new URLSearchParams({ path })}`);
  };

  useEffect(() => {
    api
      .getResource(path)
      .then((data) => {
        setDirectoryListing(data["entries"]);
      })
      .catch((e) => {
        if (e instanceof AuthenticationError) {
          route("/login");
        } else {
          throw e;
        }
      });
  }, [path, api]);

  return html`<div>
    <${Breadcrumbs} path=${path} onChangePath=${changeDirectory} />
    <${Table}
      columns=${COLUMNS}
      rows=${directoryListing}
      onCellClick=${(cell) => {
        if (cell.type === "note") {
          route(
            `/edit?${new URLSearchParams({
              path: paths.join(path, cell.name),
            })}`
          );
        } else {
          changeDirectory(paths.join(path, cell.name));
        }
      }}
    />
  </div>`;
}
