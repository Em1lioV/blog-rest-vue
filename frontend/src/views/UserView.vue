<template>
  <section class="mx-auto max-w-3xl pb-8 mt-5 px-6 lg:px-8 flex justify-center items-center flex-col">
    <header v-if="userData"
      class="flex flex-row justify-start flex-wrap md:flex-nowrap max-w-3xl w-full mt-6  mx-2 mb-2 gap-x-3 items-center">
      <div class="flex flex-1 gap-x-2 items-center">

        <Avatar responsive :initials="userData.initials" :name="userData.fullname" :src="userData.profile_image"
          size="md" />

        <div>
          <h1 class="text-2xl sm:text-3xl font-bold">{{ userData.fullname }}</h1>
          <h2 class="text-xl">{{ userData.role.description }}</h2>
        </div>
      </div>
      <div class="mt-4 sm:mt-0 flex-1 basis-full sm:basis-0 sm:flex-none sm:ml-auto flex items-center gap-x-2">
        <template v-if="userData.email">
          <Button block>Edit Profile</Button>
        </template>
        <template v-else>
          <FollowButton :user-id="userData.id" :initial-is-following="userData.is_following"></FollowButton>
        </template>
      
        <div>
          <EllipsisHorizontalIcon class="cursor-pointer h-10 w-10 stroke-slate-600 hover:stroke-blumine-400" />
        </div>

      </div>

    </header>
    <hr class="w-full border my-4 border-blumine-200">
    <div class="w-full flex gap-y-4 flex-col mt-5" v-if="posts">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>

  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { userService, PostService } from '@/services';
import { Avatar } from '@/components';
import { PostCard } from '@/components/post_components';
import { useRoute } from 'vue-router';
import { Button,FollowButton } from '@/components/input_components';
import { EllipsisHorizontalIcon } from '@heroicons/vue/24/outline'

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
