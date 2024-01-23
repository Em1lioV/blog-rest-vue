<template>
  <article class="flex max-w-2xl flex-col items-start justify-between border border-gray-200 rounded-lg shadow">
  
    <div v-if="post.thumbnail" class="max-h-48 sm:max-h-60 lg:max-h-48 w-full object-cover rounded-t-md">
      <router-link :to="'/post/'+ post.slug " >
        <img :src="post.thumbnail" alt="" loading="lazy" class="w-full h-full object-cover rounded-t-md" />
    </router-link>
    </div>

    <div v-else class="p-5 w-full">
      <router-link :to="'/post/'+ post.slug " >
        <img src="../assets/logo.png" loading="lazy" alt="" class="max-h-48 m-auto object-fit rounded-t-md" />
      </router-link>
    </div>

    <div class="flex items-center gap-x-4 text-xs pt-3 px-3">
      <time :datetime="post.published" class="text-gray-500">
        {{ new Date(post.published).toLocaleDateString("es-ES", { month: "short", day: "2-digit", year: "numeric" }) }}
      </time>
      <a class="relative z-10 rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 hover:bg-gray-100">{{
        post.category }}</a>
    </div>

    <div class="group relative p-3">
      <router-link :to="'/post/'+ post.slug " >
        <h3 class="mt-3 text-lg text-start font-semibold leading-6 text-gray-900 group-hover:text-gray-600">{{ post.title }}</h3>
        <p class="mt-5 line-clamp-3 text-sm leading-6 text-gray-600"><span v-show="post.excerpt">{{ post.excerpt }} - </span>{{ post.content }}</p>
      </router-link>
    </div>

    <div class="text-start relative mt-8 flex items-center gap-x-4 pb-3 px-3">
      
      <Avatar :src="author_profile_image" :name="post.author_name"/>
     
      <div class="text-sm leading-6">
        <p class="font-semibold text-gray-900">{{ post.author_name }}</p>
        <p class="text-gray-600">{{ post.author_role_description }}</p>
      </div>
    </div>
  </article>
</template>

<script setup>
import { UserCircleIcon } from '@heroicons/vue/24/solid'
import { computed } from 'vue';
import Avatar from './Avatar.vue';

const props = defineProps(['post']);



const author_profile_image = computed(() => {
  return props.post.author_profile_image?  'api/media/'+ props.post.author_profile_image : props.post.author_profile_image;
});
</script>


  
