<script setup>
import { ref, onMounted } from 'vue'
import { getProperties, createProperty } from '../api/properties'
import PropertyCard from '../components/PropertyCard.vue'

const properties = ref([])
const loading = ref(true)
const showForm = ref(false)
const error = ref(null)

const newProperty = ref({
  nickname: '',
  address: '',
  purchase_price: '',
  purchase_date: '',
  square_footage: '',
})

onMounted(async () => {
  try {
    properties.value = await getProperties()
  } catch (e) {
    error.value = 'Failed to load properties.'
  } finally {
    loading.value = false
  }
})

async function submitNewProperty() {
  if (!newProperty.value.nickname || !newProperty.value.address) return
  error.value = null

  try {
    const created = await createProperty({
      nickname: newProperty.value.nickname,
      address: newProperty.value.address,
      purchase_price: newProperty.value.purchase_price || '0',
      purchase_date: newProperty.value.purchase_date || null,
      square_footage: newProperty.value.square_footage
        ? parseInt(newProperty.value.square_footage)
        : null,
    })
    properties.value.push(created)
    newProperty.value = { nickname: '', address: '', purchase_price: '', purchase_date: '', square_footage: '' }
    showForm.value = false
  } catch (e) {
    error.value = 'Failed to create property.'
  }
}

function onPropertyDeleted(id) {
  properties.value = properties.value.filter(p => p.id !== id)
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Properties</h1>
      <button
        @click="showForm = !showForm"
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
      >
        {{ showForm ? 'Cancel' : '+ Add Property' }}
      </button>
    </div>

    <div v-if="showForm" class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-6">
      <h2 class="text-base font-semibold text-gray-800 dark:text-gray-100 mb-4">New Property</h2>
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Nickname *</label>
          <input v-model="newProperty.nickname" type="text" placeholder="e.g. Beach House"
            class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Address *</label>
          <input v-model="newProperty.address" type="text" placeholder="123 Main St"
            class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Purchase Price</label>
          <input v-model="newProperty.purchase_price" type="number" step="0.01" placeholder="0.00"
            class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Purchase Date</label>
          <input v-model="newProperty.purchase_date" type="date"
            class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Square Footage</label>
          <input v-model="newProperty.square_footage" type="number" placeholder="e.g. 1200"
            class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
      </div>
      <button
        @click="submitNewProperty"
        class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
      >
        Save Property
      </button>
    </div>

    <p v-if="error" class="text-red-600 dark:text-red-400 text-sm mb-4">{{ error }}</p>
    <p v-if="loading" class="text-gray-500 dark:text-gray-400 text-sm">Loading...</p>
    <p v-else-if="properties.length === 0" class="text-gray-400 dark:text-gray-500 text-sm">
      No properties yet. Add your first one above.
    </p>

    <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <PropertyCard
        v-for="p in properties"
        :key="p.id"
        :property="p"
        @deleted="onPropertyDeleted"
      />
    </div>
  </div>
</template>
