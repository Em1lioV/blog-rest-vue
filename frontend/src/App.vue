<template>
  <div>
    <NavBar v-if="showNavBar" class="top-level-container"/>
    <main class="top-level-container">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue';
import { useRoute } from 'vue-router'
import { computed } from 'vue';

const route = useRoute();
const showNavBar = computed(() => {

  return route.path !== '/login';
});
</script>
<style>
@media (min-width: 1024px ) {
  .top-level-container {
    padding-left: calc(100vw - 100%);
  }
}

html {
  scroll-behavior: smooth;
}
html:focus-within {
  scroll-behavior: smooth;
}
</style>