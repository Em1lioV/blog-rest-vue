<template>
  <div class="mx-auto max-w-3xl mt-6 pb-8 px-6 lg:px-8 flex flex-col justify-center items-center">
    <div class="flex flex-col w-full">
      <div class="md:hidden mx-6">
        <SearchBar :searchPage="computedsearchpage" />
      </div>
      <div v-show="searchQuery" class="text-2xl md:text-4xl font-bold pt-2 md:pt-5 mx-6 md:mx-0 mt-4 md:mt-0">
        <h2 class="text-gray-600 overflow-ellipsis whitespace-nowrap overflow-hidden">
          Resultados para
          <span aria-label="none" class="text-blumine-500 ">{{ searchQuery }}</span>
        </h2>
      </div>

      <div v-if="searchQuery" class="mx-6 md:mx-0 mt-4 md:mt-2">
        <RouterTabs :tabs="computedTabs" />
      </div>
      <section v-if="searchQuery" class="mx-6 md:mx-0 mt-8">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </section>

      <div v-else class="mx-6 md:mx-0 mt-8">
        <h1 class="text-4xl font-bold">Búsquedas recientes</h1>
        <p class="text-md mt-2">No tienes búsquedas recientes</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRoute } from 'vue-router';
import { SearchBar } from "@/components/input_components";
import { RouterTabs } from "@/components";
import { RouterView } from "vue-router";

const route = useRoute();
const searchQuery = ref();

const computedTabs = computed(() => {
  return [
    { to: { name: 'search-posts', query: { q: searchQuery.value } }, title: 'articulos' },
    { to: { name: 'search-users', query: { q: searchQuery.value } }, title: 'usuarios' },
    { to: { name: 'search-tags', query: { q: searchQuery.value } }, title: 'tags' }
  ];
});

const computedsearchpage = computed(() => {
  return route.name;
});

watch(() => route.query['q'], (newVal) => {
  searchQuery.value = newVal || '';
});

onMounted(() => {
  searchQuery.value = route.query['q'] || '';
});

</script>
