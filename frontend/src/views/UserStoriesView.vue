<template>
    <section class="mx-auto max-w-7xl pb-8 mt-5 px-6 lg:px-8 flex justify-center items-center flex-col">
      <header class="flex flex-row justify-between max-w-3xl w-full mt-6  mx-2 mb-2 gap-x-3 items-center">
        <h1 class="text-3xl font-bold">Mis Publicaciones</h1>
        <Button size="md" intent="secondary" ring>Escribir una Publicación</Button>
      </header>
      <div class="w-full max-w-3xl mt-4">
        <div class="flex justify-start">
            <button @click="handleTabChange('draft')" :class="{ 'bg-blumine-500 text-white': selectedTab === 'draft', 'text-blumine-500': selectedTab !== 'draft' }" class="p-4 m-2">Borradores</button>
          <button @click="handleTabChange('published')" :class="{ 'bg-blumine-500 text-white': selectedTab === 'published', 'text-blumine-500': selectedTab !== 'published' }" class="p-4 m-2">Publicados</button>
        </div>
        <div v-if="filteredPosts.length > 0" class="w-full grid gap-y-4 place-items-center">
          <PostCard v-for="post in filteredPosts" :key="post.id" :post="post" :showAuthorInfo="false" />
        </div>
        <div v-else class="text-center mt-4 text-gray-500">
          <p v-if="selectedTab === 'draft'">No tienes nada guardado en borrador. ¡Escribe algo o lee en BlogThat!</p>
          <p v-else>No tienes ninguna publicación todavía. ¡Escribe tu primera publicación!</p>
        </div>
      </div>
    </section>  
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { PostService } from '@/services';
  import { PostCard } from '@/components';
  import { Button } from '@/components/input_components';
  
  const posts = ref(null);
  const selectedTab = ref('draft');
  
  const fetchUserData = async () => {
    try {
      const responsePosts = await PostService.getPostsUserByRequest();
      console.log(responsePosts);
      posts.value = responsePosts;
    } catch (error) {
      console.error('Error al obtener datos del usuario:', error);
    }
  };
  
  const handleTabChange = (tabName) => {
    selectedTab.value = tabName;
  };
  
  const filteredPosts = computed(() => {
    if (!posts.value) return [];
    if (selectedTab.value === 'published') {
      return posts.value.filter(post => post.status === 'published');
    } else if (selectedTab.value === 'draft') {
      return posts.value.filter(post => post.status === 'draft');
    } else {
      return posts.value;
    }
  });
  
  fetchUserData();
  
  </script>
  