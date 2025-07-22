<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps<{
  credentials: { username: string; password: string } | null
}>()

interface Category {
  category_name: string
  description?: string
  [key: string]: any
}

const categories = ref<Category[]>([])
const isLoading = ref(false)
const error = ref('')
const showAddModal = ref(false)
const editingCategory = ref<Category | null>(null)

// Форма для добавления/редактирования категории
const form = ref({
  category_name: '',
  description: ''
})

const apiHeaders = () => ({
  'Authorization': `Basic ${btoa(`${props.credentials?.username}:${props.credentials?.password}`)}`,
  'Content-Type': 'application/json'
})

const loadCategories = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await fetch('http://localhost:8000/categories', {
      headers: apiHeaders()
    })
    
    if (response.ok) {
      categories.value = await response.json()
    } else {
      error.value = 'Ошибка загрузки категорий'
    }
  } catch (err) {
    error.value = 'Ошибка подключения к серверу'
  } finally {
    isLoading.value = false
  }
}

const openAddModal = () => {
  form.value = { category_name: '', description: '' }
  editingCategory.value = null
  showAddModal.value = true
}

const openEditModal = (category: Category) => {
  form.value = { ...category }
  editingCategory.value = category
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  editingCategory.value = null
  form.value = { category_name: '', description: '' }
}

const saveCategory = async () => {
  if (!form.value.category_name.trim()) {
    error.value = 'Название категории обязательно'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const url = editingCategory.value 
      ? `http://localhost:8000/categories/${editingCategory.value.category_name}`
      : 'http://localhost:8000/categories'
    
    const method = editingCategory.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: apiHeaders(),
      body: JSON.stringify(form.value)
    })

    if (response.ok) {
      await loadCategories()
      closeModal()
    } else {
      const errorData = await response.json()
      error.value = errorData.detail || 'Ошибка сохранения категории'
    }
  } catch (err) {
    error.value = 'Ошибка подключения к серверу'
  } finally {
    isLoading.value = false
  }
}

const deleteCategory = async (categoryName: string) => {
  if (!confirm(`Вы уверены, что хотите удалить категорию "${categoryName}"?`)) {
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const response = await fetch(`http://localhost:8000/categories/${categoryName}`, {
      method: 'DELETE',
      headers: apiHeaders()
    })

    if (response.ok) {
      await loadCategories()
    } else {
      error.value = 'Ошибка удаления категории'
    }
  } catch (err) {
    error.value = 'Ошибка подключения к серверу'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h2 class="text-lg font-medium text-gray-900">Управление категориями</h2>
      <button
        @click="openAddModal"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Добавить категорию
      </button>
    </div>

    <!-- Error message -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
      <div class="text-sm text-red-600">{{ error }}</div>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="flex justify-center py-8">
      <svg class="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <!-- Categories list -->
    <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
      <div v-if="categories.length === 0" class="text-center py-8 text-gray-500">
        Категории не найдены. Добавьте первую категорию.
      </div>
      <ul v-else class="divide-y divide-gray-200">
        <li v-for="category in categories" :key="category.category_name" class="px-6 py-4">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <h3 class="text-sm font-medium text-gray-900">
                {{ category.category_name }}
              </h3>
              <p v-if="category.description" class="text-sm text-gray-500 mt-1">
                {{ category.description }}
              </p>
            </div>
            <div class="flex space-x-2">
              <button
                @click="openEditModal(category)"
                class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200"
              >
                Редактировать
              </button>
              <button
                @click="deleteCategory(category.category_name)"
                class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200"
              >
                Удалить
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingCategory ? 'Редактировать категорию' : 'Добавить категорию' }}
          </h3>
          
          <form @submit.prevent="saveCategory" class="space-y-4">
            <div>
              <label for="category_name" class="block text-sm font-medium text-gray-700">
                Название категории
              </label>
              <input
                id="category_name"
                v-model="form.category_name"
                type="text"
                :disabled="!!editingCategory"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm disabled:bg-gray-100"
                placeholder="Введите название категории"
              />
            </div>
            
            <div>
              <label for="description" class="block text-sm font-medium text-gray-700">
                Описание (необязательно)
              </label>
              <textarea
                id="description"
                v-model="form.description"
                rows="3"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Введите описание категории"
              ></textarea>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Отмена
              </button>
              <button
                type="submit"
                :disabled="isLoading"
                class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {{ editingCategory ? 'Сохранить' : 'Добавить' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>