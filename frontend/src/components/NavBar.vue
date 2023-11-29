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
            <!-- Ícono de menú móvil -->
            <span v-if="!mobileMenuOpen" class="block h-6 w-6" aria-hidden="true">☰</span>
            <span v-else class="block h-6 w-6" aria-hidden="true">×</span>
          </button>

          <!-- Logo y botones de navegación -->
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <!-- Logo -->
              <img
                class="h-[80px] w-auto mx-4"
                src="../assets/logo.png"
                alt="Tu Compañía"
              />
            </router-link>
            <!-- Enlaces de navegación -->
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
          <div class="relative">
            <template v-if="isAuthenticated">
              <!-- Mostrar información del usuario autenticado -->
              <div class="flex row items-center" @click="toggleUserDropdown">
                <!-- Imagen de perfil o ícono predeterminado -->
                <img v-if="userProfileImageUrl"
                  class="h-12 w-12 rounded-full m-2"
                  :src="'api/'+userProfileImageUrl"
                  alt=""
                />
                <div v-else>
                  <UserCircleIcon class="h-12 w-12 rounded-full m-2"/>
                </div>
                <!-- Nombre de usuario -->
                <p class="hidden sm:block xl:text-xl md:text-lg sm:text-md">{{ userName }}</p>
              </div>

              <!-- Menú desplegable del usuario -->
              <transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div v-if="userDropdownOpen" class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                  <!-- Enlaces del menú desplegable -->
                  <router-link to="/perfil" class="block px-4 py-2 text-lg text-gray-700">Tu Perfil</router-link>
                  <router-link to="/configuracion" class="block px-4 py-2 text-lg text-gray-700">Configuración</router-link>
                  <a href="#" class="block px-4 py-2 text-lg text-gray-700" @click="logout">Cerrar Sesión</a>
                </div>
              </transition>
            </template>
            <template v-else>
              <!-- Usuario no autenticado, muestra botones de inicio de sesión y registro -->
              <div class="hidden sm:block">
                <router-link to="/login" class="bg-blumine-400 text-white font-bold py-2 px-4 rounded mr-2 text-sm md:text-md lg:text-lg ">Iniciar Sesión</router-link>
                <router-link to="/register" class="border-2 border-blumine-400 text-blumine-400 font-bold py-2 px-4 rounded text-sm md:text-md lg:text-lg ">Registrar</router-link>
              </div>
              <!-- Ícono de usuario para dispositivos móviles -->
              <div class="sm:hidden" @click="toggleUserDropdown">
                <UserIcon class="h-12 w-12 m-2" />
              </div>
              <!-- Menú desplegable del usuario para dispositivos móviles -->
              <transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div v-if="userDropdownOpen" class="sm:hidden absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                  <!-- Enlaces del menú desplegable para dispositivos móviles -->
                  <router-link to="/login" class="block px-4 py-2 text-lg text-gray-700">Iniciar Sesión</router-link>
                  <router-link to="/register" class="block px-4 py-2 text-lg text-gray-700">Registrar</router-link>
                </div>
              </transition>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Menú móvil -->
    <div v-if="mobileMenuOpen" class="sm:hidden">
      <div class="flex flex-col p-4 z-5">
        <!-- Enlaces de navegación para dispositivos móviles -->
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
import { fetchData } from '@/util/fetchData.js';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
import { UserCircleIcon, UserIcon } from '@heroicons/vue/24/solid';

// Uso de store y refs
const store = useStore();
let isAuthenticated = ref(false); // Cambiamos a ref() para asegurar la reactividad
const mobileMenuOpen = ref(false);
const userDropdownOpen = ref(false);
const userProfileImageUrl = ref('');
const userName = ref('');

// Uso de ruta actual
const route = useRoute();

// Funciones para manejar eventos y lógica
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const toggleUserDropdown = () => {
  userDropdownOpen.value = !userDropdownOpen.value;
};

const checkAuthentication = () => {
  const token = store.state.access_token;
  if (token) {
    isAuthenticated.value = true; 
    fetchUserData();
  }
};

const fetchUserData = async () => {
  try {
    const url = '/user/navbar/';
    const data = await fetchData(url);
    userProfileImageUrl.value = data.profile_image;
    userName.value = data.name;
  } catch (error) {
    console.error('Error al obtener datos del usuario:', error);
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

// Verificación de autenticación al cargar el componente
onMounted(() => {
  checkAuthentication();
});

// Observador para limpiar la imagen de perfil si el usuario no está autenticado
watch(isAuthenticated, (newVal) => {
  if (!newVal) {
    userProfileImageUrl.value = '';
  }
});
</script>
