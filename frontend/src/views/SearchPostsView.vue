<template>
    <div v-if="postsLoading" class="w-full grid place-items-center">
        <p>Cargando...</p>
    </div>
    <div v-else class="w-full">
        <div v-if="posts && posts.length > 0" class="w-full">
            <PostList :posts="posts" />
        </div>
        <div v-else class="pt-10">
            <p class="text-gray-600 text-lg md:text-xl">
                No se encontraron resultados. Por favor, verifica la ortografía,
                prueba con diferentes palabras clave o utiliza palabras clave más generales.
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, onActivated, onDeactivated } from "vue";
import { PostService } from '@/services';
import { useRoute } from 'vue-router';
import { PostList } from "@/components/post_components";

const route = useRoute()
const searchQuery = ref(null)
const lastSearchQuery = ref(null); // Variable para almacenar la última consulta de búsqueda
const postsLoading = ref(false)
const posts = ref([])

const performSearch = async (query) => {
    console.log('consulta');
    try {
        postsLoading.value = true;

        if (query.trim() !== '') {
            const response = await PostService.searchPosts(query);
            posts.value = response;
        } else {
            posts.value = [];
        }
    } catch (error) {
        console.error("Error al realizar la búsqueda:", error);
    } finally {
        postsLoading.value = false;
    }
};

watch(() => route.query['q'], (newVal) => {
    // Guarda la nueva consulta de búsqueda
    searchQuery.value = newVal || '';
    if(route.name === 'search-posts'){
        if (lastSearchQuery.value !== searchQuery.value) {
        // Si la nueva consulta es diferente de la última consulta guardada, realiza la búsqueda
        performSearch(searchQuery.value);
        lastSearchQuery.value = searchQuery.value; // Actualiza la última consulta guardada
    }
    }
});

onMounted(() => {
    searchQuery.value = route.query['q'] || '';
    lastSearchQuery.value = searchQuery.value;
    performSearch(searchQuery.value);
});

onActivated(() => {
    if (searchQuery.value !== lastSearchQuery.value) {
        performSearch(searchQuery.value);
        lastSearchQuery.value = searchQuery.value;
    }
});

onDeactivated(() => {
    if(route.name === 'search-posts'){
        lastSearchQuery.value = searchQuery.value; 
    } 
});
</script>