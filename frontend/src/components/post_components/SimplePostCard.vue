<template>
  <article
    class="max-w-3xl w-full flex flex-row items-start justify-between border border-gray-200 rounded-lg shadow 
    overflow-hidden h-[125px]">
    <div class="w-full h-full p-4 flex flex-col justify-between">
      <div class="group relative flex flex-col h-full">
        <router-link :to="'/posts/' + post.slug + '-' + post.id">
          <h2
            class="mt-1 text-base md:text-lg text-start font-semibold leading-5 text-gray-900 group-hover:text-gray-600 !line-clamp-1">
            {{ post.title }}
          </h2>
          <p class="mt-1 text-sm md:text-base leading-1 text-gray-600 !line-clamp-1" v-html="PostPreview">
          </p>
        </router-link>
      </div>
      <div>
        <div v-if="post.category">
          <router-link :to="'/tag/' + post.category"
            class="relative z-10 rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 hover:bg-gray-100">
            {{ post.category }}
          </router-link>
        </div>
        <p class="text-gray-600 text-xs md:text-sm">fecha de publicacion
          <time :datetime="post.published">
            {{ formattedDate }}
          </time>
        </p>
      </div>
    </div>
  </article>
</template>
  
  
<script setup>
import { computed } from 'vue';
import DOMPurify from 'dompurify';

const props = defineProps({
  post: {
    type: Object,
  },
})

const sanitizedContent = computed(() => {
  const textContent = DOMPurify.sanitize(props.post.content, { ALLOWED_TAGS: [] });
  const trimmedText = textContent.replace(/^(?:&nbsp;|\s)+|(?:&nbsp;|\s)+$/g, '');
  return trimmedText.trim().slice(0, 300);
});

const PostPreview = computed(() => {
  return props.post.excerpt ? `${props.post.excerpt} - ${sanitizedContent.value}` : sanitizedContent.value;
});
const formattedDate = computed(() => {
  return new Date(props.post.published).toLocaleDateString("es-ES", { month: "short", day: "2-digit", year: "numeric" });
});

</script>
  