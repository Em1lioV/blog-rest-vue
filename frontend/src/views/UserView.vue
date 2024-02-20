<template>
  <div class="mx-auto max-w-7xl pb-8 mt-5 px-6 lg:px-8 flex justify-center items-center flex-col">
    <div v-if="userData" class="flex flex-row justify-start max-w-3xl w-full mt-6  mx-2 mb-2 gap-x-3 items-center">
      <div>
        <Avatar :initials="userData.initials" :name="userData.fullname" :src="userData.profile_image" size="md"/>
      </div>
      <div><h1 class="text-3xl font-bold">{{ userData.fullname }}</h1>
      <h2 class="text-xl">{{ userData.role.description }}</h2></div>
    </div>
    <hr class="w-full max-w-3xl border my-4 border-blumine-200">
    <div v-if="posts" class="w-full grid place-items-center">
      <PostCardVue v-for="post in posts" :key="post.id" :post="post" :showAuthorInfo="false" />
    </div>

  </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { userService, PostService } from '@/services';
import PostCardVue from '@/components/PostCard.vue';
import { useRoute } from 'vue-router';
import Avatar from '@/components/Avatar.vue';

const route = useRoute()

const userData = ref(null);
const posts = ref(null);

const fetchUserData = async (userId) => {
  try {
    const response = await userService.getUserById(userId);
    const responsePosts = await PostService.getPostsUserById(userId);

    console.log(response);

    userData.value = response;
    posts.value = responsePosts;

    console.log(posts.value);
  } catch (error) {
    console.error('Error al obtener datos del usuario:', error);
  }
};

// Obtenemos la ID del usuario del URL cuando el componente se monta
onMounted(() => {
  const userId = route.params.id; // Suponiendo que la ruta tenga un parámetro llamado 'id'
  fetchUserData(userId);
});
</script>
