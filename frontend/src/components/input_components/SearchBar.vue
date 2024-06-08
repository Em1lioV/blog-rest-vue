<template>
  <div :class="['relative', props.block ? 'w-full' :'']">
    <Input  :class="['pr-[40px] peer',baseInputClass]" :id="props.id" v-model="searchQuery" :required="required" :invalid="invalid"
      @keyup.enter="handleEnterKey" :ariaDescribeBy="ariaDescribeBy"
      :placeholder="placeholder" />
    <button type="button" @click="handleSearch"
      class="absolute inset-y-0 right-0 px-2 py-1.5 flex items-center focus:outline-none text-gray-300 peer-focus/:text-blumine-400">
      <MagnifyingGlassIcon :class="['fill-current hover:text-blumine-500',iconClass]" />
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import Input from './Input.vue';
import { MagnifyingGlassIcon } from '@heroicons/vue/24/solid';
import { cva } from 'class-variance-authority';

const props = defineProps({
  id: String,
  required: Boolean,
  invalid: Boolean,
  block: Boolean,
  disable: Boolean,
  ariaDescribeBy: String,
  searchPage: {
    type: String,
    default: 'search-posts'
  },
  size: {
    type: String,
    validator: val => ["xm", "sm", "md", "lg", "xl"].includes(val),
    default: "md",
  },
  parentSearchPage: String,
  placeholder: {
    type: String,
    default: 'Buscar'
  }
});

const router = useRouter();
const route = useRoute();
const searchQuery = ref('');

const handleSearch = () => {
  const trimmedQuery = searchQuery.value.trim();

  if (trimmedQuery !== '' && trimmedQuery !== route.query.q) {
    router.push({ name: props.searchPage, query: { q: trimmedQuery } });
  }
};

const handleEnterKey = () => {

  handleSearch();

};

function isSearchPage() {
  if (props.parentSearchPage) {
    const parentroute = route.matched[route.matched.length - 2];
    return parentroute && parentroute.name === props.parentSearchPage;
  }
  return route.name == props.searchPage

}

onMounted(() => {
  if (isSearchPage()) {
    searchQuery.value = route.query.q || '';
  }
});

const baseInputClass = cva(
  '',
  {
    variants: {
      size: {
        xm: '!text-xs  min-h-[20px] ',
        sm: '!text-sm  min-h-[28px] ',
        md: '!text-md  min-h-[36px] ',
        lg: '!text-lg  min-h-[44px] ',
        xl: '!text-xl  min-h-[52px] ',
      }
    }
  }
)({  size: props.size });

const iconClass = cva(
  '',
  {
    variants: {
      size: {
        xm: 'w-4 h-4  ',
        sm: 'w-5 h-5 ',
        md: 'w-6 h-6  ',
        lg: 'w-7 h-7 ',
        xl: 'w-8 h-8 ',
      }
    }
  }
)({  size: props.size });



watch(route, () => {
  if (isSearchPage()) {
    searchQuery.value = route.query.q || '';
  } else {
    searchQuery.value = '';
  }
}, { deep: true });

</script>