<template>
  <Combobox by="value" :model-value="props.modelValue" @update:model-value="handleUpdateModel">
    <div class="relative mt-1">
      
        <ComboboxInput required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6"
          :displayValue="(option) => option.label" @change="query = $event.target.value" />
        <ComboboxButton class="absolute inset-y-0 right-0 flex items-center pr-2">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </ComboboxButton>
     
      <TransitionRoot leave="transition ease-in duration-100" leaveFrom="opacity-100" leaveTo="opacity-0"
        @after-leave="query = ''">
        <ComboboxOptions
          class="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
          <div v-if="filteredOptions.length === 0 && !isLoading && !queryOption && !props.createOption"
            class="relative cursor-default select-none py-2 px-4 text-gray-700">
            Nothing found.
          </div>
          <div v-if="isLoading" class="relative cursor-default select-none py-2 px-4 text-gray-700">
            Loading...
          </div>

          <template v-if="!isLoading">
            <ComboboxOption v-if="queryOption && !filteredOptions.length && props.createOption" as="template"  :value="queryOption"
              v-slot="{  active }">
              <li class="relative cursor-default select-none py-2 pl-10 pr-4" :class="{
                'bg-blumine-500 text-white': active,
                'text-gray-900': !active,
              }">
               Create "{{ queryOption.label }}"
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
import { ref, computed, watch } from 'vue'
import {
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
  TransitionRoot,
} from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'


const props = defineProps({
  modelValue: Object,
  options: {
    type: Array,
    default: () => []
  },
  loadOptions: Function,
  createOption: Function,
})

const emit = defineEmits(["update:modelValue"])


let query = ref('')
const options = ref(props.options)
const isLoading = ref(false)

const queryOption = computed(() => {
  return query.value === "" ? null : {
    missing: true,
    label: query.value
  }
})

watch(query, (q) => {
  if (props.loadOptions) {
    isLoading.value = true
    props.loadOptions(q, (results) => {
      options.value = results
      if (props.modelValue && !options.value.some(o => {
        return o.value === props.modelValue?.value
      })
      ) {
        options.value.unshift(props.modelValue)
      }
      isLoading.value = false
    })

  }
}, { immediate: true })

let filteredOptions = computed(() =>
  query.value === ''
    ? options.value
    : options.value.filter((option) =>
      option.label
        .toLowerCase()
        .replace(/\s+/g, '')
        .includes(query.value.toLowerCase().replace(/\s+/g, ''))
    )
)

function handleUpdateModel(selected){
  emit("update:modelValue",selected)

  if(props.createOption && selected?.missing){
    isLoading.value = true
    props.createOption(selected,option => {
      emit("update:modelValue",option)
      isLoading.value = false
    })
  }
}
</script>
