<template>
  <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
    <form class="w-full  lg:max-w-screen-lg" @submit="submitForm" enctype="multipart/form-data">
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-semibold leading-7 text-gray-900">Nuevo Post</h2>

          <div class="sm:col-span-full mt-2">
            <Field id="coverImage" label="Imagen de Portada">
              <CoverImageInput v-model="post.thumbnail" />
            </Field>
          </div>
          <div class="sm:col-span-full mt-2">
            <Field id="title" label="Titulo" required>
              <Input v-model="post.title" type="text" autocomplete="off" title="Ingrese un título válido" />
            </Field>
          </div>
          <div class="sm:col-span-full mt-2">
            <Field id="excerpt" label="Resumen">
              <Input v-model="post.excerpt" type="text" autocomplete="off" />
            </Field>
          </div>
          <div class="sm:col-span-full w-full mt-2">
            <Field id="content" label="Contenido" required>
                <div v-if="showEditorSkeleton">
                  <TinyEditorSkeleton/>
                </div>
                <div  v-show="!showEditorSkeleton">
                  <TinyEditor  v-model="post.content" @editor-loaded="handleEditorLoaded"/>
                </div>
              
            </Field>
          </div>
        </div>
      </div>

      <div class="mt-6 flex items-center justify-end gap-x-6">
        <button type="button" class="text-md font-semibold leading-6 rounded-md px-2 py-1 text-gray-900"
          @click="volver">Volver</button>

        <button type="submit" @click="submitDraft"
          class="border-2 border-blumine-400 text-blumine-400 text-md font-semibold  px-4 py-2 rounded-md shadow-sm hover:bg-blumine-400 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blumine-500">
          Guardar
        </button>

        <button type="submit" @click="submitPublished"
          class="rounded-md bg-blumine-400 px-4 py-2 text-md font-semibold text-white shadow-sm hover:bg-blumine-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blumine-500">
          Publicar
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { getAPImultipart } from '@/services/axiosConfig';
import { Field,Input,TinyEditor,CoverImageInput } from '@/components/input_components';

import TinyEditorSkeleton from '@/components/TinyEditorSkeleton.vue';




const route = useRouter();
const post = ref({
  title: '',
  excerpt: '',
  content: '',
  thumbnail: null,
});

const showEditorSkeleton = ref(true);

const handleEditorLoaded = () => {
  showEditorSkeleton.value = false;  
};



const volver = () => {
  route.go(-1);
};

const submitDraft = async (event) => {
  if (event) {
    event.preventDefault();
  }
  await submitPost('draft');
};

const submitPublished = async (event) => {
  if (event) {
    event.preventDefault();
  }
   await submitPost('published'); 

 
};


const submitPost = async (status) => {
  try {
    const formData = new FormData();
    formData.append('title', post.value.title);
    formData.append('content', post.value.content);

    if (post.value.excerpt) {
      formData.append('excerpt', post.value.excerpt);
    }

    if (post.value.thumbnail) {
      formData.append('thumbnail', post.value.thumbnail);
    }

    formData.append('status', status); // Add the status field
    const url = 'post/create/'
    const response = await getAPImultipart.post(url, formData, { requiresAuth: true })

    if (response.status === 201) {
      console.log("Publicación exitosa:", response.data);
      route.push({ name: 'post-detail', params: { slug: response.data.slug } });
    } else {
      console.error("Error en la publicación:", response.data);
      if (response.data && response.data.slug) {
        console.error('Error de slug:', response.data.slug);
      }
    }
  } catch (error) {
    if (error.response && error.response.status === 400) {
      console.error('Error de solicitud HTTP 400:', error.response.data);
    } else {
      console.error('Error al enviar el formulario:', error);
    }
  }
};


</script>

<style>
/* Agrega estilos si es necesario */
</style>