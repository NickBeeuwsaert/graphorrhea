import { useState, useEffect, useCallback } from "preact/hooks";

const setItem = (key) => (value) =>
  window.localStorage.setItem(key, JSON.stringify(value));
const getItem = (key, defaultValue) => {
  const item = window.localStorage.getItem(key);
  try {
    return JSON.parse(item);
  } catch (e) {
    return defaultValue;
  }
};
/**
 * Helper hook to store a value in local-storage.
 *
 * Meant for tracking values across requests (e.g. a refresh token)
 *
 * @param {string} name
 * @param {any} initialValue
 * @returns
 */
export default function useLocalStorage(name, initialValue) {
  const [value, setValue] = useState(getItem(name, initialValue)),
    set = useCallback(setItem(name), [name]);

  useEffect(() => {
    const handleStorageEvent = ({ key, newValue, storageArea }) => {
      if (storageArea !== window.localStorage) return;
      if (key != name) return;

      setValue(newValue);
    };
    window.addEventListener("storage", handleStorageEvent);
    return () => window.removeEventListener("storage", handleStorageEvent);
  }, [name]);

  return [value, set];
}
