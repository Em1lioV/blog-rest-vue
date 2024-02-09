<template>
    <div class="relative ">
      <Input
        v-bind="$attrs"
        :id="id"
        :required="required"
        :invalid="invalid"
        :ariaDescribeBy="ariaDescribeBy"
        :type="inputType"
        :class="'pr-[40px] peer '"

      />
      <!-- Botón de mostrar/ocultar contraseña -->
      <button type="button"
        class="absolute inset-y-0 right-0 px-2 py-1.5 flex items-center focus:outline-none text-gray-300 peer-focus/:text-blumine-400"
        @click="togglePasswordVisibility"
      >
        <template v-if="isVisible">
          <EyeSlashIcon class="h-6 w-6  fill-current hover:text-blumine-500" />
        </template>
        <template v-else>
          <EyeIcon class="h-6 w-6 fill-current hover:text-blumine-500"  />
        </template>
      </button>
    </div>
  </template>
  
  <script setup>
  import Input from './Input.vue';
  import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/solid';
  import { defineProps, ref, computed } from 'vue';
  
  const props = defineProps({
    id: String,
    required: Boolean,
    invalid: Boolean,
    ariaDescribeBy: String,
    type: String
  });
  
  // Variable para controlar la visibilidad de la contraseña
  const isVisible = ref(false);
  
  // Método para alternar la visibilidad de la contraseña
  const togglePasswordVisibility = () => {
    isVisible.value = !isVisible.value;
  };
  
  // Calcula el tipo de entrada (password o text) según la visibilidad de la contraseña
  const inputType = computed(() => {
    return isVisible.value ? 'text' : 'password';
  });
  </script>