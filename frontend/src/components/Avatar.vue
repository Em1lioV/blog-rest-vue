<template>
  <span class="" :title="props.name" :class="ContainerClass">
    <img class="h-full w-full object-cover" v-if="verifiedSrc" :src="verifiedSrc" :alt="props.name" />
    <template v-else><span class="mt-[0.05rem]">{{ fallback }}</span></template>
    <span :class="innerBorderClass"></span>
  </span>
</template>

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
  responsive: {
    type: Boolean,
    default: false,
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
    "relative inline-flex items-center justify-center font-bold text-slate-700 select-none shrink-0 bg-blumine-100  overflow-hidden",
    {
      variants: {
        size: {
          sm: "text-xs h-8 w-8",
          base: props.responsive ? "text-lg md:text-xl h-10 w-10 md:h-12 md:w-12 " : "text-xl h-12 w-12",
          md: props.responsive ? "text-xl md:text-2xl h-14 w-14 md:h-16 md:w-16" : "text-2xl h-16 w-16",
          lg: props.responsive ? "text-4xl md:text-5xl h-24 w-24 md:h-28 md:w-28" : "text-5xl h-28 w-28",
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