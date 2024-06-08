<template>
  <section class="mx-auto max-w-7xl pb-8 mt-5 px-6 lg:px-8 flex justify-center items-center flex-col">
    <header v-if="TagData" class="flex flex-row justify-center max-w-3xl w-full mt-6 mx-2 mb-2 gap-x-3 items-center">
      <div class="flex flex-col justify-center w-full gap-y-2">
        <h1 class="text-3xl font-bold self-center text-slate-800">{{ TagData.name }}</h1>
        <div class="flex flex-row gap-x-2 justify-center text-slate-700">
          <h3 class="text-md">Tema</h3>
          -
          <h3 class="text-md">{{ TagData.post_count }} posts</h3>
          -
          <h3 class="text-md">{{ TagData.follower_count }} seguidores</h3>
        </div>
        <div class="flex justify-center items-center mt-1">
            <Button v-if="!TagData.is_following" @click="toggleFollow">seguir</Button>
            <Button v-if="TagData.is_following" ring @click="toggleFollow">siguiendo</Button>
        </div>
      </div>
    </header>
    <hr class="w-full max-w-3xl border my-4 border-blumine-200" />
    <div v-if="TagData && TagData.posts.length > 0" class="w-full grid gap-y-4 place-items-center">
      <PostCard v-for="post in TagData.posts" :key="post.id" :post="post" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { tagService, PostService } from "@/services";

import { PostCard } from "@/components/post_components";
import { useRoute } from "vue-router";
import { Button } from "@/components/input_components";

const route = useRoute();

const toggleFollow = async () => {
  const res = await tagService.togglefollowTag(TagData.value.slug);
  TagData.value.is_following = res.is_following;
  TagData.value.follower_count = res.follower_count;

};

const TagData = ref(null);

const fetchTagData = async (tagSlug) => {
  try {
    const response = await tagService.getTagById(tagSlug);

    TagData.value = response;

  } catch (error) {
    console.error("Error al obtener datos del usuario:", error);
  }
};

onMounted(() => {
  const tagSlug = route.params.slug;
  fetchTagData(tagSlug);
});
</script>
