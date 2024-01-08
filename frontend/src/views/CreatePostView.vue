<template>
  <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
    <form class="w-full  lg:max-w-screen-lg" @submit="submitForm" enctype="multipart/form-data">
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-semibold leading-7 text-gray-900">Nuevo Post</h2>
          <label for="coverImage" class="block text-sm font-medium leading-6 text-gray-900">
            Imagen de Portada
          </label>
          <div
            class="w-full  border-blumine-400 rounded-md border-[1px] relative bg-cover-container aspect-[16/6] shadow-black">
            <img v-if="coverImageUrl" class="w-full h-full object-cover" :src="coverImageUrl" alt="" />
            <div v-else class="w-full h-full justify-center flex items-center aspect-[16/6]">
              <img src="../assets/logo.png" alt="" class="bg-cover w-[25%] min-w-[100px] " />
            </div>

            <div class="absolute inset-0 flex flex-col items-end justify-end p-4">
              <div class="mt-auto">

                <input type="file" accept="image/*" ref="coverImageInput" style="display: none"
                  @change="handleCoverImageChange" />
                <button type="button" @click="openCoverImageInput"
                  class="rounded-md bg-white mr-1 px-2.5 py-1.5 text-xs sm:text-sm font-semibold text-gray-900  ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                  Cambiar
                </button>
                <button type="button" @click="removeCoverImage"
                  class="rounded-md bg-white px-2.5 py-1.5 text-xs sm:text-sm font-semibold text-red-600 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                  Eliminar
                </button>
              </div>
            </div>
          </div>

          <div class="sm:grid sm:grid-cols-12 sm:gap-6 mt-2">
            <div class="sm:col-span-6">
              <label for="title" class="block text-sm font-medium leading-6 text-gray-900">Título<span
                  class="text-red-600">*</span></label>
              <div class="mt-2">
                <input v-model="post.title" @input="updateSlug" type="text" name="title" id="title"
                  autocomplete="given-name"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6"
                  required pattern="^[A-Za-z0-9\s!@#$%^&*()_+{}|{1,100}$" title="Ingrese un título válido"/>
              </div>
            </div>

            <div class="sm:col-span-6">
              <label for="slug" class="block text-sm font-medium leading-6 text-gray-900">Slug</label>
              <div class="mt-2">
                <input v-model="post.slug" type="text" id="slug" :readonly="true" :disabled="true"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6" />
              </div>
            </div>
          </div>

          <div class="sm:col-span-full mt-2">
            <label for="excerpt" class="block text-sm font-medium leading-6 text-gray-900">Resumen</label>
            <div class="mt-2">
              <input v-model="post.excerpt" type="text" name="excerpt" id="excerpt" autocomplete="given-name"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6"
                required pattern="[A-Za-z ]{1,32}" />
            </div>
          </div>

          <div class="sm:col-span-full w-full mt-2">
            <label for="content" class="block text-sm font-medium leading-6 text-gray-900">Contenido<span
                class="text-red-600">*</span></label>
            <div class="mt-2 min-w-full ">
              <editor :api-key="apiKey" v-model="post.content" :init="editorOptions"></editor>
            </div>
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
import axios from 'axios';
import { useRouter } from 'vue-router';
import Editor from '@tinymce/tinymce-vue';
import { postData } from '../util/apiUtils';

const apiKey = process.env.VUE_APP_TINYMCEAPIKEY;


const editorOptions = {
  selector: 'textarea#post-content',
  plugins: 'print preview quickbars anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount save',
  toolbar: 'undo redo | searchreplace |bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange  formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment',
  width: "100%",
  language: 'es',
  height: 500,
  quickbars_insert_toolbar: false,
  menubar: 'file edit view insert format tools table tc help',
  quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote image quicktable',
  toolbar_mode: 'sliding',
  content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }',
  setup: function (editor) {
    editor.on('SaveContent', function () {
      submitDraft();
      console.log('draft');
    });
  },
}

const route = useRouter();
const post = ref({
  title: '',
  excerpt: '',
  content: '',
  slug: '',
  thumbnail: null,
});

const coverImageUrl = ref(null);
const coverImageInput = ref(null);

const openCoverImageInput = () => {
  if (coverImageInput.value) {
    coverImageInput.value.click();
  }
};

const handleCoverImageChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    coverImageUrl.value = URL.createObjectURL(file);
    post.value.thumbnail = file;
  }
};

const removeCoverImage = () => {
  if (coverImageInput.value && coverImageUrl.value) {
    coverImageUrl.value = null;
    post.value.thumbnail = null;
    coverImageInput.value.value = null;
  }
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

    const response = await postData("post/create/", formData, true);

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


const updateSlug = () => {
  post.value.slug = slugify(post.value.title);
};

// Función para convertir el título en un 'slug'
const slugify = (text) => {
  return text.toString().toLowerCase()
    .replace(/\s+/g, '-')           // Reemplaza los espacios con guiones
    .replace(/[^\w\-]+/g, '')       // Elimina caracteres no alfanuméricos excepto guiones
    .replace(/\-\-+/g, '-')         // Reemplaza múltiples guiones por uno solo
    .replace(/^-+/, '')             // Elimina guiones al principio del texto
    .replace(/-+$/, '');            // Elimina guiones al final del texto
};
</script>

<style>
/* Agrega estilos si es necesario */
</style>