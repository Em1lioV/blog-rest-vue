<template>
    <BaseTooltip content="guardar" placement="top">
        <div @click="toggleBookmark">
            <BookmarkIcon
                :class="{ 'fill-blumine-400 stroke-blumine-400': isBookmarked, 'stroke-gray-600 hover:stroke-blumine-400': !isBookmarked }"
                class="w-6 h-6 cursor-pointer select-none" />
        </div>
    </BaseTooltip>
</template>

<script setup>
import { computed, ref } from 'vue';
import { BookmarkIcon } from "@heroicons/vue/24/outline";
import { PostService } from '@/services';
import store from '@/store';
import { useRouter } from 'vue-router';
import { BaseTooltip } from '..';

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: null
    },
    initialIsBookmarked: {
        type: Boolean,
        default: false
    },
    postId: {
        type: Number,
        required: true
    }
});

const router = useRouter();

console.log(props);


const initialIsBookmarked = ref(props.initialIsBookmarked);

const isBookmarked = computed(() => props.modelValue !== null ? props.modelValue : initialIsBookmarked.value);

const emit = defineEmits(['update:modelValue']);

const toggleBookmark = async () => {
    if (store.state.access_token) {
        const res = await PostService.toggleBookmark(props.postId);
        const newValue = res.is_bookmarked;

        if (props.modelValue !== null ) {
            emit('update:modelValue', newValue);
        } else {
            initialIsBookmarked.value = newValue;
        }
    } else {
        router.push({ name: 'login' });
    }
};
</script>