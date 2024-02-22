<template>
  <div class="relative">
    <Input v-bind="$attrs" :id="props.id" v-model="searchQuery" :required="required" :invalid="invalid"
      @keyup.enter="handleSearch" :ariaDescribeBy="ariaDescribeBy" :class="'pr-[40px] peer'" placeholder="buscar" />
    <button type="button" @click="handleSearch"
      class="absolute inset-y-0 right-0 px-2 py-1.5 flex items-center focus:outline-none text-gray-300 peer-focus/:text-blumine-400">
      <MagnifyingGlassIcon class="w-6 h-6 fill-current hover:text-blumine-500" />
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import Input from './Input.vue';
import { MagnifyingGlassIcon } from '@heroicons/vue/24/solid';

const props = defineProps({
  id: String,
  required: Boolean,
  invalid: Boolean,
  ariaDescribeBy: String,
});

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
  } else { searchQuery.value = '' }
}, { deep: true });

// Función para verificar si estamos en la página de búsqueda
const isSearchPage = () => route.name === 'search';
</script>

