<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps<{
  credentials: { username: string; password: string } | null
}>()

interface Item {
  item_id: string
  name: string
  description?: string
  price?: number
  category?: string
  [key: string]: any
}

interface Category {
  category_name: string
  description?: string
  [key: string]: any
}

const items = ref<Item[]>([])
const categories = ref<Category[]>([])
const isLoading = ref(false)
const error = ref('')
const showAddModal = ref(false)
const editingItem = ref<Item | null>(null)

// Форма для добавления/редактирования товара
const form = ref({
  item_id: '',
  name: '',
  description: '',
  price: 0,
  category: ''
})

const apiHeaders = () => ({
  'Authorization': `Basic ${btoa(`${props.credentials?.username}:${props.credentials?.password}`)}`,
  'Content-Type': 'application/json'
})

const loadItems = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await fetch('http://localhost:8000/items', {
      headers: apiHeaders()
    })
    
    if (response.ok) {
      items.value = await response.json()
    } else {
      error.value = 'Ошибка загрузки товаров'
    }
  } catch (err) {
    error.value = 'Ошибка подключения к серверу'
  } finally {
    isLoading.value = false
  }
}

const loadCategories = async () => {
  try {
    const response = await fetch('http://localhost:8000/categories', {
      headers: apiHeaders()
    })
    
    if (response.ok) {
      categories.value = await response.json()
    }
  } catch (err) {
    console.error('Ошибка загрузки категорий:', err)
  }
}

const openAddModal = () => {
  form.value = {
    item_id: '',
    name: '',
    description: '',
    price: 0,
    category: ''
  }
  editingItem.value = null
  showAddModal.value = true
}

const openEditModal = (item: Item) => {
  form.value = { ...item }
  editingItem.value = item
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  editingItem.value = null
  form.value = {
    item_id: '',
    name: '',
    description: '',
    price: 0,
    category: ''
  }
}

const saveItem = async () => {
  if (!form.value.item_id.trim() || !form.value.name.trim()) {
    error.value = 'ID товара и название обязательны'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const url = editingItem.value 
      ? `http://localhost:8000/items/${editingItem.value.item_id}`
      : 'http://localhost:8000/items'
    
    const method = editingItem.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: apiHeaders(),
      body: JSON.stringify(form.value)
    })

    if (response.ok) {
      await loadItems()
      closeModal()
    } else {
      const errorData = await response.json()
      error.value = errorData.detail || 'Ошибка сохранения товара'
    }
  } catch (err) {
    error.value = 'Ошибка подключения к серверу'
  } finally {
    isLoading.value = false
  }
}

const deleteItem = async (itemId: string) => {
  if (!confirm(`Вы уверены, что хотите удалить товар с ID "${itemId}"?`)) {
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const response = await fetch(`http://localhost:8000/items/${itemId}`, {
      method: 'DELETE',
      headers: apiHeaders()
    })

    if (response.ok) {
      await loadItems()
    } else {
      error.value = 'Ошибка удаления товара'
    }
  } catch (err) {
    error.value = 'Ошибка подключения к серверу'
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadItems(), loadCategories()])
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h2 class="text-lg font-medium text-gray-900">Управление товарами</h2>
      <button
        @click="openAddModal"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Добавить товар
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

    <!-- Items list -->
    <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
      <div v-if="items.length === 0" class="text-center py-8 text-gray-500">
        Товары не найдены. Добавьте первый товар.
      </div>
      <ul v-else class="divide-y divide-gray-200">
        <li v-for="item in items" :key="item.item_id" class="px-6 py-4">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-3">
                <h3 class="text-sm font-medium text-gray-900">
                  {{ item.name }}
                </h3>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  ID: {{ item.item_id }}
                </span>
                <span v-if="item.category" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {{ item.category }}
                </span>
              </div>
              <p v-if="item.description" class="text-sm text-gray-500 mt-1">
                {{ item.description }}
              </p>
              <p v-if="item.price" class="text-sm text-green-600 mt-1 font-medium">
                Цена: {{ item.price }} ₽
              </p>
            </div>
            <div class="flex space-x-2">
              <button
                @click="openEditModal(item)"
                class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200"
              >
                Редактировать
              </button>
              <button
                @click="deleteItem(item.item_id)"
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
      <div class="relative top-10 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingItem ? 'Редактировать товар' : 'Добавить товар' }}
          </h3>
          
          <form @submit.prevent="saveItem" class="space-y-4">
            <div>
              <label for="item_id" class="block text-sm font-medium text-gray-700">
                ID товара
              </label>
              <input
                id="item_id"
                v-model="form.item_id"
                type="text"
                :disabled="!!editingItem"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm disabled:bg-gray-100"
                placeholder="Введите ID товара"
              />
            </div>
            
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">
                Название товара
              </label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Введите название товара"
              />
            </div>

            <div>
              <label for="category" class="block text-sm font-medium text-gray-700">
                Категория
              </label>
              <select
                id="category"
                v-model="form.category"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
                <option value="">Выберите категорию</option>
                <option v-for="category in categories" :key="category.category_name" :value="category.category_name">
                  {{ category.category_name }}
                </option>
              </select>
            </div>

            <div>
              <label for="price" class="block text-sm font-medium text-gray-700">
                Цена (₽)
              </label>
              <input
                id="price"
                v-model.number="form.price"
                type="number"
                min="0"
                step="0.01"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Введите цену"
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
                placeholder="Введите описание товара"
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
                {{ editingItem ? 'Сохранить' : 'Добавить' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>