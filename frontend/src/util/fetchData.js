import { getAPI } from '../axios';
import store from '@/store';  // Importa useStore para acceder al store de Vuex

export const fetchData = async (url, options = {}) => {
  try {


    // Validación de URL
    if (typeof url !== 'string' || !url) {
      throw new Error('URL de solicitud no válida');
    }

    // Validación de opciones de solicitud
    if (typeof options !== 'object') {
      throw new Error('Opciones de solicitud no válidas');
    }

    // Verificación de tokens y configuración de encabezados de autorización
    if (store.state.access_token) {
      if (!options.headers) {
        options.headers = {};
      }
      options.headers.Authorization = `Bearer ${store.state.access_token}`;
    }

    // Límite de tiempo de solicitud
    options.timeout = options.timeout || 10000; // 10 segundos por defecto

    const response = await getAPI.request({
      url,
      ...options,
    });

    // Validación de la respuesta
    if (!response || response.status !== 200) {
      throw new Error('Respuesta de solicitud no válida');
    }

    return response.data;
  } catch (error) {
    // Manejo de errores
    if (error.response && error.response.status === 401) {
      // Intenta refrescar el token utilizando la función refreshToken del store
      try {
        await store.dispatch('refreshToken');
        // Después de refrescar el token, realiza la solicitud nuevamente con el nuevo token de acceso
        return await fetchData(url, options);
      } catch (refreshError) {
        // Error en el refresco del token
        console.error('Error al refrescar el token:', refreshError);
        throw refreshError;
      }
    } else {
      // Otro tipo de error
      console.error('Error al obtener datos:', error);
      throw error;
    }
  }
};
