import axios from "axios";
import store from "@/store";
import { jwtDecode } from "jwt-decode";
import { getValidationError, sweetAlert } from "@/util";

let isRefreshing = false;
let refreshSubscribers = [];
let refreshTokenPromise = null;

const configureAxios = (baseURL, headers) => {
  const instance = axios.create({
    baseURL,
    headers,
    withCredentials: true,
  });

  instance.interceptors.request.use(async (config) => {
    const requiresAuth = config.requiresAuth || false;

    if (!requiresAuth || !store.getters.accessToken) {
      console.log("No se requiere autenticación o no hay token de acceso.");
      return config;
    }

    const decodedToken = jwtDecode(store.getters.accessToken);
    const currentTime = Date.now() / 1000;

    if (decodedToken.exp && decodedToken.exp >= currentTime) {
      console.log("El token de acceso es válido.");
      config.headers.Authorization = `Bearer ${store.getters.accessToken}`;
      return config;
    }

    if (isRefreshing) {
      console.log("Token de acceso caducado. Esperando renovación.");
      await waitForRefresh();
    }

    console.log("Iniciando la renovación del token de acceso.");
    refreshTokenPromise = refreshTokenPromise || store.dispatch("refreshToken");

    try {
      const newAccessToken = await Promise.race([
        refreshTokenPromise,
        new Promise((_, reject) => setTimeout(reject, 5000)),
      ]);

      if (!newAccessToken) {
        console.log("La renovación del token de acceso falló.");
        throw new Error("Token renewal failed");
      }

      console.log("Token de acceso renovado con éxito:", newAccessToken);
      config.headers.Authorization = `Bearer ${newAccessToken}`;
      return config;
    } catch (error) {
      console.error("Error durante la renovación del token:", error);
      throw error;
    }
  });

  instance.interceptors.response.use(null, (err) => {
    const error = getValidationError(err);

    if (Object.keys(error.validation).length === 0) {
      sweetAlert.showErrorAlert(error);
    }

    return Promise.reject(error);
  });

  return instance;
};

const waitForRefresh = () => {
  return new Promise((resolve, reject) => {
    refreshSubscribers.push((newAccessToken) => {
      if (newAccessToken) {
        console.log("Token de acceso renovado.");
        resolve();
      } else {
        console.log("La renovación del token de acceso falló.");
        reject();
      }
    });
  });
};

export const getAPI = configureAxios("/api", {
  "Content-Type": "application/json",
});

export const getAPImultipart = configureAxios("/api", {
  "Content-Type": "multipart/form-data",
});
