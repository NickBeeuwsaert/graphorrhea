import { html } from "htm/preact";
import { h } from "preact";
import * as paths from "../../path.js";

const HOME = String.fromCodePoint(0x1f3e0);

/**
 * @typedef BreadcrumbItem
 * @property {string} component
 * @property {function(): void} onClick
 *
 * @param {BreadcrumbItemProps} props
 */
function BreadcrumbItem({ component, onClick }) {
  return html`
    <li>
      <button onClick=${onClick}>${component}</button>
    </li>
  `;
}

/**
 * @typedef BreadcrumbProps
 * @property {string[]} path
 * @property {function(string): void} onChangePath
 *
 * @param {BreadcrumbProps} props
 */
export default function Breadcrumbs({ path, onChangePath }) {
  const pathSegments = paths.parts(path);
  return html`
    <ul className="breadcrumbs">
      <li>
        <${BreadcrumbItem}
          onClick=${() => onChangePath("")}
          component=${HOME}
        />
      </li>
      ${pathSegments.map((component, i) =>
        h(BreadcrumbItem, {
          component,
          onClick() {
            onChangePath(pathSegments.slice(0, i + 1).join("/"));
          },
        })
      )}
    </ul>
  `;
}
