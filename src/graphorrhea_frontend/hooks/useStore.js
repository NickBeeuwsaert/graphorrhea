import { StoreContext } from "../context.js";
import { useContext, useState, useMemo, useEffect } from "preact/hooks";

/**
 * @template T
 *
 * @param {T} store
 * @param {Object.<string, function(T, ...): Partial<T>} actions
 * @returns
 */
function bindActions(store, actions) {
  return Object.fromEntries(
    Object.entries(actions).map(([key, action]) => [key, store.action(action)])
  );
}

function runReducer(state, reducer) {
  if (typeof reducer === "string") return state[reducer];
  if (Array.isArray(reducer)) {
    return Object.fromEntries(reducer.map((key) => [key, state[key]]));
  }
  return reducer(state);
}

export default function useStore(reducer, actions) {
  const store = useContext(StoreContext),
    [state, setState] = useState(runReducer(store.getState(), reducer)),
    boundActions = useMemo(() => bindActions(store, actions), [store, actions]);

  // Note: unistores subscribe function returns a unsubscribe callback
  // be careful when refactoring to return it from the useEffect hook
  useEffect(
    () =>
      store.subscribe((newState) => {
        setState(runReducer(newState, reducer));
      }),
    [reducer]
  );

  return [state, boundActions];
}
