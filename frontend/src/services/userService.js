import { axios, axiosMultipart } from "@/services";

const userService = {
  // Función para crear un nuevo usuario
  async createUser(userData) {
    return await axiosMultipart.post("users/", userData);
  },

  // Función para obtener la información de un usuario por su ID
  async getUserById(userId) {
    try {
      const response = await axios.get(`/users/${userId}/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getUserSession() {
    try {
      const response = await axios.get('/users/logged/', { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getUserPartial() {
    try {
      const response = await axios.get('/users/partial/', { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Función para actualizar la información de un usuario
  async updateUser(userId, updatedUserData) {
    try {
      const response = await axios.put(`/users/${userId}`, updatedUserData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Función para eliminar un usuario por su ID
  async deleteUser(userId) {
    try {
      const response = await axios.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default userService;
