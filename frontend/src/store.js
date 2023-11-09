import { createStore } from 'vuex';
import { getAPI } from './axios';
import Cookies from 'js-cookie';

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
    async refreshToken({ commit, state }) {
      try {
        const response = await getAPI.post('/token/refresh/');

        const access = response.data.access;
        commit('updateStorage', { access });

        return access;
      } catch (error) {
        throw error;
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
