// utils/sweetAlert.js

import Swal from "sweetalert2";

export const showAlert = (type, message, title = "") => {
  Swal.fire({
    icon: type,
    title: title,
    text: message,
  });
};

export const showSuccessAlert = (message, title = "Success") => {
  showAlert("success", message, title);
};

export const showErrorAlert = (error) => {
    let errorMessage = error.detail || error.message;

    Swal.fire({
        icon: "error",
        text:errorMessage,
    });
};
export const showInfoAlert = (message, title = "Info") => {
  showAlert("info", message, title);
};

export const showWarningAlert = (message, title = "Warning") => {
  showAlert("warning", message, title);
};
