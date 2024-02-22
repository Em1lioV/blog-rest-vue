import axiosInstance  from "axios";
import store from "@/store";
import { jwtDecode } from "jwt-decode";
import { getValidationError, sweetAlert } from "@/util";

let isRefreshing = false;
let refreshSubscribers = [];
let refreshTokenPromise = null;

const configureAxios = (baseURL, headers) => {
  const instance = axiosInstance.create({
    baseURL,
    headers,
    withCredentials: true,
  });

  instance.interceptors.request.use(async (config) => {
    const requiresAuth = config.requiresAuth || false;

    if (!requiresAuth || !store.getters.accessToken) {
      return config;
    }

    const decodedToken = jwtDecode(store.getters.accessToken);
    const currentTime = Date.now() / 1000;

    if (decodedToken.exp && decodedToken.exp >= currentTime) {
      config.headers.Authorization = `Bearer ${store.getters.accessToken}`;
      return config;
    }

    if (isRefreshing) {
      console.log("Token de acceso caducado. Esperando renovación.");
      await waitForRefresh();
    }

    refreshTokenPromise = refreshTokenPromise || store.dispatch("refreshToken");

    try {
      const newAccessToken = await Promise.race([
        refreshTokenPromise,
        new Promise((_, reject) => setTimeout(reject, 5000)),
      ]);

      if (!newAccessToken) {
        throw new Error("Token renewal failed");
      }

      config.headers.Authorization = `Bearer ${newAccessToken}`;
      return config;
    } catch (error) {
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
        resolve();
      } else {
        reject();
      }
    });
  });
};

export const axios = configureAxios("/api", {
  "Content-Type": "application/json",
});

export const axiosMultipart = configureAxios("/api", {
  "Content-Type": "multipart/form-data",
});
