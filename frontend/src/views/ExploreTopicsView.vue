<template>
    <div class="max-w-3xl mx-auto py-4 flex flex-grow justify-center items-center flex-col mt-10">
        <h1 class="text-3xl mb-5 font-bold">Explorar temas</h1>
        <SearchBar  block size="lg" search-page="search-tags"/>
    </div>
    <div class="grid grid-cols-1  md:grid-cols-3 xl:grid-cols-4 justify-between gap-10 p-5 md:p-12">
        <div  v-for="cat in categorias" :key="cat">
            <details class=" md:hidden">
                <summary class="flex justify-between">
                    <h2 class="text-2xl font-bold text-slate-700 justify-between flex">{{ cat.name }}</h2>
                </summary>
                <ul class="pl-10 mt-2">
                    <li  v-for="tag in cat.subcategorias">
                        <Button span-class="text-start" class="!justify-start" :to="{name:'tag-detail',params:{slug:tag.slug}}" intent="link">{{ tag.name }}</Button>
                    </li>
                </ul>
            </details>
            <h2 class="hidden md:block text-2xl font-bold text-slate-700">{{ cat.name }}</h2>
            <ul class="hidden md:block pl-10 mt-2">
                <li  v-for="tag in cat.subcategorias">
                    <Button span-class="text-start" class="!justify-start" :to="{name:'tag-detail',params:{slug:tag.slug}}" intent="link">{{ tag.name }}</Button>
                </li>
            </ul>
        </div>
    </div>
</template>


<script setup>
import { Button, SearchBar } from "@/components/input_components";
const categorias = [
    {
        name: "Fotografía y Diseño",
        subcategorias: [
            { name: "Fotografía", slug: "fotografia" },
            { name: "Diseño gráfico", slug: "diseno-grafico" },
            { name: "Diseño web", slug: "diseno-web" },
            { name: "Edición de imágenes", slug: "edicion-de-imagenes" },
            { name: "Ilustración", slug: "ilustracion" },
            { name: "Fotografía de moda", slug: "fotografia-de-moda" },
            { name: "Fotografía de paisajes", slug: "fotografia-de-paisajes" },
            { name: "Fotografía de retratos", slug: "fotografia-de-retratos" },
            { name: "Fotografía de bodas", slug: "fotografia-de-bodas" },
            { name: "Fotografía de viajes", slug: "fotografia-de-viajes" }
        ]
    },
    {
        name: "Ciencias de la Salud",
        subcategorias: [
            { name: "Medicina", slug: "medicina" },
            { name: "Nutrición", slug: "nutricion" },
            { name: "Enfermería", slug: "enfermeria" },
            { name: "Farmacología", slug: "farmacologia" },
            { name: "Terapia física", slug: "terapia-fisica" },
            { name: "Terapia ocupacional", slug: "terapia-ocupacional" },
            { name: "Odontología", slug: "odontologia" },
            { name: "Optometría", slug: "optometria" },
            { name: "Psiquiatría", slug: "psiquiatria" },
            { name: "Pediatría", slug: "pediatria" }
        ]
    },
    {
        name: "Educación y Aprendizaje",
        subcategorias: [
            { name: "Educación primaria", slug: "educacion-primaria" },
            { name: "Educación secundaria", slug: "educacion-secundaria" },
            { name: "Educación universitaria", slug: "educacion-universitaria" },
            { name: "Educación a distancia", slug: "educacion-a-distancia" },
            { name: "Educación especial", slug: "educacion-especial" },
            { name: "Pedagogía", slug: "pedagogia" },
            { name: "Didáctica", slug: "didactica" },
            { name: "Aprendizaje online", slug: "aprendizaje-online" },
            { name: "Técnicas de estudio", slug: "tecnicas-de-estudio" },
            { name: "Tutoría académica", slug: "tutoria-academica" }
        ]
    },
    {
        name: "Viajes y Aventura",
        subcategorias: [
            { name: "Viajes de aventura", slug: "viajes-de-aventura" },
            { name: "Ecoturismo", slug: "ecoturismo" },
            { name: "Turismo rural", slug: "turismo-rural" },
            { name: "Turismo de montaña", slug: "turismo-de-montana" },
            { name: "Turismo de playa", slug: "turismo-de-playa" },
            { name: "Turismo cultural", slug: "turismo-cultural" },
            { name: "Turismo gastronómico", slug: "turismo-gastronomico" },
            { name: "Turismo de lujo", slug: "turismo-de-lujo" },
            { name: "Turismo deportivo", slug: "turismo-deportivo" },
            { name: "Turismo de naturaleza", slug: "turismo-de-naturaleza" }
        ]
    },
    {
        name: "Marketing y Publicidad",
        subcategorias: [
            { name: "Marketing digital", slug: "marketing-digital" },
            { name: "Publicidad online", slug: "publicidad-online" },
            { name: "Estrategias de marketing", slug: "estrategias-de-marketing" },
            { name: "Marketing de contenidos", slug: "marketing-de-contenidos" },
            { name: "Publicidad en redes sociales", slug: "publicidad-en-redes-sociales" },
            { name: "Branding", slug: "branding" },
            { name: "Marketing de influencers", slug: "marketing-de-influencers" },
            { name: "Publicidad nativa", slug: "publicidad-nativa" },
            { name: "Marketing de afiliados", slug: "marketing-de-afiliados" },
            { name: "Marketing de guerrilla", slug: "marketing-de-guerrilla" }
        ]
    },
    {
        name: "Tecnología y Desarrollo",
        subcategorias: [
            { name: "Desarrollo web", slug: "desarrollo-web" },
            { name: "Desarrollo móvil", slug: "desarrollo-movil" },
            { name: "Desarrollo de software", slug: "desarrollo-de-software" },
            { name: "Tecnología blockchain", slug: "tecnologia-blockchain" },
            { name: "Seguridad informática", slug: "seguridad-informatica" },
            { name: "Internet de las cosas", slug: "internet-de-las-cosas" },
            { name: "Realidad aumentada", slug: "realidad-aumentada" },
            { name: "Realidad virtual", slug: "realidad-virtual" },
            { name: "Inteligencia artificial", slug: "inteligencia-artificial" },
            { name: "Ciberseguridad", slug: "ciberseguridad" }
        ]
    },
    {
        name: "Negocios y Finanzas",
        subcategorias: [
            { name: "Negocios", slug: "negocios" },
            { name: "Finanzas", slug: "finanzas" },
            { name: "Emprendimiento", slug: "emprendimiento" },
            { name: "Marketing", slug: "marketing" },
            { name: "Ventas", slug: "ventas" },
            { name: "Inversiones", slug: "inversiones" },
            { name: "Gestión del Tiempo", slug: "gestion-del-tiempo" },
            { name: "Recursos Humanos", slug: "recursos-humanos" },
            { name: "Liderazgo", slug: "liderazgo" },
            { name: "Contabilidad", slug: "contabilidad" }
        ]
    },
    {
        name: "Salud y Bienestar",
        subcategorias: [
            { name: "Salud", slug: "salud" },
            { name: "Fitness", slug: "fitness" },
            { name: "Nutrición", slug: "nutricion" },
            { name: "Medicina", slug: "medicina" },
            { name: "Bienestar", slug: "bienestar" },
            { name: "Yoga", slug: "yoga" },
            { name: "Pilates", slug: "pilates" },
            { name: "Running", slug: "running" },
            { name: "Ciclismo", slug: "ciclismo" },
            { name: "Natación", slug: "natacion" }
        ]
    },
    {
        name: "Arte y Cultura",
        slug: "arte-y-cultura",
        subcategorias: [
            { name: "Arte", slug: "arte" },
            { name: "Literatura", slug: "literatura" },
            { name: "Música", slug: "musica" },
            { name: "Cine", slug: "cine" },
            { name: "Fotografía", slug: "fotografia" },
            { name: "Diseño", slug: "diseno" },
            { name: "Pintura", slug: "pintura" },
            { name: "Escultura", slug: "escultura" },
            { name: "Arquitectura", slug: "arquitectura" },
            { name: "Danza", slug: "danza" }
        ]
    },
    {
        name: "Ciencia y Educación",
        subcategorias: [
            { name: "Ciencia", slug: "ciencia" },
            { name: "Historia", slug: "historia" },
            { name: "Astronomía", slug: "astronomia" },
            { name: "Biología", slug: "biologia" },
            { name: "Física", slug: "fisica" },
            { name: "Matemáticas", slug: "matematicas" },
            { name: "Psicología", slug: "psicologia" },
            { name: "Sociología", slug: "sociologia" },
            { name: "Educación", slug: "educacion" },
            { name: "Neurociencia", slug: "neurociencia" }
        ]
    },
    {
        name: "Turismo y Viajes",
        subcategorias: [
            { name: "Viajes", slug: "viajes" },
            { name: "Turismo Rural", slug: "turismo-rural" },
            { name: "Turismo Cultural", slug: "turismo-cultural" },
            { name: "Turismo de Aventura", slug: "turismo-de-aventura" },
            { name: "Turismo de Playa", slug: "turismo-de-playa" },
            { name: "Turismo de Montaña", slug: "turismo-de-montana" },
            { name: "Turismo Gastronómico", slug: "turismo-gastronomico" },
            { name: "Ecoturismo", slug: "ecoturismo" },
            { name: "Turismo Urbano", slug: "turismo-urbano" },
            { name: "Turismo de Naturaleza", slug: "turismo-de-naturaleza" }
        ]
    }
];

</script>
