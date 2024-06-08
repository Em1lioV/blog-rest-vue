<template>
    <component :is="elementType" role="tab"
        class="inline-flex items-center justify-center p-1 focus:outline-none focus-visible:ring focus-visible:ring-blumine-300"
        :to="tab.to" :tabindex="tabindex" :aria-selected="isTabActive" :disabled="tab.disabled" :title="tabTitle">

        <component :is="tab.leftIcon" class="w-5 h-5 mr-2" />
        <component :is="tab.Icon" class="w-5 h-5" />
        {{tab.title}}
        <component :is="tab.rightIcon" class="w-5 h-5 ml-2" />

    </component>
</template>

<script setup>
import { useRoute } from "vue-router";
import { computed } from 'vue'

const props = defineProps({
    tab: Object
});

const route = useRoute();

const elementType = computed(() => {
    return props.tab.to ? 'router-link' : 'button';
});

const isTabActive = computed(() => {
    return route.path === props.tab.to;
});

const tabindex = computed(() => {
    return props.tab.tabIndex ? props.tab.tabIndex : isTabActive.value ? '0' : '-1';
});

const tabTitle = computed(() => {
    return props.tab.iconTitle || props.tab.title;
});
</script>