const plural = (value: number) => (value === 1 ? 's' : '');

export const convertFileSize = (size: number) => {
  if (size < 1024) {
    return `${size} Byte${plural(size)}`;
  }
  size /= 1024;
  if (size < 1024) {
    return `${size.toFixed(2)} KB`;
  }
  size /= 1024;
  if (size < 1024) {
    return `${size.toFixed(2)} MB`;
  }
  size /= 1024;
  if (size < 1024) {
    return `${size.toFixed(2)} GB`;
  }
  size /= 1024;
  if (size < 1024) {
    return `${size.toFixed(2)} TB`;
  }
  size /= 1024;
  if (size < 1024) {
    return `${size.toFixed(2)} PB`;
  }
  return Infinity;
};
