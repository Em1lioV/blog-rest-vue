<template>
  <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
    <form @submit="submitForm" ref="registrationForm">
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-semibold leading-7 text-gray-900">Personal Information</h2>
          <p class="mt-1 text-sm leading-6 text-gray-500">Use a permanent address where you can receive mail.</p>

          <div class="col-span-full">
            <label for="photo" class="block text-sm font-medium leading-6 text-gray-900">Photo</label>
            <div class="mt-2 flex items-center gap-x-3">
              <img v-if="fotoUrl" class="h-12 w-12 rounded-full" :src="fotoUrl" alt="" />
              <UserCircleIcon v-else class="h-12 w-12 text-gray-300" aria-hidden="true" />
              <input type="file" accept="image/*" ref="fileInput" style="display: none" @change="handleFileChange" />
              <button type="button" @click="openFileInput" class="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">Change</button>
            </div>
          </div>

          <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
            <div class="sm:col-span-3">
              <label for="first-name" class="block text-sm font-medium leading-6 text-gray-900">First name</label>
              <div class="mt-2">
                <input type="text" name="first-name" id="first-name" autocomplete="given-name"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6" required />
              </div>
            </div>

            <div class="sm:col-span-3">
              <label for="last-name" class="block text-sm font-medium leading-6 text-gray-900">Last name</label>
              <div class="mt-2">
                <input type="text" name="last-name" id="last-name" autocomplete="family-name"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6" required />
              </div>
            </div>

            <div class="sm:col-span-4">
              <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
              <div class="mt-2">
                <input id="email" name="email" type="email" autocomplete="email"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6" required />
              </div>
            </div>
            <div class="sm:col-span-4">
              <label for="ocupacion" class="block text-sm font-medium leading-6 text-gray-900">Occupation</label>
              <div class="mt-2">
                <Combobox :load-options="loadRoles" v-model="role" :create-option="createRole" required />
              </div>
            </div>
            <div class="sm:col-span-4">
              <label for="ocupacion" class="block text-sm font-medium leading-6 text-gray-900">contraseña</label>
              <div class="mt-2">
                        <input v-model="password" id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 p-1.5 text-gray-900 shadow-sm ring-1 
                    ring-inset ring-gray-300 placeholder:text-gray-400 
                    focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6 outline-none">
              </div>
            </div>
            <div class="sm:col-span-4">
              <label for="ocupacion" class="block text-sm font-medium leading-6 text-gray-900">confirmar contraseña</label>
              <div class="mt-2">
                        <input v-model="password" id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 p-1.5 text-gray-900 shadow-sm ring-1 
                    ring-inset ring-gray-300 placeholder:text-gray-400 
                    focus:ring-2 focus:ring-inset focus:ring-blumine-400 sm:text-sm sm:leading-6 outline-none">
              </div>
            </div>
        </div>
        </div>
      </div>

      <div class="mt-6 flex items-center justify-end gap-x-6">
        <button type="button" class="text-sm font-semibold leading-6 rounded-md px-2 py-1 text-gray-900" @click="resetForm">Cancel</button>
        <button type="submit" class="rounded-md bg-blumine-400 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blumine-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blumine-500">
          Save
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { PhotoIcon, UserCircleIcon } from '@heroicons/vue/24/solid'
import { ref } from 'vue'
import Combobox from '@/components/Combobox.vue';

const role = ref()
const user = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: ''
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
const formDataJson = ref(null);

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    fotoUrl.value = URL.createObjectURL(file);
  }
};

const submitForm = (event) => {
  event.preventDefault();

  // Accede a los valores del formulario utilizando las variables de datos
  const data = {
    role: role.value,
    fotoUrl: fotoUrl.value,
    // Agrega aquí los otros campos del formulario
  };

  // Convierte los datos a JSON y muestra en consola
  const jsonData = JSON.stringify(data, null, 2);
  console.log(jsonData);
  // También puedes enviar los datos al servidor para procesamiento aquí
}
</script>


