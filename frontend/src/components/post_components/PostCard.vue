<template>
  <article
    class="max-w-3xl w-full flex flex-row items-start justify-between border border-gray-200 rounded-lg shadow overflow-hidden h-[200px] sm:h-[225px] md:h-[250px]">
    <div class="w-full h-full p-4 flex flex-col justify-between ">
      <div class="flex items-center text-xs mb-3 gap-x-2 md:gap-x-4">
        <router-link v-if="post.author" :to="{ name: 'profile', params: { id: post.author.id } }" class="none">
          <div class="text-start relative flex items-center gap-x-2">
            <Avatar responsive :src="post.author.profile_image" :name="post.author.fullname"
              :initials="post.author.initials" />
            <div class="text-sm leading-1">
              <h2 class="font-semibold text-gray-900">
                {{ post.author.fullname }}
              </h2>
              <h3 class="text-gray-600 hidden sm:inline-block p-0 m-0" v-if="post.author.role">
                {{ post.author.role.description }}
              </h3>
            </div>
          </div>
        </router-link>
        <span v-if="post.author" class="text-3xl">·</span>
        <time :datetime="post.published" class="text-gray-600 text-sm md:text-base flex items-center">
          {{ formattedDate }}
        </time>
      </div>

      <div class="flex flex-nowrap justify-between w-full max-w-full grow">
        <router-link class="break-words max-w-[calc(100%-90px)]"
          :to="{ name: 'article', params: { id: post.id, slug: post.slug } }">
          <h2
            class="mt-1 text-ellipsis overflow-hidden break-words text-base md:text-lg text-start font-semibold leading-5 text-gray-900 group-hover:text-gray-600 !line-clamp-3 sm:!line-clamp-2">
            {{ post.title }}
          </h2>
          <p :class="PostPreviewClasses">
            {{ PostPreview }}
          </p>
        </router-link>
        <div v-if="post.thumbnail" class="w-auto self-start h-[64px] sm:h-[85px] block md:hidden aspect-[10/7]">
          <router-link :to="{ name: 'article', params: { id: post.id, slug: post.slug } }"
            class="w-full h-full object-cover">
            <img :src="post.thumbnail" :alt="post.title" loading="lazy" class="w-full h-full object-cover rounded-md" />
          </router-link>
        </div>
      </div>


      <div class="flex items-center  flex-nowrap  w-full max-w-full ">
        <div class="flex gap-x-1 items-center w-full max-w-[35%] sm:max-w-[50%] lg:max-w-[75%]">
          <div v-if="post.popular_tag" class="max-w-full">
            <Button class="max-w-full" span-class="text-nowrap text-xs sm:text-sm text-ellipsis overflow-hidden" ring
              :to="{ name: 'tag-detail', params: { slug: post.popular_tag.slug } }" size="sm" intent="secondary">
              {{ post.popular_tag.name }}
            </Button>
          </div>
          <p class="text-nowrap flex-shrink-0">6 min</p>
        </div>
        <div class="ml-auto flex gap-x-1 sm:gap-x-2 items-center">
          
          <BookmarkButton :initial-is-bookmarked="post.is_bookmarked" :post-id="post.id" />
          <BaseTooltip content="más">
            <EllipsisHorizontalIcon class="w-6 h-6 aspect-square  hover:stroke-blumine-500 cursor-pointer" />
          </BaseTooltip>
        </div>
      </div>
    </div>
    <div v-if="post.thumbnail" class="w-[50%] h-full hidden md:block">
      <router-link :to="{ name: 'article', params: { id: post.id, slug: post.slug } }"
        class="w-full h-full object-cover">
        <img :src="post.thumbnail" :alt="post.title" loading="lazy" class="w-full h-full object-cover" />
      </router-link>
    </div>
  </article>
</template>

<script setup>
import { computed } from "vue";
import { Avatar, BaseTooltip } from "../";
import { BookmarkButton, Button } from "../input_components";
import { BookmarkIcon, EllipsisHorizontalIcon } from '@heroicons/vue/24/outline'


const props = defineProps({
  post: {
    type: Object,
  },
});

console.log(props.post);
const PostPreview = computed(() => {
  return props.post.subtitle
    ? `${props.post.subtitle} - ${props.post.excerpt}`
    : props.post.excerpt;
});
const formattedDate = computed(() => {
  return new Date(props.post.published).toLocaleDateString("es-ES", {
    month: "short",
    day: "2-digit",
    year: "numeric",
  });
});

const PostPreviewClasses = computed(() => {
  return {
    "hidden sm:block mt-1 text-sm md:text-base leading-1 text-gray-600": true,
    "sm:!line-clamp-2": props.post.title.length > 45,
    "sm:!line-clamp-3": props.post.title.length <= 45,
  };
});
</script>
