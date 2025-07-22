<template>
  <div class="min-h-screen bg-gray-50">
    <div class="bg-white shadow p-4 flex items-center justify-between">
      <h1 class="text-2xl font-bold">Админ-панель</h1>
      <button @click="logout" class="bg-red-500 text-white px-4 py-1 rounded">Выйти</button>
    </div>
    <div class="flex justify-center mt-8">
      <button :class="tabClass('categories')" @click="activeTab = 'categories'">Категории</button>
      <button :class="tabClass('products')" @click="activeTab = 'products'">Товары</button>
    </div>
    <div class="mt-8 max-w-2xl mx-auto">
      <Categories v-if="activeTab === 'categories'" />
      <Products v-else />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Categories from './Categories.vue';
import Products from './Products.vue';

const activeTab = ref<'categories' | 'products'>('categories');
const router = useRouter();

function logout() {
  localStorage.removeItem('isAuth');
  router.push('/login');
}

function tabClass(tab: 'categories' | 'products') {
  return [
    'px-4 py-2 mx-2 rounded',
    activeTab.value === tab ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700',
  ];
}
</script> 