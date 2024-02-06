<template>
  <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
    <form class="w-full  lg:max-w-screen-lg" @submit="submitForm" enctype="multipart/form-data">
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-semibold leading-7 text-gray-900">Nuevo Post</h2>

          <div class="sm:col-span-full mt-2">

            <Field id="coverImage" label="Imagen de Portada">
              <div class="w-full  border-blumine-400 rounded-md border-[1px] relative bg-cover-container aspect-[16/6] shadow-black">
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
              <div class="mt-2 min-w-full ">
                <TinyEditor v-model="post.content" />
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
import Field from '@/components/input_components/Field.vue';
import Input from '@/components/input_components/Input.vue';
import TinyEditor from '@/components/input_components/TinyEditor.vue';






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