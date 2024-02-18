import { createStore } from "vuex";
import { getAPI } from "@/services/axiosConfig";
import Cookies from "js-cookie";
import router from "./router";

export default createStore({
  state() {
    return {
      access_token: Cookies.get("access_token") || null,
    };
  },
  mutations: {
    updateStorage(state, { access }) {
      state.access_token = access;

      Cookies.set("access_token", access, {
        secure: true,
        expires: 1,
      });
    },
    clearStorage(state) {
      state.access_token = null;
    },
  },
  getters: {
    accessToken: (state) => state.access_token,
  },
  actions: {
    async refreshToken({ commit, dispatch }) {
      try {
        const newAccessToken = await getAPI.post("/token/refresh/");
        const access = newAccessToken.data.access;
        commit("updateStorage", { access });
        return access;
      } catch (error) {
        console.error("Error al refrescar el token:", error.response?.data || error.message);
   
        await dispatch("userLogout");
      
    
        throw error;
      }
    },

    async userLogin({ commit, dispatch }, userCredentials) {
      try {
        const response = await getAPI.post("token/", {
          email: userCredentials.email,
          password: userCredentials.password,
        });

        const access = response.data.access;
        commit("updateStorage", { access });

        return access;
      } catch (error) {
        commit("clearStorage");
        throw error;
      }
    },
    async userLogout({ commit, state }) {
      try {
        if (state.access_token) {
          await getAPI.post("/logout/");
          commit("clearStorage");
          router.push("/login");
        }
      } catch (error) {
        console.error("Error al cerrar sesión:", error.response?.data || error.message);
        throw error;
      }
    },
  },
});
