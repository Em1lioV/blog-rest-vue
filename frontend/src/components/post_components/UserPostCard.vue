<template>
    <article
        class="max-w-3xl w-full flex flex-row items-start justify-between border border-gray-200 rounded-lg shadow overflow-hidden h-[200px]">
        <div class="w-full h-full p-5 flex flex-col justify-between">
            <div class="group relative flex flex-col h-full">
                <router-link :to="'/posts/' + post.slug + '-' + post.id">
                    <h2
                        class="mt-1 text-base md:text-lg text-start font-semibold leading-5 text-gray-900 group-hover:text-gray-600 !line-clamp-3 sm:!line-clamp-2">
                        {{ post.title }}
                    </h2>
                    <p :class="PostPreviewClasses">{{ PostPreview }}</p>
                </router-link>
            </div>
            <div class="flex gap-x-2">
                <div v-if="post.popular_tag">
                    <Button ring :to="{name: 'tag-detail',params: { slug: post.popular_tag.slug }}" size="sm" intent="secondary">{{ post.popular_tag.name }}</Button>
                </div>
                <time :datetime="post.published" class="text-gray-600 text-sm md:text-base flex items-center">
                    {{ formattedDate }}
                </time>
            </div>
        </div>
        <div v-if="post.thumbnail" class="w-[50%] h-full">
            <router-link :to="{ name: 'article', params: { id: post.id, slug: post.slug } }"
                class="w-full h-full object-cover">
                <img :src="post.thumbnail" :alt="post.title" loading="lazy" class="w-full h-full object-cover" />
            </router-link>
        </div>
    </article>
</template>

<script setup>
import { computed } from "vue";

import { Button } from "../input_components";

const props = defineProps({
    post: {
        type: Object,
    },
});

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
