import { useCallback, useEffect, useRef } from 'react';

export const useAnimationFrame = (task: () => Promise<unknown>) => {
  const isRunning = useRef(false);
  const requestID = useRef(-1);

  const callback = useCallback(async () => {
    if (isRunning.current) {
      await task();
    } else {
      requestID.current = -1;
    }
    requestAnimationFrame(callback);
  }, []);

  const start = useCallback(() => {
    isRunning.current = true;
    requestID.current = requestAnimationFrame(callback);
  }, []);

  const stop = useCallback(() => {
    isRunning.current = false;
    cancelAnimationFrame(requestID.current);
  }, []);

  useEffect(() => {
    return () => stop();
  }, []);

  return { start, stop };
};
