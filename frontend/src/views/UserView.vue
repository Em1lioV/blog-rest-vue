<template>
  <section class="mx-auto max-w-7xl pb-8 mt-5 px-6 lg:px-8 flex justify-center items-center flex-col">
    <header v-if="userData" class="flex flex-row justify-start max-w-3xl w-full mt-6  mx-2 mb-2 gap-x-3 items-center">
      <div>
        <Avatar responsive :initials="userData.initials" :name="userData.fullname" :src="userData.profile_image" size="md"/>
      </div>
      <div><h1 class="text-3xl font-bold">{{ userData.fullname }}</h1>
      <h2 class="text-xl">{{ userData.role.description }}</h2></div>
    </header>
    <hr class="w-full max-w-3xl border my-4 border-blumine-200">
    <div v-if="posts" class="w-full grid gap-y-4 place-items-center">
      <PostCard v-for="post in posts" :key="post.id" :post="post" :showAuthorInfo="false" />
    </div>

  </section>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { userService, PostService } from '@/services';
import { PostCard,Avatar } from '@/components';
import { useRoute } from 'vue-router';

const route = useRoute()

const userData = ref(null);
const posts = ref(null);

const fetchUserData = async (userId) => {
  try {
    const response = await userService.getUserById(userId);
    const responsePosts = await PostService.getPostsUserById(userId);

    userData.value = response;
    posts.value = responsePosts;
 
  } catch (error) {
    console.error('Error al obtener datos del usuario:', error);
  }
};


onMounted(() => {
  const userId = route.params.id; 
  fetchUserData(userId);
});
</script>
