<template>
    <div
        :class="['w-full rounded-md border-[1px] relative bg-cover-container aspect-[16/6] shadow-black', field.invalid ? 'border-red-500' : 'border-blumine-400']">
        <img v-if="fileUrl" class="w-full h-full object-cover" :src="fileUrl" alt="" />
        <div v-else class="w-full h-full justify-center flex items-center aspect-[16/6]">
            <img src="../../assets/logo.svg" alt="" class="bg-cover w-[25%] min-w-[100px]" />
        </div>

        <div class="absolute inset-0 flex flex-col items-end justify-end p-4">
            <div class="mt-auto">
                <input :id="field.id" type="file" accept="image/*" ref="fileInput" class="hidden" @change="handleFileChange"
                    :required="field.required" />

                <Button intent="secondary" ring size="sm" @click="openFileInput" aria-label="Seleccionar imagen">{{
                    props.buttonText }}</Button>
                <Button intent="danger" ring size="sm" @click="removeFile" aria-label="eliminar imagen">Eliminar</Button>


            </div>
        </div>
    </div>
</template>
    
<script setup>
import { inject } from 'vue';

import useFileInput from '@/composables/useFileInput';
import Button from './Button.vue';
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
  