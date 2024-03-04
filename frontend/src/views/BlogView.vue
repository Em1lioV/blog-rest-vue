<template>
  <div class="py-24 sm:py-25">
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <div v-if="postsLoading" class="w-full grid place-items-center">
        <p>cargando...</p>
      </div>
      <div v-else>
          <PostList :posts="posts" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { axios } from '@/services';
import { PhotoIcon, UserCircleIcon } from '@heroicons/vue/24/solid'
import { PostList } from "@/components/post_components";

const posts = ref(null);
const postsLoading = ref(true);

onMounted(async () => {
  try {
    const url = 'posts/';
    const response = await axios.get(url);
    posts.value = response.data;
  } catch (error) {
    console.error("Error al obtener los datos:", error);
  } finally {
    postsLoading.value = false;
  }
});
</script>
