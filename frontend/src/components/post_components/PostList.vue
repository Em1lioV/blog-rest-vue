<template>
    <div
        class="mx-auto grid max-w-2xl grid-cols-1 gap-y-5  lg:max-w-none place-items-center">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
</template>
  
<script setup>
import PostCard from './PostCard.vue';

const props = defineProps(['posts']);
</script>
  
