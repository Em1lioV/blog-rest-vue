<template>
    <div class="hidden lg:flex flex-wrap gap-y-1 justify-end max-w-xl xl:max-w-2xl mr-4 ">
        <Button  intent="primary" ring size="sm" v-for="tag in tags" :key="tag.slug" 
            :to="{name:'tag-detail',params:{slug:tag.slug}}" :class="tag.class"
        >
            {{ tag.title }}
        </Button>
    </div> 
    
</template>

<script setup>
import { Button } from './input_components';

const tags = [
    { title: "Tecnología", slug: "tecnologia" },
    { title: "Ciencia", slug: "ciencia" },
    { title: "Arte", slug: "arte" },
    { title: "Literatura", slug: "literatura" },
    { title: "Viajes", slug: "viajes" },
    { title: "Historia", slug: "historia" },
    { title: "Cultura", slug: "cultura" },
    { title: "Música", slug: "musica" },
    { title: "Cine", slug: "cine" },
    { title: "Fotografía", slug: "fotografia" },
    { title: "Moda", slug: "moda" },
    { title: "Cocina", slug: "cocina" },
    { title: "Salud", slug: "salud" },
    { title: "Fitness", slug: "fitness" },
    { title: "Deportes", slug: "deportes" },
    { title: "Finanzas", slug: "finanzas" },
    { title: "Negocios", slug: "negocios" },
    { title: "Marketing", slug: "marketing" },
    { title: "Educación", slug: "educacion" },
    { title: "Psicología", slug: "psicologia" },
    { title: "Espiritualidad", slug: "espiritualidad" },
    { title: "Filosofía", slug: "filosofia" },
    { title: "Medio Ambiente", slug: "medio-ambiente" },
    { title: "Política", slug: "politica" },
    { title: "Derechos Humanos", slug: "derechos-humanos" },
    { title: "Justicia Social", slug: "justicia-social" },
    { title: "Viajes Espaciales", slug: "viajes-espaciales" },
    { title: "Astronomía", slug: "astronomia" },
    { title: "Ecología", slug: "ecologia" },
    { title: "Tecnología Blockchain", slug: "tecnologia-blockchain" }
];


</script>

