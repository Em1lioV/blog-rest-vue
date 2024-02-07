<template>
    <div
        :class="['w-full rounded-md border-[1px] relative bg-cover-container aspect-[16/6] shadow-black', field.invalid ? 'border-red-500' : 'border-blumine-400']">
        <img v-if="fileUrl" class="w-full h-full object-cover" :src="fileUrl" alt="" />
        <div v-else class="w-full h-full justify-center flex items-center aspect-[16/6]">
            <img src="../../assets/logo.png" alt="" class="bg-cover w-[25%] min-w-[100px]" />
        </div>

        <div class="absolute inset-0 flex flex-col items-end justify-end p-4">
            <div class="mt-auto">
                <input :id="field.id" type="file" accept="image/*" ref="fileInput" class="hidden" @change="handleFileChange"
                    :required="field.required" />
                <button type="button" @click="openFileInput" aria-label="Seleccionar imagen" :class="[' rounded-md bg-white mr-1 px-2.5 py-1.5 text-xs sm:text-sm font-semibold text-gray-900 ring-1 ring-inset hover:bg-gray-50',
                    field.invalid ? 'ring-red-500' : 'ring-gray-300', props.buttonClass]">
                    {{ props.buttonText }}
                </button>
                <button type="button" @click="removeFile"
                    class="rounded-md bg-white px-2.5 py-1.5 text-xs sm:text-sm font-semibold text-red-600 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                    Eliminar
                </button>
            </div>
        </div>
    </div>
</template>
    
<script setup>
import { inject } from 'vue';

import useFileInput from '@/composables/useFileInput';
const emit = defineEmits(["update:modelValue"]);

const emitUpdateModelValue = (file) => {
    emit('update:modelValue', file);
};

const props = defineProps({
    buttonText: {
        type: String,
        default: 'Cambiar'
    },
    buttonClass: {
        type: String,
        default: ''
    }
})

const { fileInput, fileUrl, openFileInput, handleFileChange, removeFile } = useFileInput(emitUpdateModelValue);

const field = inject('field', props);
</script>
  