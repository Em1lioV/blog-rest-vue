
<template>
    <div class="flex min-h-full overflow-hidden flex-col justify-center items-center px-6 py-12 lg:px-8 ">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <router-link to="/" class="flex items-center">
                <img class="mx-auto h-[130px] w-auto" src="../assets/logo.png" alt="Tu Empresa">
            </router-link>
            <h2 class="mt-5 sm:mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                Inicia sesión en tu cuenta
            </h2>
        </div>

        <p v-if="incorrectAuth">credenciales incorrectas - por favor intente de nuevo</p>
        <div v-on:submit.prevent="login" class="mt-5 sm:mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form class="space-y-6" action="#" method="POST">
                <div>
                    <Field id="email" label="Correo electrónico" required="">
                        <Input v-model="email" type="email" autocomplete="email" />
                    </Field>

                </div>
                <div>
                    <Field id="password" label="Contraseña" required=""
                        :leftLabelSlot="{ text: '¿Olvidaste tu contraseña?', href: '/forgot-password', class: 'font-semibold text-blumine-400 hover:text-blumine-300 hidden sm:inline-block' }">

                        <Input v-model="password" type="password" autocomplete="current-password" />
                    </Field>

                </div>

                <div>
                    <button type="submit"
                        class="flex w-full justify-center rounded-md bg-blumine-400 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-blumine-500  focus-visible:outline-blumine-400">Iniciar
                        sesión</button>
                </div>
            </form>

            <div class="w-full block sm:hidden">
                <router-link to="/forgot-password"
                    class="inline-flex items-center justify-center text-center w-full mt-2 border-2 border-blumine-400 text-blumine-400 font-bold px-3 py-1.5 rounded text-sm">
                    ¿Olvidaste tu contraseña?
                </router-link>
            </div>

            <p class="mt-8 text-center text-sm text-gray-500">
                ¿No eres miembro?
                <router-link to="/register" class="font-semibold leading-6 text-blumine-400 hover:text-blumine-300">
                    Crea una cuenta
                </router-link>
            </p>
        </div>
    </div>
</template>


<script setup>
import { Field,Input } from '@/components/input_components';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const email = ref('');
const password = ref('');
const incorrectAuth = ref(false);

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
        console.log(err);
        incorrectAuth.value = true;
    }
};
</script>
