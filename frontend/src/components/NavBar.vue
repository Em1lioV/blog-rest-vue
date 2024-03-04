<template>
  <header class="shadow-md">
    <nav
      class="bg-white text-gray-800 py-8 px-4 mx-auto lg:max-w-4xl xl:max-w-6xl flex row justify-between items-center">
      <div class="flex h-16 items-center justify-between">

        <div class="flex items-center justify-center">
          <router-link to="/" class="flex items-center justify-center mx-auto">

            <img class="h-[80px] w-auto mx-4" src="../assets/logo.png" alt="Tu Compañía" />
          </router-link>

          <div class="hidden md:flex max-w-md mx-auto items-center">
            <Field id="search" :BottomSlot="false">
              <SearchBar />
            </Field>
          </div>
        </div>
      </div>


      <router-link to="/search" class="ml-auto block md:hidden">

        <MagnifyingGlassIcon class="cursor-pointer h-10 w-10 rounded-full m-2" />
      </router-link>

      <div class="relative">
        <template v-if="isAuthenticated">
          <div class="flex row items-center">
            <div class="hidden md:inline-block ml-2">
              <Button to="/crear-post" :leftICon="PencilSquareIcon()" size="lg">Escribir</Button>
            </div>


            <Dropdown :options="dropdownOptions" v-if="user">
              <span class="cursor-pointer mx-3 flex items-center">
                <Avatar :src="user.profile_image" :name="user.fullname" :initials="user.initials" />
              </span>

              <p class="hidden sm:block xl:text-xl text-lg sm:text-md cursor-pointer" @click="toggleUserDropdown">
                {{ user.fullname }}
              </p>
            </Dropdown>
          </div>
        </template>

        <template v-else>
          <div class="hidden md:block">
            <Button to="/login">Iniciar Sesión</Button>
            <Button to="/register" ring>Registrar</Button>
          </div>
          <Dropdown :options="mobileDropdownOptions" class="md:hidden">
            <UserCircleIcon class="h-10 w-10 m-2" />
          </Dropdown>
        </template>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import store from "@/store";
import { UserCircleIcon, PencilSquareIcon, MagnifyingGlassIcon} from "@heroicons/vue/24/solid";
import { Field, SearchBar, Button } from "./input_components";
import { Avatar, Dropdown } from "./"
import { userService } from "@/services";

const user = ref({});
const isAuthenticated = ref(false);

const logout = () => {
  store.dispatch("userLogout");
};

const dropdownOptions = computed(() => {
  if (!user) return [];
  return [
    {
      label: "Escribir",
      to: "/crear-post",
      className:
        "md:hidden px-4 py-2 text-xl text-white bg-blumine-400 hover:!bg-blumine-500",
    },
    { label: "Tu Perfil", to: `/profile/${user.value.id}` },
    { label: "Mis Publicaciones", to: "/me/stories" },
    { separator: true },
    { label: "Cerrar Sesión", onClick: logout, className: "text-red-500" },
  ];
});

const checkAuthentication = () => {
  if (store.state.access_token) {
    fetchUserData();
    isAuthenticated.value = true;
  }
};

const fetchUserData = async () => {
  try {
    const responseUser = await userService.getUserPartial();

    user.value = responseUser;
  } catch (error) {
    console.error("Error al obtener datos del usuario:", error);
  }
};

const mobileDropdownOptions = [
  { label: "Iniciar Sesión", to: "/login" },
  { label: "Registrar", to: "/register" },
];

checkAuthentication();

watch(
  () => store.state.access_token,
  (newAccessToken) => {
    isAuthenticated.value = !!newAccessToken;

    if (!isAuthenticated.value) {
      user.value = {};
    }
  }
);
</script>
