<template>
  <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
    <form class="w-full  lg:max-w-screen-lg" @submit="submitForm" enctype="multipart/form-data">
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-semibold leading-7 text-gray-900">Nuevo Post</h2>

          <div class="sm:col-span-full mt-2">
            <Field id="coverImage" label="Imagen de Portada">
              <CoverImageInput v-model="post.fields.thumbnail" />
            </Field>
          </div>
          <div class="sm:col-span-full mt-2">
            <Field id="title" label="Titulo" required>
              <Input v-model="post.fields.title" type="text" autocomplete="off" title="Ingrese un título válido" />
            </Field>
          </div>
          <div class="sm:col-span-full mt-2">
            <Field id="excerpt" label="Resumen">
              <Input v-model="post.fields.excerpt" type="text" autocomplete="off" />
            </Field>
          </div>
          <div class="sm:col-span-full w-full mt-2">
            <Field id="content" label="Contenido" required>
                <div v-if="showEditorSkeleton">
                  <TinyEditorSkeleton/>
                </div>
                <div  v-show="!showEditorSkeleton">
                  <TinyEditor  v-model="post.fields.content" @editor-loaded="handleEditorLoaded"/>
                </div>
              
            </Field>
          </div>
        </div>
      </div>

      <div class="mt-6 flex items-center justify-end gap-x-2">
        <Button @click="volver" intent="ghost">Volver</Button>
        <Button type="submit" @click="submitDraft" ring>
          Guardar como borrador
        </Button>
        <Button type="submit" @click="submitPublished">
          Publicar
        </Button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Field,Input,TinyEditor,CoverImageInput,Button } from '@/components/input_components';
import PostService from '@/services/postService';
import { useForm } from '@/composables';
import TinyEditorSkeleton from '@/components/TinyEditorSkeleton.vue';


const route = useRouter();
const post = useForm({
  title: '',
  excerpt: '',
  content: '',
  status:'',
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


async function submitPost(status) {
  post.fields.status = status
  await post.submit(async fields => {
    const response = await PostService.createPost(fields);
    const slug = response.data.slug;
    const id = response.data.id;
    
    await route.push({ name: 'article', params: { slug: slug,id: id}});
  });
}


</script>

<style>
/* Agrega estilos si es necesario */
</style>