<template>
  <header class="shadow-md">
    <!-- Barra de búsqueda con colores invertidos -->
    <nav class="bg-white text-gray-800 py-8">
      <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 flex row justify-between items-center">
        <div class="flex h-16 items-center justify-between">
          <!-- Logo y barra de búsqueda -->
          <div class="flex items-center justify-center">
            <router-link to="/" class="flex items-center justify-center mx-auto">
              <!-- Logo -->
              <img class="h-[80px] w-auto mx-4" src="../assets/logo.png" alt="Tu Compañía" />
            </router-link>
            <!-- Barra de búsqueda -->

            <div class='hidden md:block max-w-md mx-auto'>
              <SearchBar />
            </div>
          </div>

        </div>
        <!-- Menú de usuario -->
        <router-link to="/search" class="ml-auto block md:hidden">
              <!-- Logo -->
              <MagnifyingGlassIcon class="cursor-pointer h-10 w-10 rounded-full m-2" />
            </router-link>
        <div class="relative">
          
            
       
          <template v-if="isAuthenticated">
            <!-- Mostrar información del usuario autenticado -->
            <div class="flex row items-center">
              <div>
                <router-link to="/crear-post">
                  <button
                    class="flex whitespace-nowrap font-bold text-lg items-center justify-center bg-blumine-400 text-white  rounded-md pl-3 pr-4 py-2 mr-2">
                    <PlusSmallIcon class="w-6" />new post
                  </button>
                </router-link>
              </div>
              <!-- Imagen de perfil o ícono predeterminado -->
              <img v-if="userProfileImageUrl" @click="toggleUserDropdown"
                class="cursor-pointer h-12 w-12 rounded-full m-2" :src="'api' + userProfileImageUrl" alt="" />
              <div v-else>
                <UserCircleIcon class="cursor-pointer h-12 w-12 rounded-full m-2 text-gray-300"
                  @click="toggleUserDropdown" />
              </div>
              <!-- Nombre de usuario -->
              <p class="hidden sm:block xl:text-xl md:text-lg sm:text-md cursor-pointer" @click="toggleUserDropdown">
                {{ userName }}
              </p>
            </div>
            <!-- Menú desplegable del usuario -->
            <transition enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95">
              <div v-if="userDropdownOpen"
                class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <!-- Enlaces del menú desplegable -->
                <router-link to="/perfil" class="block px-4 py-2 text-lg text-gray-700" @click="toggleUserDropdown">
                  Tu Perfil
                </router-link>
                <router-link to="/configuracion" class="block px-4 py-2 text-lg text-gray-700"
                  @click="toggleUserDropdown">
                  Mis Publicaciones
                </router-link>
                <a href="#" class="block px-4 py-2 text-lg text-gray-700" @click="logout">
                  Cerrar Sesión
                </a>
              </div>
            </transition>
          </template>
          <template v-else>
            <!-- Usuario no autenticado, muestra botones de inicio de sesión y registro -->
            <div class="hidden md:block">
              <router-link to="/login"
                class="bg-blumine-400 text-white font-bold py-2 px-4 rounded mr-2 text-sm md:text-md lg:text-lg">
                Iniciar Sesión
              </router-link>
              <router-link to="/register"
                class="border-2 border-blumine-400 text-blumine-400 font-bold py-2 px-4 rounded text-sm md:text-md lg:text-lg">
                Registrar
              </router-link>
            </div>
            <!-- Ícono de usuario para dispositivos móviles -->
            <div class="md:hidden" @click="toggleUserDropdown">
              <UserIcon class="h-10 w-10 m-2" />
            </div>
            <!-- Menú desplegable del usuario para dispositivos móviles -->
            <transition enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95">
              <div v-if="userDropdownOpen"
                class="md:hidden absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <!-- Enlaces del menú desplegable para dispositivos móviles -->
                <router-link to="/login" class="block px-4 py-2 text-lg text-gray-700" @click="toggleUserDropdown">
                  Iniciar Sesión
                </router-link>
                <router-link to="/register" class="block px-4 py-2 text-lg text-gray-700" @click="toggleUserDropdown">
                  Registrar
                </router-link>
              </div>
            </transition>
          </template>
        </div>
      </div>


    </nav>
  </header>
</template>

<script setup>
import { onMounted, watch, ref, computed } from 'vue';
import { fetchData } from '@/util/apiUtils';
import store from '@/store'; // Ajusta la ruta según sea necesario
import { UserCircleIcon, UserIcon, PlusIcon, PlusSmallIcon,MagnifyingGlassIcon } from '@heroicons/vue/24/solid';
import SearchBar from '@/components/input_components/SearchBar.vue';


const userDropdownOpen = ref(false);
const userProfileImageUrl = ref('');

const userName = ref('');


const isAuthenticated = computed(() => {
  return store.getters.validatedAccessToken !== null;
});


const toggleUserDropdown = () => {
  userDropdownOpen.value = !userDropdownOpen.value;
};

const checkAuthentication = () => {
  if (isAuthenticated.value) {
    fetchUserData();
  }
};

const fetchUserData = async () => {
  try {
    const url = '/user/navbar/';
    const data = await fetchData(url,undefined,true);
    userProfileImageUrl.value = data.profile_image;
    userName.value = data.name;
  } catch (error) {
    console.error('Error al obtener datos del usuario:', error);
  }
};

const logout = () => {
  store.dispatch('userLogout');
  userProfileImageUrl.value = '';
};

onMounted(() => {
  checkAuthentication();
});

watch(isAuthenticated, (newVal) => {
  if (!newVal) {
    userProfileImageUrl.value = '';
    toggleUserDropdown();
  }
});


</script>