<template>
    <div class="mt-2 flex items-center gap-x-3">
        <span class="cursor-pointer  flex items-center">
            <Avatar size="md" :src="fileUrl" :name="props.name" :initials="props.initials"
                :class="[field.invalid ? 'ring-1 ring-red-500' : '']" />
        </span>
        <input :id="field.id" type="file" accept="image/*" ref="fileInput" @change="handleFileChange" class="hidden" />
        <div >
            <Button size="sm" intent="secondary" ring @click="openFileInput">Cambiar</Button>
            <Button size="sm" intent="danger" ring @click="removeFile">Eliminar</Button>
        </div>
    </div>
</template>
    
<script setup>
import { inject } from 'vue';

import useFileInput from '@/composables/useFileInput';
import Avatar from '../Avatar.vue';
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
    name: String,
    initials: String,
    buttonClass: {
        type: String,
        default: ''
    }
})

const { fileInput, fileUrl, openFileInput, handleFileChange, removeFile } = useFileInput(emitUpdateModelValue);

const field = inject('field', props);
</script>
  