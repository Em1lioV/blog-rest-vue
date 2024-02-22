import { axios } from "@/services";

const roleService = {
  // Función para crear un nuevo usuario
  async createRole(description) {
    return await axios.post(
      "roles/",
      JSON.stringify({
        description: description,
      })
    );
  },

  // Función para obtener la información de un usuario por su ID
  async listRolesByQuery(query) {
    try {
      const response = await axios.get("roles/?description=" + query);
      return response;
    } catch (error) {
      throw error;
    }
  },
};


export default roleService;
