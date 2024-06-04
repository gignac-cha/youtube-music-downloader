export const timeout = (timeout: number) =>
  new Promise((resolve) => setTimeout(() => resolve(undefined), timeout));
