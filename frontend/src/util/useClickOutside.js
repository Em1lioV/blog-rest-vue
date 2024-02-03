import { onMounted, onUnmounted } from 'vue';

export default function useClickOutside(elementRef, callback) {
  const handleClickOutside = (event) => {
    if (elementRef.value && elementRef.value instanceof HTMLElement && !elementRef.value.contains(event.target)) {
      callback();
    }
  };

  onMounted(() => {
    document.addEventListener('click', handleClickOutside);
  });

  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
  });
}
