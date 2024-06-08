<template>
  <div class="flex items-center gap-1 flex-wrap w-full rounded-lg border-0 p-1.5 text-gray-900 shadow-sm ring-1 ring-gray-300 ring-inset  has-[:focus]:ring-2 has-[:focus]:ring-inset has-[:focus]:ring-blumine-400 sm:text-sm sm:leading-6">
    <div v-for="(tag, index) in tagsRef" :key="tag"
      class="flex items-center pl-1 pr-3  bg-blumine-100 float-left rounded-md text-nowrap">
      <span @click="removeTag(index)" class="cursor-pointer opacity-75">
        <XMarkIcon class="h-[18px] w-[18px] hover:stroke-blumine-500" />
      </span>
      <span>

        {{ tag }}
      </span>
    </div>
    <input @keydown="addTag" @keydown.delete="removeLastTag"
      class="min-w-[100px] px-1.5 py-1.5 grow border-0 h-6 sm:text-sm sm:leading-6  text-gray-900  ring-0 ring-inset placeholder:text-gray-400 focus:ring-0 "
      type="text" placeholder="agregar tag">
  </div>
</template>

<script setup>
import { ref, computed, watch, inject } from 'vue';

import { XMarkIcon } from '@heroicons/vue/20/solid';

import { useThrottle } from '@/composables';

const emit = defineEmits(['update:modelValue']);

const props = defineProps({
  modelValue: Array,
  tags: {
    type: Array,
    default: () => ['hola', 'dos'],
  },
  loadTags: Function,
  createOption: Function,
});



const field = inject('field', props);

const tagsRef = ref([])
/* const isLoading = ref(false);
const query = ref('');

const queryOption = computed(() => {
  return query.value === '' ? null : { missing: true, label: query.value };
});

const filteredTags = computed(() => {
  const queryLowerCase = query.value.toLowerCase().trim();
  if (queryLowerCase === '') {
    return tags.value.filter(option => option.label && option.label.trim() !== '');
  } else {
    return tags.value.filter(option =>
      option.label && option.label.toLowerCase().includes(queryLowerCase)
    );
  }
}); */


const addTag = (event) => {
  const { code, target } = event;
  const trimmedValue = target.value.trim();

  if ((code === 'Comma' || code === 'Enter') && trimmedValue.length > 0) {
    event.preventDefault();
    tagsRef.value.push(trimmedValue);
    target.value = '';
  } else if (code === 'Space' && target.value.slice(-1) === ' ') {
    event.preventDefault();
    const trimmedValue = target.value.trim();
    if (trimmedValue.length > 0) {
      tagsRef.value.push(trimmedValue);
      target.value = '';
    }
  }
};

const removeTag = (index) => {
  tagsRef.value.splice(index, 1)
}

watch(tagsRef.value,
  newValue => {
    emit('update:modelValue', newValue);
  })



const removeLastTag = (event) => {
  if (event.target.value.length === 0) {
    tagsRef.value.splice(tagsRef.value.length - 1)
  }
}
/* const throttledLoadTags = useThrottle((q) => {
  props.loadTags(q, (results) => {
    tags.value = results;
    if (
      props.modelValue &&
      !tags.value.some(o => {
        return o.value === props.modelValue?.value;
      })
    ) {
      tags.value.unshift(props.modelValue);
    }
    isLoading.value = false;
  });
}, 500);


watch(
  query,
  q => {
    if (props.loadTags) {
      isLoading.value = true;
      throttledLoadTags(q);
    }
  },
  { immediate: true }
);
 
function handleUpdateModelValue(selected) {
  if (props.createOption && selected?.missing) {
    isLoading.value = true;
    props.createOption(selected, option => {
      const valueToSendOption = useModelValueValidator(option, props.modelValue);
      selectedValue.value = option;
      emit('update:modelValue', valueToSendOption);
      isLoading.value = false;
    });
  } else {
    const valueToSend = useModelValueValidator(selected, props.modelValue);
    emit('update:modelValue', valueToSend);
    selectedValue.value = selected;
  }
}

function useModelValueValidator(selected, modelValue) {

} */

</script>