import { render } from "preact";
import { Router } from "preact-router";
import { html } from "htm/preact";
import createStore from "unistore";
import { createHashHistory } from "history";
import { StoreContext } from "./context.js";
import Login from "./components/login.js";
import Register from "./components/register.js";
import Browser from "./components/browser/main.js";
import Editor from "./components/editor.js";
import Nav from "./components/nav.js";
import "./main.module.css";

const store = createStore({ accessToken: null });

function App({ store }) {
  return html`
  <${StoreContext.Provider} value=${store}>
      <${Nav}/>
      <${Router} history=${createHashHistory()}>
        <${Browser} path="/"/>
        <${Login} path="/login"/>
        <${Register} path="/register"/>
        <${Editor} path="/edit"/>
      </${Router}>
      </${StoreContext.Provider}>
  `;
}

render(html` <${App} store=${store} />`, document.body);
