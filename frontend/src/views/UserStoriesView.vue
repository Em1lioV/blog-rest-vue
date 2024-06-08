<template>
  <section class="mx-auto max-w-5xl w-full pb-8 mt-5 px-6 lg:px-8 flex justify-center items-center flex-col">
    <Tabs>
      <Tab title="Borradores">
        <div class="w-full grid gap-y-4">
          <SimpleDraftPostCard v-for="post in filteredDraftPosts" :key="post.id" :post="post" />
        </div>
      </Tab>
      <Tab title="Publicados">
        <div class="w-full grid gap-y-4">
          <SimplePostCard v-for="post in filteredPublishedPosts" :key="post.id" :post="post"  />
        </div>
      </Tab>
    </Tabs>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import { Tabs, Tab } from '@/components';
import { SimpleDraftPostCard, SimplePostCard } from '@/components/post_components';
import { PostService } from '@/services';

const posts = ref([]);

const fetchPosts = async () => {
  try {
    posts.value = await PostService.getPostsUserByRequest();
  } catch (error) {
    console.error('Error al obtener los posts:', error);
  }
};

fetchPosts();

const filteredDraftPosts = computed(() => {
  return posts.value.filter(post => post.status === 'draft');
});

const filteredPublishedPosts = computed(() => {
  return posts.value.filter(post => post.status === 'published');
});
</script>