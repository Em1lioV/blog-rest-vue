<template>

    <div class="mx-auto max-w-7xl pb-8 px-6 lg:px-8">
      <div v-if="postsLoading" class="w-full grid place-items-center">
        <p>cargando...</p>
      </div>
      <div v-else>
          <PostList :posts="posts" />
      </div>
    </div>
 
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getAPI } from "@/services/axiosConfig";
import { PhotoIcon, UserCircleIcon } from '@heroicons/vue/24/solid'
import PostList from "@/components/PostList.vue";

const posts = ref(null);
const postsLoading = ref(true);

onMounted(async () => {
  try {
    const url = 'posts/';
    const response = await getAPI.get(url);
    posts.value = response.data;
  } catch (error) {
    console.error("Error al obtener los datos:", error);
  } finally {
    postsLoading.value = false;
  }
});
</script>
