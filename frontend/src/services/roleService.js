import { getAPI } from "@/services/axiosConfig";

const roleService = {
  // Función para crear un nuevo usuario
  async createRole(description) {
    return await getAPI.post(
      "roles/",
      JSON.stringify({
        description: description,
      })
    );
  },

  // Función para obtener la información de un usuario por su ID
  async listRolesByQuery(query) {
    try {
      const response = await getAPI.get("roles/?description=" + query);
      return response;
    } catch (error) {
      throw error;
    }
  },
};


export default roleService;
