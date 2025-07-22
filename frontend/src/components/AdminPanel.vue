<script setup lang="ts">
import { ref } from 'vue'
import CategoriesTab from './CategoriesTab.vue'
import ItemsTab from './ItemsTab.vue'

const props = defineProps<{
  credentials: { username: string; password: string } | null
}>()

const emit = defineEmits<{
  logout: []
}>()

const activeTab = ref('categories')

const handleLogout = () => {
  emit('logout')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900">
              Админ-панель телеграм бота
            </h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-500">
              Вошли как: {{ credentials?.username }}
            </span>
            <button
              @click="handleLogout"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Выйти
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Navigation Tabs -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex space-x-8">
          <button
            @click="activeTab = 'categories'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === 'categories'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Категории
          </button>
          <button
            @click="activeTab = 'items'"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === 'items'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            Товары
          </button>
        </div>
      </div>
    </nav>

    <!-- Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <CategoriesTab 
          v-if="activeTab === 'categories'"
          :credentials="credentials"
        />
        <ItemsTab 
          v-if="activeTab === 'items'"
          :credentials="credentials"
        />
      </div>
    </main>
  </div>
</template>