import { createContext } from "preact";

export const StoreContext = createContext(null);
export const FetchContext = createContext((...args) => self.fetch(...args));
