import { axios } from "@/services/axiosConfig";

const TagService = {
  async getAllTags() {
    try {
      const response = await axios.get('/tags/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getTagById(tagId) {
    try {
      const response = await axios.get(`/tags/${tagId}/`, { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  async searchTags(query) {
    try {
      const response = await axios.get(`tags/?search=${query}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async createTag(tagData) {
    try {
      console.log(tagData);
      const response = await axios.post('/tags/', JSON.stringify({
        name: tagData,
      }));
      return response.data;
    } catch (error) {
      throw error;
    }
    
  },

  async updateTag(tagId, tagData) {
    try {
      const response = await axios.put(`/tags/${tagId}/`, tagData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async deleteTag(tagId) {
    try {
      const response = await axios.delete(`/tags/${tagId}/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getFollowingTags() {
    try {
      const response = await axios.get('/user/following-tags/', { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async togglefollowTag(tagId) {
    try {
      const response = await axios.post(`/tags/${tagId}/toggle_follow/`, null, { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default TagService;