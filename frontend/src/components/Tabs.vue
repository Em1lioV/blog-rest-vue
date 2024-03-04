<template>
  <div class="mt-5 w-full">

    <nav class="text-sm font-medium text-center text-gray-500 border-b border-gray-200">
      <ul class="flex flex-wrap -mb-px overflow-x-auto">
        <li
          class="p-2 mr-4 cursor-pointer inline-block border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300"
          v-for="(tab, index) in tabs" :key="index" @click="selectTab(index)"
          :class="{ '!border-blumine-400 !text-blumine-400 hover:!text-blumine-500 hover:!border-blumine-500 ': selectedIndex === index }">
          {{ tab.component.props.title }}
        </li>
      </ul>
    </nav>
    <div class="mt-5">
      <div v-for="(tab, index) in tabs" :key="index" v-show="selectedIndex === index">
        <component :is="tab.component"></component>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, useSlots, watch } from 'vue';

const selectedIndex = ref(0);
const tabs = ref([]);

const selectTab = (index) => {
  selectedIndex.value = index;
};


const slots = useSlots()
const slotsDefault = slots.default();

const updateTabComponents = () => {
  const slotTabs = slotsDefault.filter(component => component.type.__name === 'Tab');

  const tabComponents = slotTabs.map(component => ({
    component: component
  }));

  tabs.value = tabComponents;
};


onMounted(() => {
  updateTabComponents();
});

// Reaccionar a los cambios en los slots
watch(() => slotsDefault, () => {
  updateTabComponents();
});
</script>