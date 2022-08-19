import { html } from "htm/preact";
import { useState, useEffect } from "preact/hooks";
import { route } from "preact-router";
import useStore from "../hooks/useStore.js";
import useAPI from "../hooks/useAPI.js";
import { APIError } from "../graphorrhea.js";

const ACTIONS = {
  setAccessToken(state, accessToken) {
    return { accessToken };
  },
};

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
      const { accessToken } = await api.login(username, password);
      actions.setAccessToken(accessToken);
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
      className="form-container"
    >
      <div className="form-group">
        <label for="username">Username:</label>
        <input
          type="text"
          id="username"
          name="username"
          value=${username}
          onInput=${({ target }) => setUsername(target.value)}
        />
      </div>
      <div className="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value=${password}
          onInput=${({ target }) => setPassword(target.value)}
        />
      </div>
      <div class="form-buttons">
        <button className="form-button primary">
          Login
        </button>
      </div>
    </form>
  `;
}
