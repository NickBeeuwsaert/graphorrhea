import { useContext, useMemo } from "preact/hooks";
import { route } from "preact-router";
import { FetchContext } from "../context.js";
import useStore from "../hooks/useStore";
import Graphorrhea, { AuthenticationError } from "../graphorrhea.js";

const ACTIONS = {};
const apiBase = "http://127.0.0.1:6543/api/v1/";

export default function useAPI() {
  const fetch = useContext(FetchContext);
  const [accessToken] = useStore("accessToken", ACTIONS);

  const api = useMemo(
    () =>
      new Graphorrhea(apiBase, (...args) => {
        const request = new Request(...args);
        if (accessToken) {
          request.headers.set("Authorization", `Bearer ${accessToken}`);
        }

        return fetch(request);
      }),
    [accessToken]
  );

  return api;
}
