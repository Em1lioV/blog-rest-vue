<template>
  <Combobox by="value" :model-value="selectedValue" @update:model-value="handleUpdateModelValue">
    <div class="relative mt-1 z-5">
      <ComboboxInput :required="field.required"
        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6"
        :displayValue="(option) => option.label" @change="query = $event.target.value" />
      <ComboboxButton class="absolute inset-y-0 right-0 flex items-center pr-2">
        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
      </ComboboxButton>

      <TransitionRoot leave="transition ease-in duration-100" leaveFrom="opacity-100" leaveTo="opacity-0"
        @after-leave="query = ''">
        <ComboboxOptions
          class="absolute mt-1 z-10 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
          <div v-if="filteredOptions.length === 0 && !isLoading && !queryOption && !props.createOption"
            class="relative cursor-default select-none py-2 px-4 text-gray-700">
            Nada encontrado.
          </div>
          <div v-if="isLoading" class="relative cursor-default select-none py-2 px-4 text-gray-700">
            Cargando...
          </div>

          <template v-if="!isLoading">
            <ComboboxOption v-if="shouldShowCreateOption" as="template" :value="queryOption" v-slot="{ active }">
              <li class="relative cursor-default select-none py-2 pl-10 pr-4" :class="{
                'bg-blumine-500 text-white': active,
                'text-gray-900': !active,
              }">
                Crear "{{ queryOption.label }}"
              </li>
            </ComboboxOption>
            <ComboboxOption v-for="option in filteredOptions" as="template" :key="option.value" :value="option"
              v-slot="{ selected, active }">
              <li class="relative cursor-default select-none py-2 pl-10 pr-4" :class="{
                'bg-blumine-500 text-white': active,
                'text-gray-900': !active,
              }">
                <span class="block truncate" :class="{ 'font-medium': selected, 'font-normal': !selected }">
                  {{ option.label }}
                </span>
                <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3"
                  :class="{ 'text-white': active, 'text-blumine-500': !active }">
                  <CheckIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </li>
            </ComboboxOption>
          </template>
        </ComboboxOptions>
      </TransitionRoot>
    </div>
  </Combobox>
</template>

<script setup>
import { ref, computed, watch, defineEmits, defineProps, inject } from 'vue';
import {
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
  TransitionRoot,
} from '@headlessui/vue';
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid';

import { useThrottle } from '@/composables';

const emit = defineEmits(['update:modelValue']);

const props = defineProps({
  modelValue: [Number, Object],
  options: {
    type: Array,
    default: () => [],
  },
  loadOptions: Function,
  createOption: Function,
});

const field = inject('field', props);

const selectedValue = ref({ value: '', label: '' });
const options = ref(props.options);
const isLoading = ref(false);
const query = ref('');

const queryOption = computed(() => {
  return query.value === '' ? null : { missing: true, label: query.value };
});

const shouldShowCreateOption = computed(() => {
  return queryOption.value && !filteredOptions.value.some(option => option.label === queryOption.value.label);
});

const filteredOptions = computed(() => {
  const queryLowerCase = query.value.toLowerCase().trim();
  if (queryLowerCase === '') {
    return options.value.filter(option => option.label && option.label.trim() !== '');
  } else {
    return options.value.filter(option =>
      option.label && option.label.toLowerCase().includes(queryLowerCase)
    );
  }
});

// Utiliza useThrottle para throttle la función loadOptions
const throttledLoadOptions = useThrottle((q) => {
  props.loadOptions(q, (results) => {
    options.value = results;
    if (
      props.modelValue &&
      !options.value.some(o => {
        return o.value === props.modelValue?.value;
      })
    ) {
      options.value.unshift(props.modelValue);
    }
    isLoading.value = false;
  });
}, 500);

watch(
  query,
  q => {
    if (props.loadOptions) {
      isLoading.value = true;
      throttledLoadOptions(q);
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
      emit('update:modelValue', valueToSendOption); // Emitir la opción creada al componente padre
      isLoading.value = false;
    });
  } else {
    const valueToSend = useModelValueValidator(selected, props.modelValue);
    emit('update:modelValue', valueToSend); 
    selectedValue.value = selected;
  }
}

function useModelValueValidator(selected, modelValue) {
  let valueToSend;

  if (typeof modelValue === 'object' && Object.keys(modelValue).length === 0) {
    // Si modelValue es un objeto vacío, envía el objeto completo seleccionado
    valueToSend = selected;
  } else if (typeof modelValue === 'number') {
    // Si modelValue es un número, envía el valor seleccionado
    valueToSend = selected.value;
  } else if (typeof modelValue === 'object' && Object.keys(modelValue).length === 2) {
    // Si modelValue es un objeto con dos propiedades, asigna los valores correctamente
    const [valueProp, labelProp] = Object.keys(modelValue);
    valueToSend = {
      [valueProp]: selected.value,
      [labelProp]: selected.label
    };
  } else {
    // En otros casos, utiliza el valor tal como está
    valueToSend = modelValue !== undefined ? modelValue : null;
  }

  return valueToSend;
}

</script>
