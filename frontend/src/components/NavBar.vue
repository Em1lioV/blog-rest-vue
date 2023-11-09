<template>
  <header class="shadow-md">
    <!-- Barra de navegación con colores invertidos -->
    <nav class="bg-white text-gray-800 py-8">
      <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div class="relative flex h-16 items-center justify-between">
          <!-- Botón del menú móvil -->
          <button
            class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-700 hover:bg-gray-200 hover:text-gray-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-700 sm:hidden"
            @click="toggleMobileMenu"
          >
            <span class="absolute -inset-0.5"></span>
            <span class="sr-only">Abrir menú principal</span>
            <span v-if="!mobileMenuOpen" class="block h-6 w-6" aria-hidden="true">☰</span>
            <span v-else class="block h-6 w-6" aria-hidden="true">×</span>
          </button>

          <!-- Logo y botones de navegación -->
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <img
                class="h-[80px] w-auto mx-4"
                src="../assets/logo.png"
                alt="Tu Compañía"
              />
            </router-link>
            <div class="hidden sm:block">
              <router-link
                v-for="item in navigation"
                :key="item.name"
                :to="item.href"
                :class="[
                  'm-1 text-lg hover:bg-gray-200 hover:text-gray-800',
                  'rounded-md px-3 py-2 font-medium',
                  route.path === item.href ? 'bg-gray-200 text-gray-800' : ''
                ]"
              >
                {{ item.name }}
              </router-link>
            </div>
          </div>

          <!-- Menú de usuario -->
          <div class="relative" @click="toggleUserDropdown">
            <template v-if="isAuthenticated">
              <img
                class="h-12 w-12 rounded-full"
                :src="userProfileImageUrl"
                alt=""
              />
              <transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div
                  v-if="userDropdownOpen"
                  class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                >
                  <router-link to="/perfil" class="block px-4 py-2 text-lg text-gray-700">Tu Perfil</router-link>
                  <router-link to="/configuracion" class="block px-4 py-2 text-lg text-gray-700">Configuración</router-link>
                  <a href="#" class="block px-4 py-2 text-lg text-gray-700" @click="logout">Cerrar Sesión</a>
                </div>
              </transition>
            </template>
            <template v-else>
              <!-- Usuario no autenticado, muestra botones de inicio de sesión y registro -->
              <div class="hidden sm:block">
                <router-link to="/login" class="bg-blumine-400 text-white font-bold py-2 px-4 rounded mr-2">Iniciar Sesión</router-link>
                <router-link to="/register" class="border-2 border-blumine-400 text-blumine-400 font-bold py-2 px-4 rounded">Registrar</router-link>
              </div>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Menú móvil -->
    <div v-if="mobileMenuOpen" class="sm:hidden">
      <div class="flex flex-col p-4 z-5">
        <router-link
          v-for="item in navigation"
          :key="item.name"
          :class="[
            'text-lg text-center hover:bg-gray-200 w-full my-1 hover:text-gray-800',
            'rounded-md px-3 py-2 font-medium',
            route.path === item.href ? 'bg-gray-200 text-gray-800' : ''
          ]"
          :to="item.href"
        >
          {{ item.name }}
        </router-link>
      </div>
    </div>
  </header>
</template>


<script setup>
import { onMounted, watch, ref } from 'vue'; // Agregamos "ref" aquí

import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

const store = useStore();
let isAuthenticated = ref(false); // Cambiamos a ref() para asegurar la reactividad

const mobileMenuOpen = ref(false);
const userDropdownOpen = ref(false);
const userProfileImageUrl = ref('');

const route = useRoute();

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const toggleUserDropdown = () => {
  userDropdownOpen.value = !userDropdownOpen.value;
};

const checkAuthentication = () => {
  const token = store.state.access_token;
  console.log(token);
  if (token) {
    isAuthenticated.value = true; // Cambiamos el valor de isAuthenticated a través de .value
      // También podrías recuperar la URL de la imagen del perfil y asignarla a userProfileImageUrl aquí
  }
};

const logout = () => {
  store.dispatch('userLogout'); // Llama a la acción de cierre de sesión en Vuex
  userProfileImageUrl.value = '';
  isAuthenticated.value = false;
};

const navigation = [
  { name: 'home', href: '/', current: route.path === '/' },
  { name: 'Blog', href: '/blog', current: route.path === '/blog' },
  { name: 'About', href: '/about', current: route.path === '/about' },
];

onMounted(() => {
  console.log('on mounted');
  checkAuthentication();
});

watch(isAuthenticated, (newVal) => {
  if (!newVal) {
    userProfileImageUrl.value = '';
  }
});
</script>
