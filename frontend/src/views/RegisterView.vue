<template>
  <div class="flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
    <form @submit.prevent="handleSubmit">
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-semibold leading-7 text-gray-900">Registrarse</h2>

          <div class="mt-10 grid grid-cols-1 gap-x-6  sm:grid-cols-4">
            <div class="sm:col-span-4">
              <Field id="photo" label="Imagen de perfil">
                <ProfileImageInput v-model="form.fields.profile_image" :initials="form.fields.initials" />
              </Field>
            </div>
            <div class="sm:col-span-2">
              <Field id="firstName" required label="Nombre">
                <Input v-model="form.fields.firstName" autocomplete="given-name" />
              </Field>
            </div>

            <div class="sm:col-span-2">
              <Field id="lastName" required label="Apellido">
                <Input v-model="form.fields.lastName" autocomplete="family-name" />
              </Field>
            </div>

            <div class="sm:col-span-4">
              <Field id="email" label="Correo electrónico" required :error="form.error?.validation?.email">
                <Input v-model="form.fields.email" type="email" autocomplete="email" />

              </Field>

            </div>
            <div class="sm:col-span-4">
              <Field id="ocupacion" label="Ocupacion">
                <Combobox :load-options="loadRoles" v-model="form.fields.role" :create-option="createRole" />
              </Field>
            </div>

            <div class="sm:col-span-4">
              <Field id="password" label="Contraseña" required help="Mínimo 8 caracteres, una mayúscula y un número">
                <PasswordInput v-model="form.fields.password" autocomplete="new-password" />
              </Field>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 flex items-center justify-end gap-x-3 ">
        <Button intent="ghost" @click="volver">Volver</Button>
        <Button type="submit" class="!mr-0" :loading="form.processing">Registrar</Button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { PhotoIcon, UserCircleIcon } from '@heroicons/vue/24/solid'
import {  watch } from 'vue';
import { useRouter } from 'vue-router';
import { Field, Input, PasswordInput, Button, ProfileImageInput, Combobox } from '@/components/input_components';
import useForm from '@/composables/useForm';
import { userService } from '@/services';

const router = useRouter();

const form = useForm({
  firstName: '',
  lastName: '',
  initials: '',
  email: '',
  password: '',
  role: 0,
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
        })
      );
    });
}




function createRole(option, setSelected) {
  fetch("http://localhost:8000/addRole/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      description: option.label, // Envía la descripción del nuevo rol al backend
    }),
  })
    .then(response => response.json())
    .then(role => {
      setSelected({
        value: role.id,
        label: role.description
      });
    });
}


async function handleSubmit() {
  await form.submit(async fields => {
    await userService.createUser(fields);
    await router.push("/login"); 
  });
}


watch(() => [form.fields.firstName, form.fields.lastName], ([newFirstName, newLastName]) => {
  const newFirstInitial = newFirstName ? newFirstName.charAt(0).toUpperCase() : '';
  const newLastInitial = newLastName ? newLastName.charAt(0).toUpperCase() : '';
  const newInitials = `${newFirstInitial}${newLastInitial}`;

  if (newInitials !== form.fields.initials) {
    form.fields.initials = newInitials;
  }
}, { deep: true });


function volver() {
  router.go(-1)
}

</script>
