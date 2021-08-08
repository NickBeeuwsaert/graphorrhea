import { useContext } from "preact/hooks";
import { fetchContext } from "../context.js";

export default function useFetch() {
  return useContext(fetchContext);
}
