<template>
    <div class="mx-auto max-w-3xl pb-8 px-6 lg:px-8">
        <div v-if="loading">Loading...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else>
            <Post v-if="post" :post="post" />
        </div>

    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { PostService } from '@/services';
import { Post } from '@/components/post_components';
import { useRoute, useRouter } from 'vue-router';

const loading = ref(false);
const post = ref(null);
const error = ref(null);
const route = useRoute();
const router = useRouter();

watch(() => route.params, async (newParams, oldParams) => {
    const { id: newId, slug: newSlug } = newParams;
    const { id: oldId } = oldParams || {};

    if (newId !== oldId) {
        try {
            loading.value = true;
            const response = await PostService.getPostById(newId);
            const { slug: fetchedSlug } = response;
            post.value = response;
            error.value = null;

            if (fetchedSlug !== newSlug) {
                router.replace({ params: { id: newId, slug: fetchedSlug } });
            }
        } catch (err) {
            console.error('Error fetching post:', err);
            error.value = err.message || 'Failed to fetch post';
        } finally {
            loading.value = false;
        }
    } else if (oldParams && newSlug !== post.value.slug) {
        router.replace({ params: { id: newId, slug: post.value.slug } });
    }
}, { immediate: true });

</script>