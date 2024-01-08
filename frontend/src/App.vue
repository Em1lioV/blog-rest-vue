<template>
  <div>
    <NavBar v-if="showNavBar"/>
    <router-view/>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue';
import { useRoute } from 'vue-router'
import { computed } from 'vue';

const route = useRoute();
const showNavBar = computed(() => {
  // Especifica aquí las rutas en las que deseas mostrar el NavBar
  return route.path !== '/login';
});
</script>
