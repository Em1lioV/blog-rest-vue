<script setup>
import { computed, watchEffect, ref } from "vue";
import { cva } from "class-variance-authority";

const props = defineProps({
  name: String,
  src: String,
  initials: String,
  size: {
    type: String,
    validator: (value) => ["sm", "base", "md", "lg"].includes(value),
    default: "base",
  },
  shape: {
    type: String,
    validator: (value) => ["circle", "square"].includes(value),
    default: "circle",
  },
});

const verifiedSrc = ref(null);



watchEffect(() => {
  if (props.src && props.src !== '') {
    const img = new Image();

    img.src = props.src;
    img.decode()
      .then(() => {
        verifiedSrc.value = props.src;
      })
      .catch((e) => {
        verifiedSrc.value = null;
      });
  } else {
    // Si no se proporciona una imagen, establecer verifiedSrc como null
    verifiedSrc.value = null;
  }
});

const fallback = computed(() => {
  return props.initials?.toUpperCase() || props.name?.charAt(0).toUpperCase() || "?";
});

const ContainerClass = computed(() => {
  return cva(
    "relative inline-flex items-center justify-center font-bold text-slate-700 select-none shrink-0 bg-slate-200  overflow-hidden",
    {
      variants: {
        size: {
          sm: "text-xs  h-8 w-8",
          base: "text-xl  h-12 w-12",
          md: "text-2xl  h-16 w-16",
          lg: "text-5xl  h-28 w-28",
        },
        shape: {
          circle: "rounded-full",
          square: "rounded",
        },
      },
    }
  )({ size: props.size, shape: props.shape })
});

const innerBorderClass = computed(() => {
  return cva(
    "absolute inset-0 border border-black/5",
    {
      variants: {
        shape: {
          circle: "rounded-full",
          square: "rounded",
        },
      },
    }
  )({ shape: props.shape })
});
</script>

<template>
  <span class="" :title="props.name" :class="ContainerClass">
    <img class="h-full w-full object-cover" v-if="verifiedSrc" :src="verifiedSrc" :alt="props.name" />
    <template v-else>{{ fallback }}</template>
    <span :class="innerBorderClass"></span>
  </span>
</template>
