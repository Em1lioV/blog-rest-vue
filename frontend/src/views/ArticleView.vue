<template>
    <div class="mx-auto max-w-3xl pb-8 px-6 lg:px-8">
        <div v-if="post">
            <Post :post="post" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { getAPI } from '@/axiosConfig';
import Post from '@/components/Post.vue';
import { useRoute } from 'vue-router';

const postSlug = ref(null);
const post = ref(null);
const route = useRoute()
// Obtener el ID del post de los parámetros de la ruta
const getPostIdFromRoute = () => {
    postSlug.value = route.params.slug;
};

// Cargar los detalles del post cuando el ID cambia
watch(postSlug, async () => {
    if (postSlug.value) {
        try {
            const url = `post/${postSlug.value}`;
            const response = await getAPI.get(url);
            post.value = response.data;
        } catch (error) {
            console.error('Error al obtener los detalles del post:', error);
        }
    }
});

onMounted(() => {
    getPostIdFromRoute();
});
</script>