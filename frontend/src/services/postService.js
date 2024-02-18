import { getAPI, getAPImultipart } from "@/services/axiosConfig";

const PostService = {
  async createPost(PostData) {
    return await getAPImultipart.post("posts/", PostData, { requiresAuth: true });
  },

  async getPostById(PostId) {
    try {
      const response = await getAPI.get(`/posts/${PostId}/`);
      console.log(response);
      return response.data;
    } catch (error) {
      return error;
    }
  },
  async getPostsUserByRequest() {
    try {
      const response = await getAPI.get('/users/posts/', { requiresAuth: true });
      return response.data;
    } catch (error) {
      return error;
    }
  },
  
  async getPostsUserById(UserId) {
    try {
      const response = await getAPI.get(`/users/posts/${UserId}/`);
      return response.data;
    } catch (error) {
      return error;
    }
  },

  async updatePost(PostSlug, updatedPostData) {
    try {
      const response = await getAPI.put(`/posts/${PostSlug}`, updatedPostData);
      return response.data;
    } catch (error) {
      throw new Error("Error updating Post: " + error.message);
    }
  },

  async deletePost(PostSlug) {
    try {
      const response = await getAPI.delete(`/posts/${PostSlug}`);
      return response.data;
    } catch (error) {
      throw new Error("Error deleting Post: " + error.message);
    }
  },
};

export default PostService;
