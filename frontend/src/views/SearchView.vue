<template>
    <div class="py-8 sm:py-11">
      <div class="mx-auto max-w-2xl md:mx-0 lg:max-w-none px-6 lg:px-8">
        <div class="md:hidden">
          <SearchBar />
        </div>
      </div>
      <div class="mx-auto mt-5 md:mt-0 max-w-7xl px-6 lg:px-8">
        <div v-if="postsLoading" class="w-full grid place-items-center">
          <p>Cargando...</p>
        </div>
        <div v-else>
          <div v-show="searchQuery" class="text-2xl md:text-4xl font-bold">
            <h2 class="text-gray-600 overflow-ellipsis whitespace-nowrap overflow-hidden">
              Resultados para
              <span class="text-blumine-500 ">{{ searchQuery }}</span>
            </h2>
          </div>
          <div v-if="posts && posts.length > 0">
            <PostList :posts="posts" />
          </div>
          <div v-else class="pt-10">
            <p class="text-gray-600 text-lg md:text-xl">
              No se encontraron resultados. Por favor, verifica la ortografía,
              prueba con diferentes palabras clave o utiliza palabras clave más generales.
            </p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch, onActivated } from "vue";
  import { getAPI } from '@/services/axiosConfig';
  import { UserCircleIcon } from '@heroicons/vue/24/solid'
  import { useRoute } from 'vue-router';
  import SearchBar from "@/components/input_components/SearchBar.vue";
  import PostList from "@/components/PostList.vue";
  
  const searchQuery = ref('');
  const posts = ref(null);
  const postsLoading = ref(true);
  const route = useRoute();
  
  const performSearch = async () => {
    try {
      postsLoading.value = true;
  
      // Only perform the search if there is a valid query
      if (searchQuery.value.trim() !== '') {
        const url = `posts/?search=${searchQuery.value}`;
        const response = await getAPI.get(url);
  
        // Update the state of posts with the search results
        posts.value = response.data;
      } else {
        // If there's no valid query, reset the posts to null or an empty array
        posts.value = null;
      }
    } catch (error) {
      console.error("Error al realizar la búsqueda:", error);
      // Handle the error, for example, show an error message
    } finally {
      // Finish loading, regardless of whether there was an error or not
      postsLoading.value = false;
    }
  };
  
  // Watch for changes in the route parameters, specifically 'q'
  watch(() => route.query['q'], (newVal) => {
    // Set the searchQuery value when the 'q' parameter changes
    searchQuery.value = newVal || '';
    performSearch();
  });
  
  // Ensure the search is performed when the component is activated or reactivated
  onActivated(performSearch);
  
  // Perform search on component mount by directly fetching the query from the route
  onMounted(() => {
    searchQuery.value = route.query['q'] || '';
    performSearch();
  });
  </script>
  