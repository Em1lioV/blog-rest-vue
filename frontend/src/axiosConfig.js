import axios from "axios";
import store from "@/store";
import { jwtDecode } from "jwt-decode";

let isRefreshing = false;
let refreshSubscribers = [];

const configureAxios = (baseURL, headers) => {
  const instance = axios.create({
    baseURL,
    headers,
    withCredentials: true,
  });

  let refreshTokenPromise = null;

  instance.interceptors.request.use(async (config) => {
    const requiresAuth = config.requiresAuth || false;

    if (requiresAuth) {

      if (!store.getters.accessToken) {
        console.log("No hay token de acceso. Configuración enviada directamente.");
        return config;
      }

      const decodedToken = jwtDecode(store.getters.accessToken);
      const currentTime = Date.now() / 1000;

      if (decodedToken.exp && decodedToken.exp < currentTime) {
        if (!isRefreshing) {
          isRefreshing = true;

          // Inicia la renovación del token si no hay una ya en progreso
          refreshTokenPromise = refreshTokenPromise || store.dispatch("refreshToken");

          try {
            const newAccessToken = await Promise.race([
              refreshTokenPromise,
              new Promise((_, reject) =>
                setTimeout(() => reject(new Error("Timeout")), 5000)
              ),
            ]);

            if (newAccessToken) {
              console.log("Token de acceso renovado con éxito, nuevo token: " + newAccessToken);
              config.headers.Authorization = `Bearer ${newAccessToken}`;
              refreshSubscribers.forEach((callback) => callback(newAccessToken));
              return config;
            } else {
              console.log("La renovación del token falló. Desconectando usuario y cancelando solicitudes pendientes.");
              refreshSubscribers.forEach((callback) => callback(null));
            }
          } catch (error) {
            console.error("Error durante la renovación del token:", error);
          } finally {
            isRefreshing = false;
            newAccessToken = null
            refreshSubscribers = [];
            refreshTokenPromise = null;
          }
        }

        // Asigna el controlador de aborto a la configuración
        const controller = new AbortController();
        config.signal = controller.signal;

        return new Promise((resolve, reject) => {
          refreshSubscribers.push((newAccessToken) => {
            if (newAccessToken) {
              console.log("Token de acceso renovado. Resolviendo la promesa con la configuración actualizada.");
              config.headers.Authorization = `Bearer ${newAccessToken}`;
              resolve(config);
            } else {
              console.log("No hay nuevo token de acceso. Rechazando la promesa.");
              reject(new Error("No new access token"));
            }
          });
        }).catch((error) => {
          console.error("Error durante la renovación del token:", error);
          console.log("Cancelando la solicitud actual...");
          controller.abort();
          throw error;
        });
      }

      console.log("Configurando la solicitud con el token de acceso existente.");
      config.headers.Authorization = `Bearer ${store.getters.accessToken}`;
    }

    return config;
  });

  return instance;
};

export const getAPI = configureAxios("/api", {

  
  "Content-Type": "application/json",
});
export const getAPImultipart = configureAxios("/api", {
  "Content-Type": "multipart/form-data",
});
