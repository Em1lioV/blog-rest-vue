<template>
  <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
    <form @submit="submitForm" ref="registrationForm" enctype="multipart/form-data">
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-semibold leading-7 text-gray-900">Registrarse</h2>

          <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-4">
            <div class="sm:col-span-4">
              <Field id="photo" label="Imagen de perfil">
                <ProfileImageInput v-model="user.profile_image" :name="user.firstName" :initials="initials" />
              </Field>
            </div>
            <div class="sm:col-span-2">
              <Field id="firstName" required label="Nombre">
                <Input v-model="user.firstName" autocomplete="given-name" />
              </Field>
            </div>

            <div class="sm:col-span-2">
              <Field id="lastName" required label="Apellido">
                <Input v-model="user.lastName" autocomplete="family-name" />
              </Field>
            </div>

            <div class="sm:col-span-4">
              <Field id="email" label="Correo electrónico" required>
                <Input v-model="user.email" type="email" autocomplete="email" />
              </Field>

            </div>
            <div class="sm:col-span-4">
              <Field id="ocupacion" label="Ocupacion">
                <Combobox :load-options="loadRoles" v-model="role" :create-option="createRole" />
              </Field>


            </div>

            <div class="sm:col-span-4">
              <Field id="password" label="Contraseña" required>
                <PasswordInput v-model="user.password" autocomplete="new-password" />
              </Field>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 flex items-center justify-end gap-x-3 ">
          <Button intent="ghost" @click="volver" >Volver</Button>
          <Button type="submit" class="!mr-0">Registrar</Button>
        
      </div>
    </form>
  </div>
</template>

<script setup>
import { PhotoIcon, UserCircleIcon } from '@heroicons/vue/24/solid'
import { computed, ref } from 'vue'
import axios from "axios";
import { useRouter } from 'vue-router';
import { getAPI } from '../services/axiosConfig';
import Combobox from '@/components/Combobox.vue';
import { Field, Input, PasswordInput,Button } from '@/components/input_components';
import ProfileImageInput from '@/components/input_components/ProfileImageInput.vue';

const route = useRouter();
const role = ref()
const user = ref({
  firstName: '',
  lastName: '',
  initials: '',
  email: '',
  password: '',
  profile_image: null
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

function volver() {
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

const initials = computed(() =>
  user.value.firstName && user.value.lastName
    ? user.value.firstName.charAt(0) + user.value.lastName.charAt(0)
    : '' 
);
</script>


