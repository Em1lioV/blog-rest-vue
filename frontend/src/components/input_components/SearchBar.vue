<template>
  <div>
    <div class="relative mt-1">
      <input
        type="text"
        id="password"
        v-model="searchQuery"
        @keyup.enter="handleSearch"
        class="w-full pl-3 pr-10 py-2 border-2 border-gray-200 rounded hover:border-blumine-400 focus:outline-none focus:ring-inset focus:ring-blumine-400 focus:border-blumine-400 transition-colors"
        placeholder="Search..."
      />
      <button
        @click="handleSearch"
        class="block w-7 h-7 text-center text-xl leading-0 absolute top-2 right-2 text-gray-400 focus:outline-none hover:text-blumine-400 transition-colors"
      >
        <MagnifyingGlassIcon class="w-6 h-6" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { MagnifyingGlassIcon } from '@heroicons/vue/24/solid';

const router = useRouter();
const route = useRoute();
const searchQuery = ref('');

const handleSearch = () => {
  const trimmedQuery = searchQuery.value.trim();

  if (trimmedQuery !== '' && trimmedQuery !== route.query.q) {
    router.push({ name: 'search', query: { q: trimmedQuery } });
  }
};

// Actualizar el valor del input solo en la página de búsqueda
onMounted(() => {
  if (isSearchPage()) {
    searchQuery.value = route.query.q || '';
  }
});

// Actualizar el valor del input cuando la ruta cambia
watch(route, () => {
  if (isSearchPage()) {
    searchQuery.value = route.query.q || '';
  } else { searchQuery.value = ''}
}, { deep: true });

// Función para verificar si estamos en la página de búsqueda
const isSearchPage = () => route.name === 'search';
</script>
