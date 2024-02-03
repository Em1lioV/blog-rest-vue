<template>
  <div ref="containerRef">
    <!-- Botón personalizado que abre/cierra el dropdown -->
    <div class="flex flex-row items-center justify-center" @click="toggleDropdown">
      <slot></slot>
    </div>

    <!-- Contenido del dropdown -->
    <transition @before-enter="beforeEnter" @after-enter="afterEnter" @before-leave="beforeLeave"
      @after-leave="afterLeave">
      <div v-if="isOpen" ref="dropdownRef" 
        class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 overflow-hidden ring-black ring-opacity-5 focus:outline-none"
      >
        <!-- Dropdown content -->
        <template v-for="(option, index) in options">
        
          <hr v-if="option.separator" class="my-1 border-t border-gray-300" :key="`hr-${index}`">
          
          <RouterLink v-if="option.to" :to="option.to" :class="[defaultClass, option.className]"
            @click="handleOptionClick(option)" :key="`router-link-${index}`">
            {{ option.label }}
          </RouterLink>
          <span v-if="option.onClick" :class="[defaultClass, option.className]" @click="handleOptionClick(option)" :key="`span-${index}`">
            {{ option.label }}
          </span>
        </template>
      </div>
    </transition>
  </div>
</template>


<script setup>
import { ref, defineProps } from 'vue';
import useClickOutside from '../util/useClickOutside';

const { options } = defineProps(['options']);
const isOpen = ref(false);
const containerRef = ref();

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const beforeEnter = (el) => {
  el.style.transformOrigin = 'top right';
  el.style.opacity = 0;
};

const afterEnter = (el) => {
  el.style.transformOrigin = '';
  el.style.opacity = 1;
};

const beforeLeave = (el) => {
  el.style.transformOrigin = 'top right';
  el.style.opacity = 1;
};

const afterLeave = (el) => {
  el.style.transformOrigin = '';
  el.style.opacity = 0;
};

const handleOptionClick = (option) => {
  toggleDropdown();
  if (option.onClick) {
    option.onClick();
  }
};

useClickOutside(containerRef, () => {
  if (isOpen.value) {
    toggleDropdown();
  }
});

const defaultClass = 'block px-4 py-2 text-lg text-gray-700 cursor-pointer hover:bg-slate-100';
</script>
