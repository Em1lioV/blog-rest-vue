import { createStore } from 'vuex';
import { getAPI } from './axiosConfig';
import Cookies from 'js-cookie';
import { isTokenValid } from './util/tokenUtils';
export default createStore({
  state() {
    return {
      access_token: Cookies.get('access_token') || null
    }
  },
  mutations: {
    updateStorage(state, { access }) {
      state.access_token = access;

      Cookies.set('access_token', access, {
        secure: true,
        expires: 1,
      });

    },
    clearStorage(state) {
      state.access_token = null;

      Cookies.remove('access_token');
    },

  },
  getters: {
    validatedAccessToken(state) {
      return isTokenValid(state.access_token) ? state.access_token : null;
    },
  },
  actions: {
    async userLogin({ commit }, userCredentials) {
      try {
        const response = await getAPI.post('/token/', {
          email: userCredentials.email,
          password: userCredentials.password,
        });

        const access = response.data.access;
     

        commit('updateStorage', { access });

        return access;
      } catch (error) {
        commit('clearStorage');
        throw error;
      }
    },
    async refreshToken({ commit, dispatch }) {
      try {
        const response = await getAPI.post('/token/refresh/');
        const access = response.data.access;
    
        commit('updateStorage', { access });
        return true; // Return true indicating successful refresh
      } catch (error) {
        // Handle the error if the refresh request fails
        console.error('Error refreshing token:', error);
        return false; // Return false indicating failure to refresh
      }
    },
    async userLogout({ commit }) {
      try {
        const response = await getAPI.post('/logout/');
        if (response){
          commit('clearStorage');

        }
        return response;
      } catch (error) {
        throw error
      }
    },
  },
});
