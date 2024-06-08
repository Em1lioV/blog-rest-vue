<template>
  <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
    <form class="w-full lg:max-w-screen-lg" @submit="submitForm" >
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <div class="sm:col-span-full mt-2">
            <Field id="coverImage" label="Imagen de Portada">
              <CoverImageInput v-model="post.fields.thumbnail" />
            </Field>
          </div>
          <div class="sm:col-span-full mt-2">
            <Field id="title" label="Titulo" required :error="post.error?.validation?.title">
              <Input v-model="post.fields.title" type="text" autocomplete="off" title="Titulo del articulo" />
            </Field>
          </div>
          <div class="sm:col-span-full mt-2">
            <Field id="subtitle" label="Subtítulo">
              <Input v-model="post.fields.subtitle" type="text" autocomplete="off" title="Subtítulo del articulo" />
            </Field>
          </div>
          <div class="sm:col-span-full mt-2">
            <Field id="tags" label="etiquetas">
              <ComboboxMultiple v-model="post.fields.tags" />
            </Field>
          </div>
          <div class="sm:col-span-full w-full mt-2">
            <Field id="content" label="Contenido" required :error="post.error?.validation?.content">
              <div v-if="showEditorSkeleton">
                <TinyEditorSkeleton />
              </div>
              <div v-show="!showEditorSkeleton">
                <TinyEditor v-model="post.fields.content" @editor-loaded="handleEditorLoaded" />
              </div>

            </Field>
          </div>
        </div>
      </div>

      <div class="mt-6 flex items-center flex-wrap sm:flex-nowrap justify-end gap-x-2 gap-y-2">
        <div class="basis-full sm:basis-0 order-3 sm:order-1">

          <Button block @click="volver" intent="ghost">Volver</Button>
        </div>
        <Button class="w-full sm:w-auto order-2 sm:order-1" type="submit" @click="submitDraft" ring>
          Guardar como borrador
        </Button>
        <Button class="w-full sm:w-auto order-1 sm:order-2" type="submit" @click="submitPublished">
          Publicar
        </Button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { Field, Input, TinyEditor, CoverImageInput, Button, ComboboxMultiple } from '@/components/input_components';
import PostService from '@/services/postService';
import { useForm } from '@/composables';
import TinyEditorSkeleton from '@/components/TinyEditorSkeleton.vue';
import DOMPurify from 'dompurify';
import { tagService } from '@/services';


const route = useRouter();
const post = useForm({
  title: '',
  subtitle: '',
  tags: [],
  content: '',
  status: '',
  excerpt: computed(() => {
    const sanitizedContent = DOMPurify.sanitize(post.fields.content, { ALLOWED_TAGS: [] });
    const contentWithoutEntities = sanitizedContent
      .trim()
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&gt;/g, '>')
      .replace(/&lt;/g, '<')
      .replace(/\s+/g, ' ');
    return contentWithoutEntities.slice(0, 200);
  }),
  thumbnail: null,
});

const showEditorSkeleton = ref(true);

const handleEditorLoaded = () => {
  showEditorSkeleton.value = false;
};


/* async function loadTags(query, setOptions) {
  try {
    const response = await tagService.searchTags(query);
    const results = response;
    const options = results.map(tag => ({
      value: tag.slug,
      label: tag.name
    }));
    setOptions(options);
  } catch (error) {

  }
} */


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

    await route.push({ name: 'article', params: { slug: slug, id: id } }); 
  });
}


</script>
