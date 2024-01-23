<template>
  <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
    <form @submit="submitForm" ref="registrationForm" enctype="multipart/form-data">
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-semibold leading-7 text-gray-900">Registrarse</h2>

          <div class="col-span-full">
            <label for="photo" class="block text-sm font-medium leading-6 text-gray-900">imagen de perfil</label>
            <div class="mt-2 flex items-center gap-x-3">
              <img v-if="fotoUrl" class="w-[66px] aspect-square rounded-full" :src="fotoUrl" alt="" />
              <UserCircleIcon v-else class="w-[66px] aspect-square text-gray-300" aria-hidden="true" />
              <input type="file" accept="image/*" ref="fileInput" style="display: none" @change="handleFileChange" />
              <button type="button" @click="openFileInput"
                class="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">Cambiar</button>
            </div>
          </div>

          <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-4">
            <div class="sm:col-span-2">
              <label for="firstName" class="block text-sm font-medium leading-6 text-gray-900">Nombre <span
                  class="text-red-600">*</span></label>
              <div class="mt-2">
                <input v-model="user.firstName" type="text" name="firstName" id="firstName" autocomplete="given-name"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6"
                  required pattern="[A-Za-z ]{1,32}" />
              </div>
            </div>

            <div class="sm:col-span-2">
              <label for="lastName" class="block text-sm font-medium leading-6 text-gray-900">Apellido <span
                  class="text-red-600">*</span></label>
              <div class="mt-2">
                <input v-model="user.lastName" type="text" name="lastName" id="lastName" autocomplete="family-name"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6"
                  required pattern="[A-Za-z ]{1,32}" />
              </div>
            </div>

            <div class="sm:col-span-4">
              <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email <span
                  class="text-red-600">*</span></label>
              <div class="mt-2">
                <input v-model="user.email" id="email" name="email" type="email" autocomplete="email" inputmode="email"
                  maxlength="254" autocapitalize="off" spellcheck="false" autocorrect="off"
                  title="Email: ejemplo@dominio.com"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6"
                  required />
              </div>
            </div>
            <div class="sm:col-span-4">
              <label for="ocupacion" class="block text-sm font-medium leading-6 text-gray-900">Ocupacion <span
                  class="text-red-600">*</span></label>
              <div class="mt-2">
                <Combobox :load-options="loadRoles" v-model="role" :create-option="createRole" />
              </div>
            </div>
            <div class="sm:col-span-4">
              <label for="ocupacion" class="block text-sm font-medium leading-6 text-gray-900">contraseña <span
                  class="text-red-600">*</span></label>
              <div class="mt-2">
                <input v-model="user.password" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                  title="Debe contener al menos un numero, una mayuscula y una minuscula, y debe terner al menos 8 o mas caracteres"
                  id="password" name="password" type="password" autocomplete="new-password" required class="block w-full rounded-md border-0 p-1.5 text-gray-900 shadow-sm ring-1 
                    ring-inset ring-gray-300 placeholder:text-gray-400 
                    focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6 outline-none">
              </div>
            </div>
            <div class="sm:col-span-4">
              <label for="ocupacion" class="block text-sm font-medium leading-6 text-gray-900">confirmar contraseña <span
                  class="text-red-600">*</span></label>
              <div class="mt-2">
                <input v-model="passwordConfirm" id="passwordConfirm" name="passwordConfirm" type="password"
                  autocomplete="new-password" required class="block w-full rounded-md border-0 p-1.5 text-gray-900 shadow-sm ring-1 
                    ring-inset ring-gray-300 placeholder:text-gray-400 
                    focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6 outline-none">
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 flex items-center justify-end gap-x-6">
        <button type="button" class="text-sm font-semibold leading-6 rounded-md px-2 py-1 text-gray-900"
          @click="volver">Volver</button>
        <button type="submit"
          class="rounded-md bg-blumine-400 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blumine-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blumine-500">
          Registrar
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { PhotoIcon, UserCircleIcon } from '@heroicons/vue/24/solid'
import { ref } from 'vue'
import axios from "axios";
import { useRouter } from 'vue-router';
import { getAPI } from '../services/axiosConfig';
import Combobox from '@/components/Combobox.vue';

const route = useRouter();
const role = ref()
const passwordConfirm = ref()
const user = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  foto: null
});

function loadRoles(query, setOptions) {
  fetch("http://localhost:8000/roles/?description=" + query)
    .then(response => response.json())
    .then(results => {
      setOptions(
        results.map(role => {
          return {
            value: role.id,
            label: role.description
          }
        }))
    })
}

function createRole(option, setSelected) {
  fetch("http://localhost:8000/addRole/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      description: option.label,
    }),
  })
    .then(response => response.json())
    .then(role => {
      setSelected({
        value: role.id,
        label: role.description,
      })
    })
}

const fotoUrl = ref(null);
const fileInput = ref(null);

const openFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};

function volver(){
  route.go(-1)
}

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    fotoUrl.value = URL.createObjectURL(file);
    user.value.foto = file
  }
};

const submitForm = async (event) => {
  event.preventDefault();
  if (user.value.password !== passwordConfirm.value) {
    alert("Las contraseñas no coinciden");
    return;
  }
  // Accede a los valores del formulario utilizando las variables de datos
  const formData = new FormData();
  formData.append("name", user.value.firstName + ' ' + user.value.lastName);
  formData.append("email", user.value.email);
  formData.append("password", user.value.password);
  formData.append("role", role.value.value);
  formData.append("profile_image", user.value.foto)

  // Convierte los datos a JSON y muestra en consola
  try {
    for (var pair of formData.entries()) {
      console.log(pair[0] + ', ' + pair[1]);
    }
    // Realiza la solicitud POST utilizando la instancia de axios personalizada

    const response = await axios.post("/api/register/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    // Verifica si la respuesta es exitosa
    if (response.status === 200) {
      // Éxito: muestra la respuesta del servidor
      console.log("Registro exitoso:", response.data);
      // Puedes redirigir al usuario a otra página o realizar alguna acción adicional aquí
    } else {
      // Error: muestra el mensaje de error del servidor
      console.error("Error en el registro:", response.data);
      // Puedes manejar el error de alguna manera (por ejemplo, mostrar un mensaje al usuario)
    }
  } catch (error) {
    console.error("Error en la solicitud:", error);
    // Puedes manejar el error de alguna manera (por ejemplo, mostrar un mensaje al usuario)
  }
  // También puedes enviar los datos al servidor para procesamiento aquí
}
</script>


