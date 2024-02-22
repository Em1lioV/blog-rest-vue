import { axios, axiosMultipart } from "@/services/axiosConfig";

const PostService = {
  async createPost(PostData) {
    return await axiosMultipart.post("posts/", PostData, { requiresAuth: true });
  },

  async getPostById(PostId) {
    try {
      const response = await axios.get(`/posts/${PostId}/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  async getPostsUserByRequest() {
    try {
      const response = await axios.get('/users/posts/', { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  async getPostsUserById(UserId) {
    try {
      const response = await axios.get(`/users/posts/${UserId}/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async updatePost(PostSlug, updatedPostData) {
    try {
      const response = await axios.put(`/posts/${PostSlug}`, updatedPostData);
      return response.data;
    } catch (error) {
      throw new Error("Error updating Post: " + error.message);
    }
  },

  async deletePost(PostSlug) {
    try {
      const response = await axios.delete(`/posts/${PostSlug}`);
      return response.data;
    } catch (error) {
      throw new Error("Error deleting Post: " + error.message);
    }
  },
};

export default PostService;
