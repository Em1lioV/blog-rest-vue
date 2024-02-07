<template>
    <div>
        <div class="flex items-center justify-between">
            <Label v-if="props.label" :for="props.id" :required="props.required">
                {{ props.label }}
            </Label>
            <div v-if="props.leftLabelSlot" class="text-sm">
                <template v-if="typeof props.leftLabelSlot === 'string'">
                    <p>{{ props.leftLabelSlot }}</p>
                </template>
                <template v-else-if="props.leftLabelSlot.href">
                    <router-link :to="props.leftLabelSlot.href" :class="props.leftLabelSlot.class">
                        {{ props.leftLabelSlot.text }}
                    </router-link>
                </template>
                <template v-else>
                    <p :class="[props.leftLabelSlot.class ? props.leftLabelSlot.class : '']">
                        {{ props.leftLabelSlot.text }}
                    </p>
                </template>
            </div>
        </div>
        <slot />
        <ErrorMessage v-if="props.error">
            {{ props.error }}
        </ErrorMessage>
        <HelperMessage v-if="props.help && !props.error">
            {{ props.help }}
        </HelperMessage>
    </div>
</template>
  
<script setup>
import { defineProps, computed, provide } from 'vue';
import ErrorMessage from './ErrorMessage.vue';
import HelperMessage from './HelperMessage.vue';
import Label from './Label.vue';
import { v4 as uuid } from 'uuid';

const props = defineProps({
    id: {
        type: String,
        default: () => `field-${uuid()}`,
        description: 'Unique identifier for the field.'
    },
    label: {
        type: String,
        description: 'Main label for the field.'
    },
    error: {
        type: String,
        description: 'Error message associated with the field.'
    },
    help: {
        type: String,
        description: 'Help message for the field.'
    },
    required: {
        type: Boolean,
        default: false,
        description: 'Indicates whether the field is required.'
    },
    leftLabelSlot: {
        type: [Object, String],
        default: null,
        description: 'Content for the left label slot or configuration object.'
    }
});

const ariaDescribeBy = computed(() => {
    return !!props.help ? `help-${uuid()}` : null;
});

provide('field', computed(() => {
    return {
        ...props,
        invalid: !!props.error,
        ariaDescribeBy: ariaDescribeBy.value
    };
}));
</script>
