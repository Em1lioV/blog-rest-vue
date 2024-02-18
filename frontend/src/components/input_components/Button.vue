<template>
  <component :is="elementType" :class="buttonClass" :to="props.to" :disabled="props.disabled" :type="props.type">
    <svg v-if="props.loading" class="animate-spin h-5 w-5 absolute" xmlns="http://www.w3.org/2000/svg"
      fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
      </path>
    </svg>
    <component :is="props.leftICon" :class="['w-5 h-5 mr-2', props.loading ? 'invisible' : '']" />
    <span :class="[props.loading ? 'invisible' : '', 'text-center']">
      <slot />
    </span>

    <component :is="props.rightICon" :class="['w-5 h-5 ml-2', props.loading ? 'invisible' : '']" />
  </component>
</template>
  
<script setup>
import { cva } from 'class-variance-authority';
import { defineProps, computed } from 'vue';

const props = defineProps({
  leftICon: Object,
  rightICon: Object,
  loading: Boolean,
  disabled: Boolean,
  ring: Boolean,
  block: Boolean,
  to: String,
  intent: {
    type: String,
    validator: val => ["primary", "secondary", "danger", "ghost", "link"].includes(val),
    default: "primary",
  },
  size: {
    type: String,
    validator: val => ["xm", "sm", "md", "lg", "xl"].includes(val),
    default: "md",
  },
  type: {
    type: String,
    validator: val => ["button", "submit"].includes(val),
    default: "button",
  }
});

const elementType = computed(() => {
  return props.to ? 'router-link' : 'button'
});

// Clases base del botón sin estilos de hover
const baseButtonClass = cva(
  "inline-flex items-center justify-center font-semibold rounded mr-2 py-0.5 ",
  {
    variants: {
      intent: {
        primary: props.ring ? "ring-2 ring-inset ring-blumine-400 bg-white text-blumine-400" : "bg-blumine-400 text-white",
        secondary: props.ring ? "ring-2 ring-inset ring-blumine-800 bg-white text-blumine-800" : "bg-blumine-800 text-white",
        danger: props.ring ? "ring-2 ring-inset ring-red-600 bg-white text-red-600" : "bg-red-600 text-white",
        ghost: props.ring ? "ring-2 ring-inset ring-transparent bg-transparent text-gray-700" : "text-gray-700",
        link: props.ring ? "ring-2 ring-inset ring-transparent bg-transparent text-blumine-400 !py-0 !px-1" : "text-blumine-400 !p-0",
      },
      disabled: {
        true: 'cursor-not-allowed opacity-60'
      },
      size: {
        xm: 'text-xs px-2 min-h-[20px] min-w-[36px]',
        sm: 'text-sm px-3 min-h-[28px] min-w-[50px]',
        md: 'text-md px-4 min-h-[36px] min-w-[64px]',
        lg: 'text-lg px-5 min-h-[44px] min-w-[78px]' ,
        xl: 'text-xl px-6 min-h-[52px] min-w-[92px]',
      },
      block: {
        true: 'w-full',
      }
    }
  }
)({ intent: props.intent, disabled: props.disabled, size: props.size, block: props.block });

// Clases de hover para cada variante de intención del botón
const hoverClass = computed(() => {
  return props.disabled ? '' : cva('', {
    variants: {
      intent: {
        primary: props.ring ? "hover:bg-blumine-100" : "hover:bg-blumine-500",
        secondary: props.ring ? "hover:bg-blumine-200" : "hover:bg-blumine-700",
        danger: props.ring ? "hover:bg-red-100" : "hover:bg-red-500",
        ghost: props.ring ? "hover:bg-black/10 hover:ring-gray-700" : "hover:bg-black/10",
        link: props.ring ? "hover:ring-blumine-300" : "hover:text-blumine-300",
      }
    }
  })({ intent: props.intent });
});

// Clase final del botón con estilos de hover
const buttonClass = computed(() => baseButtonClass + ' ' + hoverClass.value);
</script>
