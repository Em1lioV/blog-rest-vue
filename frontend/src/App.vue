<template>
  <div>
    <NavBar v-if="showNavBar" />
    <main >
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

html{
  overflow-y: scroll;
}
html, body{
  scroll-behavior: smooth;
}

</style>