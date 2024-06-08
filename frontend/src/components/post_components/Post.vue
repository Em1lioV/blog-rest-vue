<template>
  <article class="p-5">
    <h1 class="text-[42px] leading-10 font-bold">{{ post.title }}</h1>
    <div v-if="post.subtitle" class="mb-6 mt-5">
      <h2 class="text-[22px] font-semibold text-gray-500">
        {{ post.subtitle }}
      </h2>
    </div>
    <div v-if="post.author" class="flex flex-row justify-start flex-wrap md:flex-nowrap w-full items-center">
      <div class="flex flex-1 gap-x-2 items-center">
        <Avatar responsive :initials="post.author.initials" :name="post.author.fullname"
          :src="post.author.profile_image" />

        <div class="flex flex-col">
          <div class="flex items-center gap-x-2">
            <p>
              <router-link :to="{ name: 'profile', params: { id: post.author.id } }" class="none">
                {{ post.author.fullname }}
              </router-link>
            </p>

            <span class="leading-6 text-[28px]">·</span>

            <p>
              {{ post.author.role.description }}
            </p>
          </div>
          <div class="flex items-center gap-x-2">

            <p>lectura de 6 min</p>
            <span class="leading-6 text-[28px]">·</span>

            <time :datetime="post.published" class="text-gray-500">
              {{
      new Date(post.published).toLocaleDateString("es-ES", {
        month: "short",
        day: "2-digit",
        year: "numeric",
      })
    }}
            </time>
          </div>
        </div>
      </div>
      <div v-if="!post.is_author"
        class="mt-4 sm:mt-0 flex-1 basis-full sm:basis-0 sm:flex-none sm:ml-auto flex items-center gap-x-2">
        <FollowButton :initial-is-following="post.author.is_following" :user-id="post.author.id" />
      </div>
    </div>

    <div class="flex justify-between items-center p-1 mt-8 mb-4 border-y-2 border-blumine-200">

      <BoostButton v-model="boost" :post-id="post.id" />

      <div class="flex gap-x-3 py-3">
        <BookmarkButton v-model="isBookmarked" :post-id="post.id" />
        <BaseTooltip content="compartir" placement="top">
          <ShareIcon class="w-6 h-6 cursor-pointer stroke-gray-600 hover:stroke-blumine-400" />
        </BaseTooltip>
        <BaseTooltip content="más" placement="top">
          <EllipsisHorizontalIcon
            class="w-6 h-6 aspect-square stroke-gray-600 hover:stroke-blumine-400 cursor-pointer" />
        </BaseTooltip>
      </div>
    </div>

    <div v-if="post.thumbnail" class="mb-4">
      <img :src="post.thumbnail" alt="Post Thumbnail" :alt="post.title" class="w-full h-auto rounded-md" />
    </div>

    <div class="prose lg:prose-lg prose-h1:text-2xl  prose-h2:text-xl">
      <div v-html="cleanContent"></div>
    </div>

    <div>
      <Button intent="secondary" ring v-for="tag in post.tags" :key="tag"
        :to="{ name: 'tag-detail', params: { slug: tag.slug } }">
        {{ tag.name }}
      </Button>
    </div>
    <div class="flex justify-between items-center p-1 mt-8 mb-4 ">


      <BoostButton v-model="boost" :post-id="post.id" />

      <div class="flex gap-x-3 py-3">
        <BookmarkButton v-model="isBookmarked" :post-id="post.id" />
        <BaseTooltip content="compartir" placement="top">
          <ShareIcon class="w-6 h-6 stroke-gray-600 cursor-pointer hover:stroke-blumine-400" />
        </BaseTooltip>
        <BaseTooltip content="más" placement="top">
          <EllipsisHorizontalIcon
            class="w-6 h-6 aspect-square stroke-gray-600 hover:stroke-blumine-400 cursor-pointer" />
        </BaseTooltip>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed, ref } from "vue";
import { Button, FollowButton, BookmarkButton, BoostButton } from "../input_components";
import { EllipsisHorizontalIcon, ShareIcon } from "@heroicons/vue/24/outline";
import { sanitize } from "dompurify";

import Avatar from "../Avatar.vue";
import { BaseTooltip } from "..";


const props = defineProps(["post"]);

const isBookmarked = ref(props.post.is_bookmarked)
const boost = ref({
  IsBoosted: props.post.is_boosted,
  boosts_count: props.post.boosts_count
})


const cleanContent = computed(() => {
  return sanitize(props.post.content);
});
</script>
