<template>
    <input 
        :id="field.id" 
        :value="props.modelValue" @input="$emit('update:modelValue', $event.target.value)" 
        :class="['block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6',
        field.invalid ? 'ring-red-500' : 'ring-gray-300']" 
        :required="field.required" 
        :type="props.type"/>
</template>
  
<script setup>
import { inject } from 'vue';

const props = defineProps({
    id: String,
    modelValue: [String, Number],
    required: Boolean,
    invalid: Boolean,
    ariaDescribeBy: String,
    type: String
});

const field = inject('field', props);

</script>
  