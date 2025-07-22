<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LoginPage from './components/LoginPage.vue'
import AdminPanel from './components/AdminPanel.vue'

const isAuthenticated = ref(false)
const credentials = ref<{ username: string; password: string } | null>(null)

// Проверяем сохраненные учетные данные при загрузке
onMounted(() => {
  const saved = localStorage.getItem('admin_credentials')
  if (saved) {
    try {
      credentials.value = JSON.parse(saved)
      isAuthenticated.value = true
    } catch (e) {
      localStorage.removeItem('admin_credentials')
    }
  }
})

const handleLogin = (loginCredentials: { username: string; password: string }) => {
  credentials.value = loginCredentials
  isAuthenticated.value = true
  localStorage.setItem('admin_credentials', JSON.stringify(loginCredentials))
}

const handleLogout = () => {
  credentials.value = null
  isAuthenticated.value = false
  localStorage.removeItem('admin_credentials')
}
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <LoginPage 
      v-if="!isAuthenticated" 
      @login="handleLogin"
    />
    <AdminPanel 
      v-else 
      :credentials="credentials"
      @logout="handleLogout"
    />
  </div>
</template>

<style scoped>
/* Глобальные стили можно добавить здесь */
</style>
