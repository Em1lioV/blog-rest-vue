<template>
  <div v-if="!isAuthenticated" class="bg-blumine-100 flex justify-between items-center  min-h-[380px]">
    <div class="flex justify-center flex-col  items-start p-5 sm:p-10 md:py-16 md:pl-20 lg:py-20 lg:pl-28 xl:pl-48">
      <h1 class="text-4xl md:text-6xl font-bold mb-4 text-balance font-LeagueSpartan">Siempre en busca de más.</h1>
      <p class="text-lg md:text-xl mb-8 max-w-2xl text-balance">Explora junto a escritores y lectores una amplia gama de
        temas y experiencias.</p>
      <div class="flex space-x-4">
        <Button size="lg">comenzar a leer</Button>
      </div>

    </div>
    <div>

      <TagsLayout />
    </div>

  </div>
  <div>
    <div class="mx-auto max-w-3xl mt-6 pb-8 px-6 lg:px-8">
      <template v-if="isAuthenticated">
        <RouterTabs :tabs="routerTabs" />
      </template>
      <div class="flex gap-y-4 flex-col mt-5" v-if="posts">
        <PostCard v-for=" post   in    posts   " :key="post.id" :post="post" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue"; // Importa computed
import { PostService, tagService } from "@/services";
import { RouterTabs } from "@/components";
import { PlusIcon } from "@heroicons/vue/24/solid";
import { useRoute } from "vue-router";
import { PostCard } from "@/components/post_components";
import store from "@/store";
import { Button } from "@/components/input_components";
import TagsLayout from "@/components/TagsLayout.vue";

const route = useRoute();
const posts = ref(null);
const tags = ref([]);
const postsLoading = ref(true);
const isAuthenticated = ref(false);

const checkAuthentication = () => {
  if (store.state.access_token) {
    fetchUserTagsData();
    isAuthenticated.value = true;
  }
};

const tabs = [
  {
    to: { name: "my-suggestions", hash: "#suggested-topics" },
    Icon: PlusIcon,
    iconTitle: "explorar etiquetas",
    tabIndex: "0",
    noClickOnKeyNavigation: true,
  },
  { to: "/", title: "Para Ti" },
  { to: "/?feed=follow", title: "Seguidos" },
];

const routerTabs = computed(() => {
  let combinedTabs = [];

  if (tags.value) {
    combinedTabs = tags.value.map((tag) => ({
      to: "/?tag=" + tag.slug,
      title: tag.name,
    }));
  }

  if (tabs) {
    combinedTabs = [...tabs, ...combinedTabs];
  }

  return combinedTabs;
});

onMounted(async () => {
  checkAuthentication();
});

const fetchUserTagsData = async () => {
  try {
    postsLoading.value = true;
    const response = await tagService.getFollowingTags();

    tags.value = response;
  } catch (error) {
    console.error("Error al obtener datos: ", error);
  } finally {
    postsLoading.value = false;
  }
};

watch(
  () => route.query,
  async (newQuery, oldQuery) => {
    let queryString = new URLSearchParams(route.query).toString();

    if (newQuery !== oldQuery) {
      try {
        postsLoading.value = true;
        const response = await PostService.getPosts(`?${queryString}`);

        posts.value = response;
      } catch (err) {
        console.error("Error fetching post:", err);
      } finally {
        postsLoading.value = false;
      }
    }
  },
  { immediate: true }
);
</script>
