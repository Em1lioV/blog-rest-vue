<template>
    <div
        class="mx-auto grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 pt-10 sm:pt-16 lg:mx-0 lg:max-w-none lg:grid-cols-3">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
</template>
  
<script setup>
import PostCard from '@/components/PostCard.vue';

const props = defineProps(['posts']);
</script>
  
