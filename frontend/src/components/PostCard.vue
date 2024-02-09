<template>
  <article
    class="max-w-3xl w-full h-[200px] sm:h-[250px]  flex flex-row items-start justify-between border border-gray-200 rounded-lg shadow m-2">
    <div class="w-[65%] h-full p-4 flex flex-col justify-between">
      <div class="flex items-center text-xs">
        <div class="text-start relative flex items-center gap-x-2">
          <Avatar :src="author_profile_image" :name="post.author_name" />
          <div class="text-sm leading-6">
            <p class="font-semibold text-gray-900">{{ post.author_name }}</p>
            <p class="text-gray-600 hidden sm:inline-block">{{ post.author_role_description }}</p>
          </div>
        </div>
      </div>
      <div class="group relative py-3">
        <router-link :to="'/post/' + post.slug">
          <h2
            class="mt-1 text-sm sm:text-base md:text-lg lg:text-xl text-start font-semibold leading-6 text-gray-900 group-hover:text-gray-600 line-clamp-2">
            {{ post.title }}</h2>
          <p class="mt-3 text-sm leading-6 text-gray-600 hidden sm:block sm:!line-clamp-3"><span v-if="post.excerpt">
              {{ post.excerpt }} - </span>{{ post.content }}
          </p>
        </router-link>
      </div>
      <div>
        <div v-if="post.category">
          <router-link :to="'/tag/' + post.category"
            class="relative z-10 rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 hover:bg-gray-100">>
            {{ post.category }}
          </router-link>
        </div>

        <time :datetime="post.published" class="text-gray-500">
          {{ new Date(post.published).toLocaleDateString("es-ES", {
            month: "short", day: "2-digit", year: "numeric"
          })
          }}
        </time>
      </div>
    </div>
    <div class="w-[35%]  h-full">

      <router-link v-if="post.thumbnail" :to="'/post/' + post.slug" class="w-full h-full object-cover ">
        <img :src="post.thumbnail" alt="" loading="lazy" class=" w-full h-full object-cover" />
      </router-link>

      <router-link v-else :to="'/post/' + post.slug" class="p-5 grid place-items-center h-full">
        <img src="../assets/logo.png" loading="lazy" alt="" class="w-[150px] md:w-[200px] min-w-[100px]:" />
      </router-link>

    </div>
  </article>
</template>

<script setup>
import { UserCircleIcon } from '@heroicons/vue/24/solid'
import { computed } from 'vue';
import Avatar from './Avatar.vue';

const props = defineProps(['post']);



const author_profile_image = computed(() => {
  return props.post.author_profile_image ? 'api/media/' + props.post.author_profile_image : props.post.author_profile_image;
});
</script>


  
