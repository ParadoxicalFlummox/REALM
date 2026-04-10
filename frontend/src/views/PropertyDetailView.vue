<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProperty } from '../api/properties'
import { getTransactions, deleteTransaction } from '../api/transactions'
import { getAssets, deleteAsset } from '../api/assets'
import { getDeals, deleteDeal } from '../api/deals'
import TransactionForm from '../components/TransactionForm.vue'
import AssetForm from '../components/AssetForm.vue'

const route = useRoute()
const propertyId = parseInt(route.params.id)

const property = ref(null)
const allTransactions = ref([])
const allAssets = ref([])
const deals = ref([])
const loading = ref(true)
const error = ref(null)
const activeTab = ref('transactions')
const showTransactionForm = ref(false)
const showAssetForm = ref(false)

const transactions = computed(() =>
  allTransactions.value.filter(t => t.property_id === propertyId)
)

const assets = computed(() =>
  allAssets.value.filter(a => a.property_id === propertyId)
)

onMounted(async () => {
  try {
    const [prop, txns, assts, dealList] = await Promise.all([
      getProperty(propertyId),
      getTransactions(0, 200),
      getAssets(0, 200),
      getDeals(propertyId),
    ])
    property.value = prop
    allTransactions.value = txns
    allAssets.value = assts
    deals.value = dealList
  } catch (e) {
    error.value = 'Failed to load property data.'
  } finally {
    loading.value = false
  }
})

function onTransactionSaved(newTxn) {
  allTransactions.value.push(newTxn)
  showTransactionForm.value = false
}

function onAssetSaved(newAsset) {
  allAssets.value.push(newAsset)
  showAssetForm.value = false
}

async function handleDeleteTransaction(id) {
  if (!confirm('Delete this transaction?')) return
  try {
    await deleteTransaction(id)
    allTransactions.value = allTransactions.value.filter(t => t.id !== id)
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to delete transaction.')
  }
}

async function handleDeleteAsset(id) {
  if (!confirm('Delete this asset?')) return
  try {
    await deleteAsset(id)
    allAssets.value = allAssets.value.filter(a => a.id !== id)
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to delete asset.')
  }
}

async function handleDeleteDeal(id) {
  if (!confirm('Delete this saved analysis?')) return
  try {
    await deleteDeal(id)
    deals.value = deals.value.filter(d => d.id !== id)
  } catch (e) {
    alert('Failed to delete deal.')
  }
}

function formatCurrency(val) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(parseFloat(val))
}
</script>

<template>
  <div>
    <div v-if="loading" class="text-gray-500 dark:text-gray-400 text-sm">Loading...</div>
    <div v-else-if="error" class="text-red-600 dark:text-red-400 text-sm">{{ error }}</div>

    <div v-else-if="property">
      <!-- Header -->
      <div class="flex items-start justify-between mb-6">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <RouterLink to="/" class="text-sm text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300">← Properties</RouterLink>
          </div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ property.nickname }}</h1>
          <p class="text-gray-500 dark:text-gray-400 text-sm">{{ property.address }}</p>
        </div>
        <RouterLink
          :to="`/properties/${propertyId}/insights`"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
        >
          View Insights
        </RouterLink>
      </div>

      <!-- Property summary bar -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Purchase Price</p>
          <p class="font-semibold text-gray-900 dark:text-white">{{ formatCurrency(property.purchase_price) }}</p>
        </div>
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Purchase Date</p>
          <p class="font-semibold text-gray-900 dark:text-white">{{ property.purchase_date || '—' }}</p>
        </div>
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Square Footage</p>
          <p class="font-semibold text-gray-900 dark:text-white">{{ property.square_footage ? property.square_footage.toLocaleString() + ' sq ft' : '—' }}</p>
        </div>
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Status</p>
          <p :class="property.is_active ? 'text-green-600 dark:text-green-400' : 'text-gray-400 dark:text-gray-500'" class="font-semibold">
            {{ property.is_active ? 'Active' : 'Inactive' }}
          </p>
        </div>
      </div>

      <!-- Tabs -->
      <div class="flex gap-1 border-b border-gray-200 dark:border-gray-700 mb-6">
        <button
          @click="activeTab = 'transactions'"
          :class="activeTab === 'transactions'
            ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400'
            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'"
          class="px-4 py-2 text-sm font-medium transition-colors"
        >
          Transactions ({{ transactions.length }})
        </button>
        <button
          @click="activeTab = 'assets'"
          :class="activeTab === 'assets'
            ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400'
            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'"
          class="px-4 py-2 text-sm font-medium transition-colors"
        >
          Assets ({{ assets.length }})
        </button>
        <button
          @click="activeTab = 'deals'"
          :class="activeTab === 'deals'
            ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400'
            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'"
          class="px-4 py-2 text-sm font-medium transition-colors"
        >
          Deals ({{ deals.length }})
        </button>
      </div>

      <!-- Transactions Tab -->
      <div v-if="activeTab === 'transactions'">
        <div class="flex justify-end mb-4">
          <button
            @click="showTransactionForm = !showTransactionForm"
            class="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
          >
            {{ showTransactionForm ? 'Cancel' : '+ Add Transaction' }}
          </button>
        </div>

        <TransactionForm
          v-if="showTransactionForm"
          :property-id="propertyId"
          @saved="onTransactionSaved"
          class="mb-4"
        />

        <div v-if="transactions.length === 0" class="text-gray-400 dark:text-gray-500 text-sm">
          No transactions yet for this property.
        </div>

        <div v-else class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 text-left">
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Date</th>
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Category</th>
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Type</th>
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Description</th>
                <th class="px-4 py-3 font-medium text-gray-600 dark:text-gray-300 text-right">Amount</th>
                <th class="px-4 py-3"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="t in transactions"
                :key="t.id"
                class="border-b border-gray-50 dark:border-gray-700 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                <td class="px-4 py-3 text-gray-600 dark:text-gray-400">{{ t.transaction_date }}</td>
                <td class="px-4 py-3 text-gray-700 dark:text-gray-300">{{ t.category }}</td>
                <td class="px-4 py-3">
                  <span
                    :class="t.transaction_type === 'income'
                      ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
                      : 'bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300'"
                    class="px-2 py-0.5 rounded-full text-xs font-medium"
                  >
                    {{ t.transaction_type }}
                  </span>
                </td>
                <td class="px-4 py-3 text-gray-500 dark:text-gray-400">{{ t.description || '—' }}</td>
                <td
                  class="px-4 py-3 text-right font-medium"
                  :class="t.transaction_type === 'income' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
                >
                  {{ formatCurrency(t.amount) }}
                </td>
                <td class="px-4 py-3">
                  <button
                    @click="handleDeleteTransaction(t.id)"
                    class="text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors text-xs"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Assets Tab -->
      <div v-if="activeTab === 'assets'">
        <div class="flex justify-end mb-4">
          <button
            @click="showAssetForm = !showAssetForm"
            class="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
          >
            {{ showAssetForm ? 'Cancel' : '+ Add Asset' }}
          </button>
        </div>

        <AssetForm
          v-if="showAssetForm"
          :property-id="propertyId"
          @saved="onAssetSaved"
          class="mb-4"
        />

        <div v-if="assets.length === 0" class="text-gray-400 dark:text-gray-500 text-sm">
          No assets tracked for this property.
        </div>

        <div v-else class="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div
            v-for="a in assets"
            :key="a.id"
            class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 flex justify-between items-start"
          >
            <div>
              <p class="font-medium text-gray-900 dark:text-white">{{ a.name }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ a.category || 'other' }}</p>
              <p v-if="a.description" class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ a.description }}</p>
              <p v-if="a.purchase_price" class="text-sm text-gray-700 dark:text-gray-300 mt-1 font-medium">
                {{ formatCurrency(a.purchase_price) }}
              </p>
            </div>
            <button
              @click="handleDeleteAsset(a.id)"
              class="text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors text-xs ml-4 shrink-0"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
      <!-- Deals Tab -->
      <div v-if="activeTab === 'deals'">
        <div class="flex justify-end mb-4">
          <RouterLink
            :to="`/deals?property_id=${propertyId}`"
            class="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
          >
            + New Analysis
          </RouterLink>
        </div>

        <div v-if="deals.length === 0" class="text-gray-400 dark:text-gray-500 text-sm">
          No saved deal analyses for this property. Run the Deal Analyzer and save a snapshot.
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="deal in deals"
            :key="deal.id"
            class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5 flex items-center justify-between gap-4"
          >
            <div class="min-w-0">
              <p class="font-medium text-gray-900 dark:text-white truncate">
                {{ deal.name || deal.address }}
              </p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ deal.created_at }}</p>
            </div>
            <div class="flex items-center gap-6 shrink-0 text-sm">
              <div class="text-center">
                <p class="text-xs text-gray-400 dark:text-gray-500">Cash Flow</p>
                <p
                  class="font-semibold"
                  :class="parseFloat(deal.monthly_cash_flow) >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
                >
                  {{ formatCurrency(deal.monthly_cash_flow) }}/mo
                </p>
              </div>
              <div class="text-center">
                <p class="text-xs text-gray-400 dark:text-gray-500">NOI</p>
                <p class="font-semibold text-gray-900 dark:text-white">{{ formatCurrency(deal.monthly_noi) }}/mo</p>
              </div>
              <div class="text-center">
                <p class="text-xs text-gray-400 dark:text-gray-500">DSCR</p>
                <p class="font-semibold text-gray-900 dark:text-white">{{ parseFloat(deal.dscr).toFixed(2) }}</p>
              </div>
              <button
                @click="handleDeleteDeal(deal.id)"
                class="text-xs text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
