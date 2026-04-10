<script setup>
import { ref, onMounted } from 'vue'
import { getPortfolioSummary } from '../api/portfolio'

const summary = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    summary.value = await getPortfolioSummary()
  } catch (e) {
    error.value = 'Failed to load portfolio summary.'
  } finally {
    loading.value = false
  }
})

const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })
function fmt(val) {
  if (val === null || val === undefined) return '—'
  return currency.format(parseFloat(val))
}

function ltvColor(ltv) {
  if (ltv === null || ltv === undefined) return 'text-gray-400 dark:text-gray-500'
  if (ltv < 70) return 'text-green-600 dark:text-green-400'
  if (ltv < 80) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-red-600 dark:text-red-400'
}

function equityColor(equity) {
  if (equity === null || equity === undefined) return 'text-gray-400 dark:text-gray-500'
  return parseFloat(equity) >= 0
    ? 'text-green-600 dark:text-green-400'
    : 'text-red-600 dark:text-red-400'
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Portfolio Overview</h1>
      <p v-if="summary" class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        {{ summary.property_count }} {{ summary.property_count === 1 ? 'property' : 'properties' }}
      </p>
    </div>

    <div v-if="loading" class="text-gray-500 dark:text-gray-400 text-sm">Loading...</div>
    <div v-else-if="error" class="text-red-600 dark:text-red-400 text-sm">{{ error }}</div>

    <template v-else-if="summary">
      <!-- Empty state -->
      <div v-if="summary.property_count === 0" class="bg-white dark:bg-gray-800 border border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-10 text-center">
        <p class="text-gray-500 dark:text-gray-400 text-sm mb-3">No properties in your portfolio yet.</p>
        <RouterLink
          to="/properties"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
        >
          + Add Your First Property
        </RouterLink>
      </div>

      <template v-else>
        <!-- Summary cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Properties</p>
            <p class="font-semibold text-gray-900 dark:text-white text-2xl">{{ summary.property_count }}</p>
          </div>
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Total Est. Value</p>
            <p class="font-semibold text-gray-900 dark:text-white">
              {{ summary.total_estimated_value > 0 ? fmt(summary.total_estimated_value) : '—' }}
            </p>
          </div>
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Total Equity</p>
            <p class="font-semibold" :class="equityColor(summary.total_equity)">
              {{ summary.total_estimated_value > 0 ? fmt(summary.total_equity) : '—' }}
            </p>
          </div>
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Portfolio LTV</p>
            <p class="font-semibold" :class="ltvColor(summary.portfolio_ltv)">
              {{ summary.portfolio_ltv !== null ? summary.portfolio_ltv.toFixed(1) + '%' : '—' }}
            </p>
          </div>
        </div>

        <!-- Missing value notice -->
        <div
          v-if="summary.missing_value_count > 0"
          class="text-xs text-amber-600 dark:text-amber-400 mb-4"
        >
          {{ summary.missing_value_count }} {{ summary.missing_value_count === 1 ? 'property is' : 'properties are' }} missing an estimated value — set it in the property's Equity tab to include it in totals.
        </div>

        <!-- Per-property breakdown -->
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 text-left">
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Property</th>
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300 text-right">Est. Value</th>
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300 text-right">Loan Balance</th>
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300 text-right">Equity</th>
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300 text-right">LTV</th>
                <th class="px-4 py-3"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="prop in summary.properties"
                :key="prop.id"
                class="border-b border-gray-50 dark:border-gray-700 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                <td class="px-4 py-3">
                  <p class="font-medium text-gray-900 dark:text-white">{{ prop.nickname }}</p>
                  <p class="text-xs text-gray-400 dark:text-gray-500">{{ prop.address }}</p>
                </td>
                <td class="px-4 py-3 text-right text-gray-700 dark:text-gray-300">
                  {{ fmt(prop.estimated_value) }}
                </td>
                <td class="px-4 py-3 text-right text-gray-700 dark:text-gray-300">
                  {{ prop.total_loan_balance > 0 ? fmt(prop.total_loan_balance) : '—' }}
                </td>
                <td class="px-4 py-3 text-right font-medium" :class="equityColor(prop.equity)">
                  {{ fmt(prop.equity) }}
                </td>
                <td class="px-4 py-3 text-right font-medium" :class="ltvColor(prop.ltv)">
                  {{ prop.ltv !== null ? prop.ltv.toFixed(1) + '%' : '—' }}
                </td>
                <td class="px-4 py-3">
                  <RouterLink
                    :to="`/properties/${prop.id}`"
                    class="text-xs text-blue-600 dark:text-blue-400 hover:underline"
                  >
                    Details →
                  </RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </template>
  </div>
</template>
