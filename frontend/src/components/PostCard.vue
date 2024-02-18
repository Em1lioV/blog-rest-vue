<template>
  <article
    :class="['max-w-3xl w-full flex flex-row items-start justify-between border border-gray-200 rounded-lg shadow m-2 overflow-hidden', post.author ? ' h-[200px] sm:h-[250px] md:h-[270px]' : ' h-[140px] sm:h-[170px] md:h-[200px]']">
    <div :class="['w-[65%] h-full p-4 flex flex-col', post.author ? 'justify-between' : '']">
      <div class="flex items-center text-xs" v-if="post.author">
        <router-link :to="'/profile/' + post.author.id" class="none">
          <div class="text-start relative flex items-center gap-x-2">
            <Avatar :src="post.author.profile_image" :name="post.author.fullname" :initials="post.author.initials" />
            <div class="text-sm leading-6">
              <p class="font-semibold text-gray-900">{{ post.author.fullname }}</p>
              <p class="text-gray-600 hidden sm:inline-block" v-if="post.author.role">{{ post.author.role.description }}</p>
            </div>
          </div>
        </router-link>
      </div>
      <div class="group relative flex flex-col justify-center flex-grow"> <!-- Añade la clase flex-grow aquí -->
        <router-link :to="'/posts/' + post.slug + '-'+post.id">
          <h2 class="mt-1 text-sm sm:text-base md:text-lg text-start font-semibold leading-5 text-gray-900 group-hover:text-gray-600  !line-clamp-2">
            {{ post.title }}
          </h2>
          <p class="mt-1 text-sm leading-5 text-gray-600 hidden sm:block sm:!line-clamp-2 md:!line-clamp-3">
            <span v-if="post.excerpt">{{ post.excerpt }} - </span><span v-html="sanitizedContent"></span>
          </p>
        </router-link>
      </div>
      <div class="mt-auto">
        <div v-if="post.category">
          <router-link :to="'/tag/' + post.category" class="relative z-10 rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 hover:bg-gray-100">
            {{ post.category }}
          </router-link>
        </div>
        <time :datetime="post.published" class="text-gray-500">
          {{ new Date(post.published).toLocaleDateString("es-ES", { month: "short", day: "2-digit", year: "numeric" }) }}
        </time>
      </div>
    </div>
    <div class="w-[35%]  h-full">
      <router-link v-if="post.thumbnail" :to="'/posts/' + post.slug + '-'+post.id" class="w-full h-full object-cover ">
        <img :src="post.thumbnail" alt="" loading="lazy" class=" w-full h-full object-cover" />
      </router-link>
      <router-link v-else :to="'/posts/' + post.slug + '-'+post.id" class="p-5 grid place-items-center h-full">
        <img src="../assets/logo.png" loading="lazy" alt="" class="w-[150px] md:w-[200px] min-w-[100px]:" />
      </router-link>
    </div>
  </article>
</template>


<script setup>
import { computed, defineProps } from 'vue';
import Avatar from './Avatar.vue';
import DOMPurify from 'dompurify';

const props = defineProps({
  post: {
    type: Object,
  },
})

const sanitizedContent = computed(() => {
  const textContent = DOMPurify.sanitize(props.post.content, { ALLOWED_TAGS: [] });

  // Expresión regular para eliminar caracteres no visibles y espacios al inicio y al final del texto
  const trimmedText = textContent.replace(/^(?:&nbsp;|\s)+|(?:&nbsp;|\s)+$/g, '');

  // Limitar el texto a no más de 300 caracteres
  const truncatedText = trimmedText.slice(0, 300);

  return truncatedText;
});
</script>
