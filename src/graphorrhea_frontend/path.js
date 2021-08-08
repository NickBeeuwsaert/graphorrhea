const SEPARATOR = "/";
export const parts = (path, separator = SEPARATOR) =>
  path.split(separator).filter((separator) => separator.length);

export const normalize = (path, separator = SEPARATOR) =>
  parts(path, separator).join(separator);

export const join = (path, newPath, separator = SEPARATOR) =>
  [...parts(path, separator), ...parts(newPath, separator)].join(separator);

export const dirname = (path, separator = SEPARATOR) =>
  parts(path, separator).slice(0, -1).join(separator);
