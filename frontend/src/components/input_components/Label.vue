<template>
    <label :for="props.for" class="block text-sm font-medium leading-6 text-gray-900 mb-1"><slot/>
        <span v-if="props.required" class="text-red-600">*</span></label>
</template>

<script setup>
const props = defineProps({
    for: String,
    required: Boolean
})
</script>
