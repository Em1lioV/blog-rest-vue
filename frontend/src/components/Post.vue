<template>
    <div class="mx-auto pt-10 lg:mx-0 max-w-none">
        <article class="p-5">
        <h1 class="text-3xl md:text-4xl font-bold mb-2">{{ capitalizeFirstLetter(post.title) }}</h1>
        <div v-if="post.excerpt !== null && ''">
          <h2 class="text-lg md:text-xl font-semibold mb-4 text-gray-500">{{ capitalizeFirstLetter(post.excerpt) }}</h2>
        </div> 
        <div v-if="post.thumbnail" class="mb-4">
          <img :src="'api/'+post.thumbnail" alt="Post Thumbnail" class="w-full h-auto rounded-md">
        </div>
  
        <div class="flex items-center gap-x-4 text-xs mb-4">
            <time :datetime="post.published" class="text-gray-500">
        {{ new Date(post.published).toLocaleDateString("es-ES", { month: "short", day: "2-digit", year: "numeric" }) }}
      </time>
          <span class="rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600">{{ post.category }}</span>
        </div>
  
        <div class="text-start mb-6">
          <!-- Utiliza v-html para renderizar el contenido HTML de manera segura -->
          <div v-html="post.content"></div>
        </div>
  
        <div class="flex items-center gap-x-4">
          <img v-if="post.author_profile_image" :src="'api/media/' + post.author_profile_image" alt="Author Profile" class="h-10 w-10 rounded-full bg-gray-50" loading="lazy" />
          <div class="text-sm leading-6">
            <p class="font-semibold text-gray-900">{{ post.author_name }}</p>
            <p class="text-gray-600">{{ post.author_role_description }}</p>
          </div>
        </div>
      </article>
    </div>
  </template>
  
  <script setup>
  
  const props = defineProps(['post']);
  const capitalizeFirstLetter = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
};
</script>
  