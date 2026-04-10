<script setup>
import { reactive, ref, onMounted } from 'vue'
import { createTransaction, updateTransaction, getTaxCategories } from '../api/transactions'

const props = defineProps({
  propertyId: { type: Number, required: true },
  item: { type: Object, default: null },  // if provided, form is in edit mode
})

const emit = defineEmits(['saved'])

const form = reactive({
  amount: '',
  category: '',
  tax_category: '',
  transaction_type: 'expense',
  transaction_date: new Date().toISOString().split('T')[0],
  description: '',
})

const taxCategories = ref([])
const error = ref(null)
const saving = ref(false)

onMounted(async () => {
  taxCategories.value = await getTaxCategories()
  if (props.item) {
    form.amount = props.item.amount ?? ''
    form.category = props.item.category ?? ''
    form.tax_category = props.item.tax_category ?? ''
    form.transaction_type = props.item.transaction_type ?? 'expense'
    form.transaction_date = props.item.transaction_date ?? new Date().toISOString().split('T')[0]
    form.description = props.item.description ?? ''
  }
})

async function submit() {
  if (!form.amount || !form.category) {
    error.value = 'Amount and category are required.'
    return
  }
  saving.value = true
  error.value = null
  try {
    const payload = {
      amount: form.amount,
      category: form.category,
      tax_category: form.tax_category || null,
      transaction_type: form.transaction_type,
      transaction_date: form.transaction_date,
      description: form.description || null,
      property_id: props.propertyId,
    }
    const result = props.item
      ? await updateTransaction(props.item.id, payload)
      : await createTransaction(payload)
    emit('saved', result)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to save transaction.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
    <h3 class="text-sm font-semibold text-gray-800 dark:text-gray-100 mb-4">
      {{ item ? 'Edit Transaction' : 'New Transaction' }}
    </h3>

    <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Amount *</label>
        <input v-model="form.amount" type="number" step="0.01" placeholder="0.00"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Category *</label>
        <input v-model="form.category" type="text" placeholder="e.g. rent, maintenance"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Type</label>
        <select v-model="form.transaction_type"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </select>
      </div>

      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Date</label>
        <input v-model="form.transaction_date" type="date"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <!-- Schedule E tax category — optional, for annual tax reporting -->
      <div class="sm:col-span-2">
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
          Tax Category <span class="text-gray-400 font-normal">(Schedule E — optional)</span>
        </label>
        <select v-model="form.tax_category"
          class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="">— not categorized —</option>
          <option v-for="cat in taxCategories" :key="cat" :value="cat">
            {{ cat.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) }}
          </option>
        </select>
      </div>

      <div class="sm:col-span-2">
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
      {{ saving ? 'Saving...' : item ? 'Update Transaction' : 'Save Transaction' }}
    </button>
  </div>
</template>
