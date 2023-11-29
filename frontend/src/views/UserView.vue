<template>
    <div>
      <h2>Datos del Usuario</h2>
      <div v-if="userData">
        <p><strong>Nombre de usuario:</strong> {{ userData.name }}</p>
        <p><strong>Correo electrónico:</strong> {{ userData.email }}</p>
        <p><strong>ocupacion:</strong> {{ userData.role_description }}</p>
        <img  :src="'/api/' + userData.profile_image" alt="">
        <!-- Otros campos de usuario -->
      </div>
      <div v-else>
        <p>Cargando...</p>
        <p >No se ha iniciado sesión o ha ocurrido un error.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { fetchData } from '@/util/fetchData.js';
  
  const userData = ref(null);
  
  onMounted(async () => {
    try {
      const url = 'user/';
      const data = await fetchData(url);
      userData.value = data;
    } catch (error) {
      // Manejo de errores
      console.error('Error al obtener datos del usuario:', error);
    }
  });
  </script>
  