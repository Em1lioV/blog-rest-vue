<template>
    <div>
        <Label 
            v-if="props.label"
            :for="props.id"
            :required="props.required"
        >
            {{ props.label }}
        </Label>
        <slot/>
        <ErrorMessage v-if="props.error">
            {{ props.error }}
        </ErrorMessage>
        <HelperMessage v-if="props.help && !props.error">
            {{ props.help }}
        </HelperMessage>
    </div>
</template>

<script setup>
import { computed, provide } from 'vue';
import ErrorMessage from './ErrorMessage.vue';
import HelperMessage from './HelperMessage.vue';

import Label from './Label.vue';
import { v4 as uuid } from 'uuid'

const props = defineProps({	
    id : {
        type:String,
        default:() => `field-${uuid()}`
    },	
    label : String,	
    error : String,	
    help : String,	
    required : Boolean,	
})


const ariaDescribeBy = computed(()=>{
    return !!props.help ? `help-${uuid()}` : null;
})

provide('field',computed(()=>{
    return {
        ...props,
        invalid: !!props.error,
        ariaDescribeBy:ariaDescribeBy.value
    }
}));
</script>
