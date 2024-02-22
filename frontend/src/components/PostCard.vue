<template>
  <article
    :class="['max-w-3xl w-full flex flex-row items-start justify-between border border-gray-200 rounded-lg shadow overflow-hidden', post.author ? ' h-[200px] sm:h-[225px] md:h-[250px]' : ' h-[125px] sm:h-[150px] md:h-[175px]']">
    <div class="w-full h-full p-4 flex flex-col justify-between">
      <div class="flex items-center text-xs mb-3" v-if="post.author">
        <router-link :to="'/profile/' + post.author.id" class="none">
          <div class="text-start relative flex items-center gap-x-2">
            <Avatar responsive :src="post.author.profile_image" :name="post.author.fullname" :initials="post.author.initials" />
            <div class="text-sm leading-1">
              <h2 class="font-semibold text-gray-900">{{ post.author.fullname }}</h2>
              <h3 class="text-gray-600 hidden sm:inline-block p-0 m-0" v-if="post.author.role">
                {{ post.author.role.description }}
              </h3>
            </div>
          </div>
        </router-link>
      </div>
      <div class="group relative flex flex-col h-full">
        <router-link :to="'/posts/' + post.slug + '-' + post.id">
          <h2
            class="mt-1 text-base md:text-lg text-start font-semibold leading-5 text-gray-900 group-hover:text-gray-600 !line-clamp-3  sm:!line-clamp-2">
            {{ post.title }}
          </h2>
          <p :class="PostPreviewClasses" v-html="PostPreview">
          </p>
        </router-link>
      </div>
      <div >
        <div v-if="post.category">
          <router-link :to="'/tag/' + post.category"
            class="relative z-10 rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 hover:bg-gray-100">
            {{ post.category }}
          </router-link>
        </div>
        <time :datetime="post.published" class="text-gray-600 text-sm md:text-base">
          {{ formattedDate }}
        </time>
      </div>
    </div>
    <div v-if="post.thumbnail" class="w-[50%]  h-full">
      <router-link :to="'/posts/' + post.slug + '-' + post.id" class="w-full h-full object-cover ">
        <img :src="post.thumbnail" alt="" loading="lazy" class=" w-full h-full object-cover" />
      </router-link>

    </div>
  </article>
</template>


<script setup>
import { computed } from 'vue';
import Avatar from './Avatar.vue';
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

const PostPreviewClasses = computed(() => {
  return {
    'hidden sm:block mt-1 text-sm md:text-base leading-1 text-gray-600': true,
    'sm:!line-clamp-2': props.post.title.length > 45,
    'sm:!line-clamp-3': props.post.title.length <= 45,
  };
});
</script>
