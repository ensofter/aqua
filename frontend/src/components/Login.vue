<template>
  <AnimatedBackground />
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <form @submit.prevent="onLogin" class="bg-white p-8 rounded shadow-md w-80">
      <h2 class="text-2xl font-bold mb-6 text-center">Вход</h2>
      <div class="mb-4">
        <label class="block mb-1 text-gray-700">Логин</label>
        <input v-model="username" type="text" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring" required />
      </div>
      <div class="mb-6">
        <label class="block mb-1 text-gray-700">Пароль</label>
        <input v-model="password" type="password" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring" required />
      </div>
      <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition">Войти</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import AnimatedBackground from './AnimatedBackground.vue';

const username = ref('');
const password = ref('');
const router = useRouter();

function onLogin() {
  // Простая проверка (заглушка)
  if (username.value === 'admin' && password.value === 'admin') {
    localStorage.setItem('isAuth', 'true');
    router.push('/admin');
  } else {
    alert('Неверный логин или пароль');
  }
}
</script> 