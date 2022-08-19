import { html } from "htm/preact";
import { useEffect, useState } from "preact/hooks";
import { route, Link } from "preact-router";
import useAPI from "../hooks/useAPI.js";
import * as paths from "../path.js";
import { AuthenticationError } from "../graphorrhea.js";

/**
 * @typedef MatchDict
 * @property {string?} path
 *
 * @typedef Props
 * @property {MatchDict?} matches
 *
 * @param {Props} props
 */
export default function Editor({ matches = {} }) {
  const api = useAPI(),
    path = `/${paths.normalize(matches.path ?? "")}`,
    [content, setContent] = useState(null);

  useEffect(() => {
    api
      .getResource(path)
      .then((payload) => {
        switch (payload.type) {
          case "note":
            setContent(payload["content"]);
            break;
          case "directory":
            // Why are you tring to view a directory in a text editor? weirdo.
            route("/");
            break;
          default:
            console.error(
              `Something weird happened, not supposed to have a ${paylaod.type}`
            );
        }
      })
      .catch((e) => {
        if (e instanceof AuthenticationError) {
          route("/login");
        } else {
          throw e;
        }
      });
  }, [path, api]);

  const handleSave = () => {
    api.writeNote(path, content).catch((e) => {
      if (e instanceof AuthenticationError) {
        route("/login");
      } else {
        throw e;
      }
    });
  };

  return html`
    <div>
      <button onClick="${handleSave}" aria-label="Save">
        ${String.fromCodePoint(0x1f4be)} Save
      </button>

      <${Link} href="/?paths=${paths.dirname(path)}">Back to browser</${Link}>

      <span
        >Editing: <input type="text" readonly disabled value=${path}
      /></span>
    </div>
    <textarea
      onInput=${({ target }) => setContent(target.value)}
      className="editor"
    >
${content}</textarea
    >
  `;
}
