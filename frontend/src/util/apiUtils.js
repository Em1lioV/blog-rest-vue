import { getAPI, getAPImultipart } from '../axiosConfig';
import { isTokenValid } from './tokenUtils';
import store from '@/store';

const validateRequest = (url, data, options) => {
  if (typeof url !== 'string' || !url || typeof options !== 'object') {
    throw new Error('URL de solicitud u opciones no válidas');
  }
};


const addTokenToOptions = async (options) => {
  if (store.getters.validatedAccessToken) {
    if (!options.headers) {
      options.headers = {};
    }
    options.headers.Authorization = `Bearer ${store.state.access_token}`;
    console.log('Token agregado a las opciones:', options.headers.Authorization);
  } else {
    return
  }
};

// ...

export const fetchData = async (url, options = {}, token = false) => {
  validateRequest(url, null, options);

  try {
    if (token){
      await addTokenToOptions(options);
    }

    const response = await getAPI.request({
      url,
      method: 'get',
      ...options,
    });

    return response.data;
  } catch (error) {
    console.error('Error al obtener datos:', error);
    throw error;
  }
};

// ...

export const postData = async (url, data, isMultipart = false,token=false, options = {}) => {
  validateRequest(url, data, options);

  try {
    if (token){
      await addTokenToOptions(options);
    }
  
    const instance = isMultipart ? getAPImultipart : getAPI;
    const response = await instance.post(url, data, options);
  
    if (!response || response.status !== 200 && response.status !== 201) {
      throw new Error('Respuesta de solicitud no válida');
    }
  
    return response;
  } catch (error) {
    console.error('Error al realizar post:', error);
    throw error;
  }
};
