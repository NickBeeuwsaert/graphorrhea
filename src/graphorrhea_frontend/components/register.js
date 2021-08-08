import { html } from "htm/preact";
import { useState, useEffect } from "preact/hooks";
import { route } from "preact-router";
import useStore from "../hooks/useStore.js";
import useAPI from "../hooks/useAPI.js";
import { APIError } from "../graphorrhea.js";
import styles from "./form.module.css";

const ACTIONS = {};

export default function Login() {
  const [accessToken, actions] = useStore("accessToken", ACTIONS);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const api = useAPI();

  useEffect(() => {
    if (accessToken) route("/");
  }, [accessToken]);

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      await api.register(username, password);
      route("/");
    } catch (e) {
      if (e instanceof APIError) {
        console.error(e);
      } else {
        throw e;
      }
    }
  }

  return html`
    <form
      method="POST"
      onSubmit=${handleSubmit}
      className=${styles["form-container"]}
    >
      <div className=${styles["form-group"]}>
        <label for="username">Username:</label>
        <input
          type="text"
          id="username"
          name="username"
          value=${username}
          onInput=${({ target }) => setUsername(target.value)}
        />
      </div>
      <div className=${styles["form-group"]}>
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value=${password}
          onInput=${({ target }) => setPassword(target.value)}
        />
      </div>
      <div class=${styles["form-buttons"]}>
        <button className=${`${styles["form-button"]} ${styles["primary"]}`}>
          Register
        </button>
      </div>
    </form>
  `;
}
