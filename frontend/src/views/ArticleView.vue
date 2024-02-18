<template>
    <div class="mx-auto max-w-3xl pb-8 px-6 lg:px-8">
        <div v-if="post">
            <Post :post="post" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { getAPI } from '@/services/axiosConfig';
import Post from '@/components/Post.vue';
import { useRoute } from 'vue-router';
import { PostService } from '@/services';

const postId = ref(null);
const post = ref(null);
const route = useRoute()
// Obtener el ID del post de los parámetros de la ruta
const getPostIdFromRoute = () => {
    postId.value = route.params.id;
};

// Cargar los detalles del post cuando el ID cambia
watch(postId, async () => {
    if (postId.value) {
        try {
            const response = await PostService.getPostById(postId.value);
            post.value = response;
        } catch (error) {
            console.error('Error al obtener los detalles del post:', error);
        }
    }
});




onMounted(() => {
    getPostIdFromRoute();
});
</script>

