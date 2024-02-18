import Swal from "sweetalert2";

const sweetAlert = {
  showAlert(type, message, title = "") {
    Swal.fire({
      icon: type,
      title: title,
      text: message,
    });
  },

  showSuccessAlert(message, title = "Success") {
    this.showAlert("success", message, title);
  },

  showErrorAlert(error) {
    let errorMessage = error.detail || error.message;

    Swal.fire({
      icon: "error",
      text: errorMessage,
    });
  },

  showInfoAlert(message, title = "Info") {
    this.showAlert("info", message, title);
  },

  showWarningAlert(message, title = "Warning") {
    this.showAlert("warning", message, title);
  },
};

export default sweetAlert;