<template>
  <div v-if="loading" class="w-full grid place-items-center">
    <p>Cargando...</p>
  </div>
  <div v-else class="w-full">
    <div v-if="results && results.length > 0" class="w-full">
      <div v-for="user in results" :key="user.id" class="mt-5 border-b-[1px] border-blumine-100">
        <UserCard :user="user"/>
      </div>
    </div>
    <div v-else class="pt-10">
      <p class="text-gray-600 text-lg md:text-xl">
        No se encontraron resultados. Por favor, verifica la ortografía, prueba
        con diferentes palabras clave o utiliza palabras clave más generales.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onActivated, onDeactivated } from "vue";
import { userService } from "@/services";
import { useRoute } from "vue-router";
import UserCard from "@/components/UserCard.vue";

const { loading, results } = useWatchSearchQueryResults(
  userService.searchUsers,
  { routeName: "search-users" }
);

function useWatchSearchQueryResults(searchFunction, { routeName }) {
  const route = useRoute();
  const searchQuery = ref(null);
  const lastSearchQuery = ref(null);
  const loading = ref(false);
  const results = ref([]);

  const performSearch = async () => {
    try {
      loading.value = true;
      const response = await searchFunction(searchQuery.value);
      results.value = response;
    } catch (error) {
      console.error("Error al realizar la búsqueda:", error);
    } finally {
      loading.value = false;
    }
  };

  watch(
    () => route.query["q"],
    (newVal) => {
      searchQuery.value = newVal || "";
      if (route.name === routeName) {
        if (lastSearchQuery.value !== searchQuery.value) {
          lastSearchQuery.value = searchQuery.value;
          performSearch();
        }
      }
    }
  );

  onMounted(() => {
    searchQuery.value = route.query["q"] || "";
  });

  onActivated(() => {
    if (searchQuery.value !== lastSearchQuery.value) {
      lastSearchQuery.value = searchQuery.value;
      performSearch();
    }
  });

  onDeactivated(() => {
    if (route.name === routeName) {
      lastSearchQuery.value = searchQuery.value;
    }
  });

  return {
    loading,
    results,
  };
}
</script>
