<template>
    <nav
        class="relative overflow-hidden select-none text-sm font-medium -mb-px text-center text-gray-500 border-b border-gray-200">
        <button ref="leftButtonRef" tabindex="-1" aria-label="Scroll hacia la izquierda"
            class="w-[30px] md:w-[60px] top-0 h-full absolute flex items-center bg-gradient-to-r from-50% from-white">
            <ChevronLeftIcon aria-hidden="true" class="w-6 h-6 cursor-pointer hover:fill-blumine-400" />
        </button>
        <ul class="flex gap-4 list-none m-0 overflow-x-scroll no-scrollbar scroll-smooth" ref="tabsList" role="tablist">
            <li v-for="(tab, index) in tabs" :key="index" role="presentation"
                :data-no-click-on-key-navigation="tab.noClickOnKeyNavigation"
                class="p-1 cursor-pointer inline-block border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300 text-nowrap"
                :class="{
                '!border-blumine-400 !text-blumine-400 hover:!text-blumine-500 hover:!border-blumine-500':
                    isTabActive(tab.to),
            }">
                <TabButton :tab="tab" />
            </li>
        </ul>
        <button ref="rightButtonRef" aria-label="Scroll hacia la derecha"
            tabindex="-1"
            class="bg-gradient-to-l from-50% from-white w-[30px] md:w-[60px] top-0 right-0 justify-end h-full absolute flex items-center">
            <ChevronRightIcon aria-hidden="true" class="w-6 h-6 cursor-pointer hover:fill-blumine-400" />
        </button>
    </nav>
</template>

<script setup>
import { ref ,watch} from "vue";
import { useRoute } from "vue-router";
import { ChevronLeftIcon, ChevronRightIcon } from "@heroicons/vue/24/solid";
import { TabButton } from "../components";
import { useScrollControls,useTabKeyNavigation } from "@/composables";

const props = defineProps({
    tabs: Array,
});

const tabsList = ref(null);
const route = useRoute();


const leftButtonRef = ref(null);
const rightButtonRef = ref(null);


const isTabActive = (to) => {
      if (to.name){
        return route.name === to.name
      } else {
        return route.fullPath === to;
      }
}


useScrollControls(tabsList, {leftButtonRef :leftButtonRef, rightButtonRef:rightButtonRef});
useTabKeyNavigation(tabsList);


</script>