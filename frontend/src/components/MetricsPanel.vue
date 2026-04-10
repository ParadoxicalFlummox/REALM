<script setup>
const props = defineProps({
  insights: { type: Object, required: true },
})

const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })

function formatCurrency(val) {
  return currency.format(parseFloat(val))
}

function formatPercent(val) {
  return val.toFixed(2) + '%'
}

function totalExpenses() {
  return Object.values(props.insights.expense_distribution)
    .reduce((sum, v) => sum + parseFloat(v), 0)
}

function categoryPercent(amount) {
  const total = totalExpenses()
  if (total === 0) return 0
  return (parseFloat(amount) / total) * 100
}
</script>

<template>
  <div class="space-y-6">
    <p class="text-xs text-gray-400 dark:text-gray-500">
      Period: {{ insights.period.start }} → {{ insights.period.end }}
    </p>

    <!-- Core metrics -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Net Cash Flow</p>
        <p
          class="text-2xl font-bold"
          :class="parseFloat(insights.metrics.net_cash_flow) >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
        >
          {{ formatCurrency(insights.metrics.net_cash_flow) }}
        </p>
      </div>

      <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Operating Expense Ratio</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ formatPercent(insights.metrics.operating_expense_ratio_percentage) }}
        </p>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">expenses ÷ income</p>
      </div>

      <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Return on Investment</p>
        <p
          class="text-2xl font-bold"
          :class="insights.metrics.return_on_income_percentage >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
        >
          {{ formatPercent(insights.metrics.return_on_income_percentage) }}
        </p>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">net cash flow ÷ purchase price</p>
      </div>
    </div>

    <!-- Rent suggestions -->
    <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
      <h2 class="text-sm font-semibold text-gray-800 dark:text-gray-100 mb-4">Rent Targets</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Break-Even per Tenant</p>
          <p class="text-xl font-bold text-gray-900 dark:text-white">
            {{ formatCurrency(insights.rent_suggestions.break_even_per_tenant) }}
          </p>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-0.5">covers expenses only</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">With Profit Target per Tenant</p>
          <p class="text-xl font-bold text-blue-700 dark:text-blue-400">
            {{ formatCurrency(insights.rent_suggestions.custom_profit_target_per_tenant) }}
          </p>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-0.5">covers expenses + profit goal</p>
        </div>
      </div>
    </div>

    <!-- Expense breakdown -->
    <div
      v-if="Object.keys(insights.expense_distribution).length > 0"
      class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5"
    >
      <h2 class="text-sm font-semibold text-gray-800 dark:text-gray-100 mb-4">Expense Breakdown</h2>
      <div class="space-y-3">
        <div
          v-for="(amount, category) in insights.expense_distribution"
          :key="category"
        >
          <div class="flex justify-between text-sm mb-1">
            <span class="text-gray-700 dark:text-gray-300 capitalize">{{ category }}</span>
            <span class="font-medium text-gray-900 dark:text-white">{{ formatCurrency(amount) }}</span>
          </div>
          <div class="h-1.5 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              class="h-full bg-blue-400 dark:bg-blue-500 rounded-full"
              :style="{ width: categoryPercent(amount) + '%' }"
            />
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-gray-400 dark:text-gray-500 text-sm">
      No expenses recorded in this period.
    </div>
  </div>
</template>
