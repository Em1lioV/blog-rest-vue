<template>
    <div class="inline-flex items-center ">
        <div class="" ref="referenceRef" @mouseenter="show" @mouseleave="hide" @focus="show" @blur="hide">
            <slot />
        </div>

        <div ref="floatingRef" :class="['absolute top-0 left-0 z-50 bg-blumine-700 select-none text-sm text-white px-3 py-1.5 rounded-md cursor-default',
            isHidden && 'hidden']">
            {{props.content}}
            <div class="absolute bg-blumine-700 h-[8px] w-[8px] rotate-45" ref="arrowRef">

            </div>
        </div>
    </div>
</template>

<script setup>

import { arrow, computePosition, flip, offset, shift } from '@floating-ui/vue'
import { ref } from 'vue'

const referenceRef = ref(null)
const floatingRef = ref(null)
const arrowRef = ref(null)
const isHidden = ref(true)

const props = defineProps({
    content: String,
    placement: {
        type: String,
        default: 'bottom'
    }
})

function hide() {
    isHidden.value = true
}
function show() {
    isHidden.value = false
    calculatePosition()
}

async function calculatePosition() {
    const { x, y, middlewareData, placement } = await computePosition(referenceRef.value, floatingRef.value, {
        placement: props.placement,
        middleware: [offset(8), flip(), shift({ padding: 5 }), arrow({ element: arrowRef.value })]
    });

    Object.assign(floatingRef.value.style, {
        left: `${x}px`,
        top: `${y}px`
    })
 
    const { x: arrowX, y: arrowY } = middlewareData.arrow;

    const opposedSide = {
        left: 'right',
        right: 'left',
        top: 'bottom',
        bottom: 'top',
    }[placement.split('-')[0]];

    Object.assign(arrowRef.value.style, {
        left: arrowX ? `${arrowX}px` : '',
        top: arrowY ? `${arrowY}px` : '',
        bottom: "",
        right: "",
        [opposedSide]: "-4px"
    })

}
</script>