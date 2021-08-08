import { html } from "htm/preact";
import { Link } from "preact-router";
import styles from "./nav.module.css";
import useStore from "../hooks/useStore.js";

const ACTIONS = {
  logout(state) {
    return { accessToken: null };
  },
};

export default function Nav() {
  const [accessToken, actions] = useStore("accessToken", ACTIONS);

  return html`
    <nav className=${styles.nav}>
      <h1>Graphorrhea</h1>

      <ul className=${styles["nav-menu"]}>
        ${accessToken && html`<li><${Link} href="/">Home</${Link}></li>`}
        ${accessToken &&
        html`<li><${Link} onClick=${actions.logout} href="/">Logout</${Link}></li>`}
        ${!accessToken && html`<li><${Link} href="/login">Login</${Link}></li>`}
        ${!accessToken &&
        html`<li><${Link} href="/register">Register</${Link}></li>`}
      </ul>
    </nav>
  `;
}
