<template>
    <div
        class=" relative overflow-hidden select-none text-sm font-medium -mb-px text-center text-gray-500 border-b border-gray-200">
        <div v-show="showLeftButton"
            class="w-[30px] md:w-[60px] top-0 h-full absolute flex items-center bg-gradient-to-r from-50% from-white"
            ref="LeftButton" @click="moveScrollLeft()">
            <ChevronLeftIcon class="w-6 h-6 cursor-pointer hover:fill-blumine-400" />
        </div>
        <ul class="flex gap-4 list-none m-0  overflow-x-scroll no-scrollbar !scroll-smooth" ref="tabsList"
            @scroll="manageScrollButtons" @mousedown="startDrag" @mouseup="endDrag" @mouseleave="endDrag"
            @mousemove="drag">
            <li v-for="(tab, index) in tabs" :key="index"
                class="p-2 cursor-pointer inline-block border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300 text-nowrap"
                :class="{ '!border-blumine-400 !text-blumine-400 hover:!text-blumine-500 hover:!border-blumine-500': isTabActive(tab.link) }">
                <router-link :to="tab.link"
                    class="p-px focus:outline-none focus-visible:ring focus-visible:ring-blumine-300">{{
            tab.title }}</router-link>
            </li>
        </ul>
        <div v-show="showRightButton" @click="moveScrollRight()" ref="RightButton"
            class="bg-gradient-to-l from-50% from-white  w-[30px] md:w-[60px] top-0  right-0 justify-end h-full absolute flex items-center">
            <ChevronRightIcon class="w-6 h-6 cursor-pointer hover:fill-blumine-400" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from "vue";
import { useRoute } from "vue-router";
import { ChevronLeftIcon, ChevronRightIcon } from "@heroicons/vue/24/solid";

const props = defineProps({
    tabs: {
        type: Array,
        required: true,
    },
});

const route = useRoute();
const tabsList = ref(null);
const LeftButton = ref(null);
const RightButton = ref(null);
const showLeftButton = ref(false);
const showRightButton = ref(false);

let isDragging = false;
let startX = 0;
let scrollLeft = 0;

const moveScrollLeft = () => {
    const container = tabsList.value;
    container.scrollLeft -= 200;
    manageScrollButtons();
};

const moveScrollRight = () => {
    const container = tabsList.value;
    container.scrollLeft += 200;
    manageScrollButtons();
};

const startDrag = (event) => {
    isDragging = true;
    startX = event.pageX - tabsList.value.offsetLeft;
    scrollLeft = tabsList.value.scrollLeft;
};

const endDrag = () => {
    isDragging = false;
};

const drag = (event) => {
    if (!isDragging) return;
    event.preventDefault();
    const x = event.pageX - tabsList.value.offsetLeft;
    const walk = x - startX;
    tabsList.value.scrollLeft = scrollLeft - walk;
    manageScrollButtons();
};

const isTabActive = (link) => {
    return route.fullPath === link;
};

const manageScrollButtons = () => {
    const container = tabsList.value;

    if (!container) return;

    const maxScrollValue = container.scrollWidth - container.clientWidth;

    showLeftButton.value = container.scrollLeft > 0;
    showRightButton.value = container.scrollLeft < maxScrollValue;
};

onMounted(() => {
    manageScrollButtons();
});

</script>