<script setup>
import { reactive, ref, onMounted } from 'vue'
import { createAsset, updateAsset, getAssetCategories } from '../api/assets'

const props = defineProps({
  propertyId: { type: Number, required: true },
  item: { type: Object, default: null },  // if provided, form is in edit mode
})

const emit = defineEmits(['saved'])

const form = reactive({
  name: '',
  category: '',
  description: '',
  purchase_price: '',
  purchase_date: '',
  serial_number: '',
})

const categories = ref([])
const error = ref(null)
const saving = ref(false)

onMounted(async () => {
  categories.value = await getAssetCategories()
  if (props.item) {
    form.name = props.item.name ?? ''
    form.category = props.item.category ?? ''
    form.description = props.item.description ?? ''
    form.purchase_price = props.item.purchase_price ?? ''
    form.purchase_date = props.item.purchase_date ?? ''
    form.serial_number = props.item.serial_number ?? ''
  }
})

async function submit() {
  if (!form.name) {
    error.value = 'Name is required.'
    return
  }
  saving.value = true
  error.value = null
  try {
    const payload = {
      name: form.name,
      category: form.category || null,
      description: form.description || null,
      purchase_price: form.purchase_price || '0',
      purchase_date: form.purchase_date || null,
      serial_number: form.serial_number || null,
      property_id: props.propertyId,
    }
    const result = props.item
      ? await updateAsset(props.item.id, payload)
      : await createAsset(payload)
    emit('saved', result)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to save asset.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
    <h3 class="text-sm font-semibold text-gray-800 dark:text-gray-100 mb-4">
      {{ item ? 'Edit Asset' : 'New Asset' }}
    </h3>

    <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Name *</label>
        <input v-model="form.name" type="text" placeholder="e.g. John Deere Mower"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Category</label>
        <select v-model="form.category"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="">— select —</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>

      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Purchase Price</label>
        <input v-model="form.purchase_price" type="number" step="0.01" placeholder="0.00"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Purchase Date</label>
        <input v-model="form.purchase_date" type="date"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Serial Number</label>
        <input v-model="form.serial_number" type="text" placeholder="Optional"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Description</label>
        <input v-model="form.description" type="text" placeholder="Optional notes"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
    </div>

    <p v-if="error" class="text-red-600 dark:text-red-400 text-xs mt-3">{{ error }}</p>

    <button
      @click="submit"
      :disabled="saving"
      class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded disabled:opacity-50 transition-colors"
    >
      {{ saving ? 'Saving...' : item ? 'Update Asset' : 'Save Asset' }}
    </button>
  </div>
</template>
