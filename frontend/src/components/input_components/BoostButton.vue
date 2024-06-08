<template>
    <BaseTooltip content="impulsar" placement="top">
        <div class="flex gap-x-2 items-center" @click="toggleBoost">
            <solidRocketIcon v-if="isBoosted" class="w-7 h-7 cursor-pointer fill-blumine-400 select-none" />
            <outlineRocketIcon v-else class="w-7 h-7 cursor-pointer stroke-gray-600 hover:stroke-blumine-400 select-none" />

            <p class="text-sm text-gray-400">{{ boostCounts }}</p>
        </div>
    </BaseTooltip>
</template>

<script setup>
import { computed, ref, defineProps, defineEmits } from 'vue';
import { PostService } from '@/services';
import store from '@/store';
import { useRouter } from 'vue-router';
import { BaseTooltip } from '..';
import { RocketLaunchIcon as outlineRocketIcon } from "@heroicons/vue/24/outline";
import { RocketLaunchIcon as solidRocketIcon } from "@heroicons/vue/24/solid";

const props = defineProps({
    modelValue: {
        type: Object
    },
    initialIsBoosted: {
        type: Boolean,
        default: false
    },
    initialBoostsCounts: {
        type: [Number]
    },
    postId: {
        type: Number,
        required: true
    }
});

const router = useRouter();

const initialIsBoosted = ref(props.initialIsBoosted);
const initialBoostsCounts = ref(props.initialBoostsCounts);

const emit = defineEmits(['update:modelValue']);

const isBoosted = computed(() => props.modelValue ? props.modelValue.IsBoosted : initialIsBoosted.value);
const boostCounts = computed(() => props.modelValue ? props.modelValue.boosts_count : initialBoostsCounts.value);

const toggleBoost = async () => {
    if (store.state.access_token) {
        const res = await PostService.toggleBoost(props.postId);
        let newCount = boostCounts.value;
        if (res.boosted) {
            newCount = ++newCount; // Incremento
        } else {
            newCount = --newCount; // Decremento
        }
        const newValue = {
            IsBoosted: res.boosted,
            boosts_count: newCount
        };

        if (props.modelValue !== null) {
            emit('update:modelValue', newValue);
        } else {
            initialIsBoosted.value = newValue.IsBoosted;
            initialBoostsCounts.value = newValue.boosts_count;
        }
    } else {
        router.push({ name: 'login' });
    }
};
</script>