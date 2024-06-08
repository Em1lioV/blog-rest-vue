<template>
    <Button v-if="isFollowing" ring block @click="toggleFollow">siguiendo</Button>
    <Button v-else block @click="toggleFollow">seguir</Button>
    
</template>

<script setup>
import { ref } from 'vue';
import { userService } from '@/services';
import { Button } from '@/components/input_components';
import store from '@/store';
import { useRouter } from 'vue-router';


const props = defineProps({
    userId: {
        type: Number,
        required: true
    },
    initialIsFollowing: {
        type: Boolean,
        default: false
    }
})
const router = useRouter()

const userId = ref(props.userId);
const isFollowing = ref(props.initialIsFollowing);


const toggleFollow = async () => {
    if (store.state.access_token) {
        const res = await userService.togglefollowUser(userId.value);
        isFollowing.value = res.is_following;
    }else{
        router.push({ name: 'login'});
    }
};

</script>
