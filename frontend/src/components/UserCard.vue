<template>
    <div class="flex items-center text-xs mb-3">
        <router-link :to="'/profile/' + user.id" class="none">
            <div class="text-start relative flex items-center gap-x-2">
                <Avatar responsive :src="user.profile_image" :name="user.fullname" :initials="user.initials" />
                <div class="text-sm leading-1">
                    <h2 class="font-semibold text-gray-900">{{ user.fullname }}</h2>
                    <h3 class="text-gray-600 hidden sm:inline-block p-0 m-0" v-if="user.role">
                        {{ user.role.description }}
                    </h3>
                </div>
            </div>
        </router-link>
    </div>
</template>

<script setup>
import { Avatar } from '.';

const props = defineProps({
    user: Object
})

</script>
