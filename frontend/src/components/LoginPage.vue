<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  login: [credentials: { username: string; password: string }]
}>()

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')

const handleSubmit = async () => {
  if (!username.value || !password.value) {
    error.value = 'Заполните все поля'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    // Тестируем подключение к API с учетными данными
    const response = await fetch('http://localhost:8000/categories', {
      headers: {
        'Authorization': `Basic ${btoa(`${username.value}:${password.value}`)}`
      }
    })

    if (response.ok) {
      emit('login', { 
        username: username.value, 
        password: password.value 
      })
    } else {
      error.value = 'Неверный логин или пароль'
    }
  } catch (err) {
    error.value = 'Ошибка подключения к серверу'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">
    <div class="max-w-md w-full space-y-8 p-8">
      <div class="bg-white rounded-lg shadow-xl p-8">
        <div class="text-center">
          <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
            Вход в админ-панель
          </h2>
          <p class="mt-2 text-sm text-gray-600">
            Управление категориями и товарами
          </p>
        </div>
        
        <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Логин
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Введите логин"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Пароль
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Введите пароль"
            />
          </div>

          <div v-if="error" class="text-red-600 text-sm text-center">
            {{ error }}
          </div>

          <div>
            <button
              type="submit"
              :disabled="isLoading"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
                <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
              {{ isLoading ? 'Вход...' : 'Войти' }}
            </button>
          </div>
        </form>
        
        <div class="mt-6 text-center text-xs text-gray-500">
          <p>Для тестирования используйте:</p>
          <p>Логин: admin, Пароль: admin123</p>
        </div>
      </div>
    </div>
  </div>
</template>