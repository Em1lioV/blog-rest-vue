import { ref, onUnmounted } from "vue";

const useFileInput = (emitUpdateModelValue) => {
  const fileUrl = ref(null);
  const fileInput = ref(null);

  const openFileInput = () => {
    if (fileInput.value) {
      fileInput.value.click();
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      fileUrl.value = URL.createObjectURL(file);
      emitUpdateModelValue(file);
    }
  };

  const removeFile = () => {
    fileUrl.value = null;
    fileInput.value.value = null;
    emitUpdateModelValue(null);
  };

  onUnmounted(() => {
    if (fileUrl.value) {
      URL.revokeObjectURL(fileUrl.value);
    }
  });

  return {
    fileUrl,
    fileInput,
    openFileInput,
    handleFileChange,
    removeFile,
  };
};

export default useFileInput;
