<template>
    <div v-if="Loading" class="grid place-items-center">
        <p>Cargando...</p>
    </div>
    <div v-else>
        
        <div v-if="tags && tags.length > 0" class="flex flex-wrap gap-y-2">
            <Button v-for="tag in tags" :key="tag.id" ring intent="secondary" :to="{ name: 'tag-detail', params: { slug: tag.slug } }">
                {{ tag.name }}
            </Button>
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
import { ref, onMounted, watch, onActivated,onDeactivated } from "vue";
import { tagService } from '@/services';
import { useRoute } from 'vue-router';
import { Button } from "@/components/input_components";

const route = useRoute()
const searchQuery = ref(null)
const lastSearchQuery = ref(null);
const Loading = ref(false)
const tags = ref([])

const performSearch = async () => {
    try {
        Loading.value = true;

        if (searchQuery.value.trim() !== '') {
            const response = await tagService.searchTags(searchQuery.value)

            tags.value = response;
        } else {
            posts.value = null;
        }
    } catch (error) {
        console.error("Error al realizar la búsqueda:", error);
    } finally {
        Loading.value = false;
    }
};

watch(() => route.query['q'], (newVal) => {
    searchQuery.value = newVal || '';
    if(route.name === 'search-tags'){
        if (lastSearchQuery.value !== searchQuery.value) {
        // Si la nueva consulta es diferente de la última consulta guardada, realiza la búsqueda
        lastSearchQuery.value = searchQuery.value;
        performSearch();
    }
    }
});



onMounted(() => {
    searchQuery.value = route.query['q'] || '';
});

onActivated(() => {
    if (searchQuery.value !== lastSearchQuery.value) {
        lastSearchQuery.value = searchQuery.value;
        performSearch();
    }
});

onDeactivated(() => {
    if(route.name === 'search-tags'){
        lastSearchQuery.value = searchQuery.value; 
    }
});
</script>
