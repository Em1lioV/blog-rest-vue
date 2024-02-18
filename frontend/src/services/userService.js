import { getAPI, getAPImultipart } from "@/services/axiosConfig";

const userService = {
  // Función para crear un nuevo usuario
  async createUser(userData) {
    return await getAPImultipart.post("users/", userData);
  },

  // Función para obtener la información de un usuario por su ID
  async getUserById(userId) {
    try {
      const response = await getAPI.get(`/users/${userId}/`);
      return response.data;
    } catch (error) {
      throw new Error("Error getting user by ID: " + error.message);
    }
  },

  async getUserSession() {
    try {
      const response = await getAPI.get('/users/logged/', { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw new Error("Error getting user by ID: " + error.message);
    }
  },

  async getUserPartial() {
    try {
      const response = await getAPI.get('/users/partial/', { requiresAuth: true });
      return response.data;
    } catch (error) {
      return error;
    }
  },

  // Función para actualizar la información de un usuario
  async updateUser(userId, updatedUserData) {
    try {
      const response = await getAPI.put(`/users/${userId}`, updatedUserData);
      return response.data;
    } catch (error) {
      throw new Error("Error updating user: " + error.message);
    }
  },

  // Función para eliminar un usuario por su ID
  async deleteUser(userId) {
    try {
      const response = await getAPI.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw new Error("Error deleting user: " + error.message);
    }
  },
};

export default userService;
