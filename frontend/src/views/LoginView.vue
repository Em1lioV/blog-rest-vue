
<template>
    <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8 ">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <router-link to="/" class="flex items-center">
                <img class="mx-auto h-[130px] w-auto" src="../assets/logo.png" alt="Tu Empresa">
              </router-link>
            <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Inicia sesión en tu
                cuenta
            </h2>
        </div>

        <p v-if="incorrectAuth">credenciales incorrectas - por favor intente de nuevo</p>
        <div v-on:submit.prevent="login" class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form class="space-y-6" action="#" method="POST">
                <div>
                    <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Dirección de correo
                        electrónico</label>
                    <div class="mt-2">
                        <input v-model="email" id="email" name="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 p-1.5 text-gray-900 
                    shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 
                    focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6 outline-none">
                    </div>
                </div>

                <div>
                    <div class="flex items-center justify-between">
                        <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Contraseña</label>
                        <div class="text-sm">
                            <a href="#" class="font-semibold text-blumine-400 hover:text-blumine-300">¿Olvidaste tu
                                contraseña?</a>
                        </div>
                    </div>
                    <div class="mt-2">
                        <input v-model="password" id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 p-1.5 text-gray-900 shadow-sm ring-1 
                    ring-inset ring-gray-300 placeholder:text-gray-400 
                    focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6 outline-none">
                    </div>
                </div>

                <div>
                    <button type="submit"
                        class="flex w-full justify-center rounded-md bg-blumine-400 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-blumine-300  focus-visible:outline-blumine-400">Iniciar
                        sesión</button>
                </div>
            </form>

            <p class="mt-10 text-center text-sm text-gray-500">
                ¿No eres miembro?
                <a href="#" class="font-semibold leading-6 text-blumine-400 hover:text-blumine-300">Crea una cuenta</a>
            </p>
        </div>
    </div>
</template>


<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const email = ref('');
const password = ref('');
const incorrectAuth = ref(false);

const router = useRouter();
const store = useStore(); // Accede al store Vuex

const login = async () => {
  const data = {
    email: email.value,
    password: password.value,
  };

  try {
    await store.dispatch('userLogin', data); // Llama a la acción del store

    // Redirige al usuario a la página de inicio
    router.push({ name: 'perfil' });
  } catch (err) {
    // Maneja el error como desees
    console.log('Error en la autenticación');
    incorrectAuth.value = true;
  }
};
</script>
