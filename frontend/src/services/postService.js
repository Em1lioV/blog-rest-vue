import { axios, axiosMultipart } from "@/services/axiosConfig";

const PostService = {
  async createPost(PostData) {
    return await axiosMultipart.post("posts/", PostData, { requiresAuth: true });
  },

  async getPostById(PostId) {
    try {
      const response = await axios.get(`/posts/${PostId}/`,{requiresAuth:true});
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  async getPosts(query) {
    try {
      const response = await axios.get(`/posts/${query}`,{ requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  async getPostsUserByRequest() {
    try {
      const response = await axios.get('/user/posts/', { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  async getPostsUserById(UserId) {
    try {
      const response = await axios.get(`/user/posts/${UserId}/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  async searchPosts(query) {
    try {
      const response = await axios.get(`posts/?search=${query}`);
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

  async toggleBoost(postId) {
    try {
      const response = await axios.post(`/posts/${postId}/boost/`,null, { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  async toggleBookmark(postId) {
    try {
      const response = await axios.post(`/posts/${postId}/bookmark/`,null, { requiresAuth: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
};



export default PostService;
