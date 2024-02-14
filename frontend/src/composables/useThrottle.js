// useThrottle.js
import { ref } from 'vue';

export default function useThrottle(callback, delay) {
  let timerId = null;
  const lastArgs = ref(null);

  const throttledFunction = (...args) => {
    lastArgs.value = args;
    if (!timerId) {
      timerId = setTimeout(() => {
        callback(...lastArgs.value);
        timerId = null;
      }, delay);
    }
  };

  return throttledFunction;
}
