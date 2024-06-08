<template>
    <div class="flex min-h-full overflow-hidden flex-col justify-center items-center px-6 py-12 lg:px-8 ">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <router-link to="/" class="flex items-center">
                <img class="mx-auto w-60" src="../assets/logo.svg" alt="Tu Empresa">
            </router-link>
            <h2 class=" text-center text-xl font-bold leading-9 tracking-tight text-gray-600">
                Inicia sesión en tu cuenta
            </h2>
        </div>

        <div class="mt-5 sm:mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form class="space-y-2" v-on:submit.prevent="login">

                <Field id="email" label="Correo electrónico" required="">
                    <Input v-model="email" type="email" autocomplete="email" />
                </Field>

                <Field id="password" label="Contraseña" required :leftLabelSlot="leftLabelSlot">
                    <PasswordInput v-model="password" autocomplete="current-password" />
                </Field>

                <div class="flex justify-center items-center w-full mt-2">
                    <Button type="submit" class="w-full md:w-auto">
                        Iniciar sesión
                    </Button>
                </div>

                <div class="w-full block sm:hidden mt-2">
                    <Button to="/forgot-password" intent="secondary" block ring>
                        ¿Olvidaste tu contraseña?
                    </Button>
                </div>

                <p class="mt-8 text-center text-sm text-gray-500">
                    ¿No eres miembro?
                    <Button to="/register" intent="link">Crea una cuenta</Button>
                </p>
            </form>
        </div>
    </div>
</template>


<script setup>
import { Field, Input, PasswordInput, Button } from '@/components/input_components';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const email = ref('');
const password = ref('');


const router = useRouter();
const store = useStore();

const login = async () => {
    const data = {
        email: email.value,
        password: password.value,
    };

    try {
        await store.dispatch('userLogin', data);
        router.push({ name: 'home' });
    } catch (err) {
    }
};

const leftLabelSlot = {
    text: '¿Olvidaste tu contraseña?',
    href: '/forgot-password',
    class: 'font-semibold text-blumine-400 hover:text-blumine-300 hidden sm:inline-block'
}
</script>
