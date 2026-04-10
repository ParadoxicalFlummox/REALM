<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProperty } from '../api/properties'
import { getInsights } from '../api/dashboard'
import MetricsPanel from '../components/MetricsPanel.vue'

const route = useRoute()
const propertyId = parseInt(route.params.id)

const property = ref(null)
const insights = ref(null)
const loading = ref(false)
const error = ref(null)

const today = new Date().toISOString().split('T')[0]
const sixMonthsAgo = new Date(Date.now() - 180 * 86400000).toISOString().split('T')[0]

const startDate = ref(sixMonthsAgo)
const endDate = ref(today)
const targetProfit = ref('200.00')
const numTenants = ref(1)

async function fetchInsights() {
  loading.value = true
  error.value = null
  try {
    insights.value = await getInsights(propertyId, {
      startDate: startDate.value,
      endDate: endDate.value,
      targetProfit: targetProfit.value,
      numTenants: numTenants.value,
    })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load insights.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    property.value = await getProperty(propertyId)
  } catch (e) {
    error.value = 'Property not found.'
    return
  }
  await fetchInsights()
})

watch([startDate, endDate, targetProfit, numTenants], fetchInsights)
</script>

<template>
  <div>
    <div class="mb-6">
      <RouterLink
        :to="`/properties/${propertyId}`"
        class="text-sm text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"
      >
        ← {{ property?.nickname || 'Property' }}
      </RouterLink>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mt-1">Insights</h1>
      <p v-if="property" class="text-gray-500 dark:text-gray-400 text-sm">{{ property.address }}</p>
    </div>

    <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5 mb-6">
      <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">Date Range & Settings</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div>
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Start Date</label>
          <input v-model="startDate" type="date"
            class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">End Date</label>
          <input v-model="endDate" type="date"
            class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Target Profit / mo</label>
          <input v-model="targetProfit" type="number" step="0.01"
            class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Number of Tenants</label>
          <input v-model.number="numTenants" type="number" min="1"
            class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
      </div>
    </div>

    <p v-if="error" class="text-red-600 dark:text-red-400 text-sm mb-4">{{ error }}</p>
    <p v-if="loading" class="text-gray-400 dark:text-gray-500 text-sm">Calculating...</p>

    <MetricsPanel v-if="insights && !loading" :insights="insights" />
  </div>
</template>
