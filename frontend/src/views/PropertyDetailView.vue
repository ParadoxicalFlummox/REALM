<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProperty } from '../api/properties'
import { getTransactions, deleteTransaction } from '../api/transactions'
import { getAssets, deleteAsset } from '../api/assets'
import { getDeals, deleteDeal } from '../api/deals'
import { getEquity, createLoan, updateLoan, deleteLoan } from '../api/loans'
import { updateProperty } from '../api/properties'
import TransactionForm from '../components/TransactionForm.vue'
import AssetForm from '../components/AssetForm.vue'

const route = useRoute()
const propertyId = parseInt(route.params.id)

const property = ref(null)
const allTransactions = ref([])
const allAssets = ref([])
const deals = ref([])
const equity = ref(null)
const loading = ref(true)
const error = ref(null)
const activeTab = ref('transactions')
const showTransactionForm = ref(false)
const showAssetForm = ref(false)
const showLoanForm = ref(false)
const editingTransactionId = ref(null)
const editingAssetId = ref(null)
const editingLoanId = ref(null)
const editLoanForm = ref({})

const editingTransaction = computed(() =>
  editingTransactionId.value ? allTransactions.value.find(t => t.id === editingTransactionId.value) : null
)
const editingAsset = computed(() =>
  editingAssetId.value ? allAssets.value.find(a => a.id === editingAssetId.value) : null
)
const estimatedValueInput = ref('')
const savingEstimatedValue = ref(false)

const newLoan = ref({
  label: '',
  lender: '',
  original_balance: '',
  interest_rate: '',
  loan_term_years: 30,
  origination_date: '',
  balance_override: '',
})

const transactions = computed(() =>
  allTransactions.value.filter(t => t.property_id === propertyId)
)

const assets = computed(() =>
  allAssets.value.filter(a => a.property_id === propertyId)
)

onMounted(async () => {
  try {
    const [prop, txns, assts, dealList, equityData] = await Promise.all([
      getProperty(propertyId),
      getTransactions(0, 200),
      getAssets(0, 200),
      getDeals(propertyId),
      getEquity(propertyId),
    ])
    property.value = prop
    allTransactions.value = txns
    allAssets.value = assts
    deals.value = dealList
    equity.value = equityData
    estimatedValueInput.value = prop.estimated_value ? String(prop.estimated_value) : ''
  } catch (e) {
    error.value = 'Failed to load property data.'
  } finally {
    loading.value = false
  }
})

function onTransactionSaved(result) {
  if (editingTransactionId.value) {
    const idx = allTransactions.value.findIndex(t => t.id === result.id)
    if (idx !== -1) allTransactions.value[idx] = result
    editingTransactionId.value = null
  } else {
    allTransactions.value.push(result)
    showTransactionForm.value = false
  }
}

function onAssetSaved(result) {
  if (editingAssetId.value) {
    const idx = allAssets.value.findIndex(a => a.id === result.id)
    if (idx !== -1) allAssets.value[idx] = result
    editingAssetId.value = null
  } else {
    allAssets.value.push(result)
    showAssetForm.value = false
  }
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

async function saveEstimatedValue() {
  if (!estimatedValueInput.value) return
  savingEstimatedValue.value = true
  try {
    const updated = await updateProperty(propertyId, { estimated_value: estimatedValueInput.value })
    property.value = updated
    equity.value = await getEquity(propertyId)
  } catch (e) {
    alert('Failed to save estimated value.')
  } finally {
    savingEstimatedValue.value = false
  }
}

async function submitNewLoan() {
  if (!newLoan.value.original_balance || !newLoan.value.interest_rate || !newLoan.value.origination_date) return
  try {
    const payload = {
      property_id: propertyId,
      label: newLoan.value.label || null,
      lender: newLoan.value.lender || null,
      original_balance: newLoan.value.original_balance,
      interest_rate: newLoan.value.interest_rate,
      loan_term_years: newLoan.value.loan_term_years || 30,
      origination_date: newLoan.value.origination_date,
      balance_override: newLoan.value.balance_override || null,
    }
    await createLoan(payload)
    equity.value = await getEquity(propertyId)
    newLoan.value = { label: '', lender: '', original_balance: '', interest_rate: '', loan_term_years: 30, origination_date: '', balance_override: '' }
    showLoanForm.value = false
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to add loan.')
  }
}

function startEditLoan(loan) {
  editingLoanId.value = loan.id
  editLoanForm.value = {
    label: loan.label ?? '',
    lender: loan.lender ?? '',
    original_balance: loan.original_balance,
    interest_rate: loan.interest_rate,
    loan_term_years: loan.loan_term_years,
    origination_date: loan.origination_date,
    balance_override: loan.balance_override ?? '',
  }
}

async function submitEditLoan() {
  try {
    const payload = {
      label: editLoanForm.value.label || null,
      lender: editLoanForm.value.lender || null,
      original_balance: editLoanForm.value.original_balance,
      interest_rate: editLoanForm.value.interest_rate,
      loan_term_years: editLoanForm.value.loan_term_years || 30,
      origination_date: editLoanForm.value.origination_date,
      balance_override: editLoanForm.value.balance_override || null,
    }
    await updateLoan(editingLoanId.value, payload)
    equity.value = await getEquity(propertyId)
    editingLoanId.value = null
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to update loan.')
  }
}

async function handleDeleteLoan(id) {
  if (!confirm('Delete this loan?')) return
  try {
    await deleteLoan(id)
    equity.value = await getEquity(propertyId)
  } catch (e) {
    alert('Failed to delete loan.')
  }
}

function ltvColor(ltv) {
  if (ltv < 70) return 'text-green-600 dark:text-green-400'
  if (ltv < 80) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-red-600 dark:text-red-400'
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
            <RouterLink to="/properties" class="text-sm text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300">← Properties</RouterLink>
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
        <button
          @click="activeTab = 'equity'"
          :class="activeTab === 'equity'
            ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400'
            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'"
          class="px-4 py-2 text-sm font-medium transition-colors"
        >
          Equity ({{ equity?.loans?.length ?? 0 }})
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
        <TransactionForm
          v-if="editingTransactionId && !showTransactionForm"
          :property-id="propertyId"
          :item="editingTransaction"
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
                  <div class="flex items-center gap-3">
                    <button
                      @click="editingTransactionId = editingTransactionId === t.id ? null : t.id; showTransactionForm = false"
                      class="text-gray-400 dark:text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 transition-colors text-xs"
                    >
                      {{ editingTransactionId === t.id ? 'Cancel' : 'Edit' }}
                    </button>
                    <button
                      @click="handleDeleteTransaction(t.id)"
                      class="text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors text-xs"
                    >
                      Delete
                    </button>
                  </div>
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
        <AssetForm
          v-if="editingAssetId && !showAssetForm"
          :property-id="propertyId"
          :item="editingAsset"
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
            <div class="flex flex-col gap-1 ml-4 shrink-0">
              <button
                @click="editingAssetId = editingAssetId === a.id ? null : a.id; showAssetForm = false"
                class="text-gray-400 dark:text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 transition-colors text-xs"
              >
                {{ editingAssetId === a.id ? 'Cancel' : 'Edit' }}
              </button>
              <button
                @click="handleDeleteAsset(a.id)"
                class="text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors text-xs"
              >
                Delete
              </button>
            </div>
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
      <!-- Equity Tab -->
      <div v-if="activeTab === 'equity'">
        <!-- Estimated Value editor -->
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5 mb-6">
          <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">Estimated Market Value</h2>
          <div class="flex items-center gap-3">
            <input
              v-model="estimatedValueInput"
              type="number"
              step="0.01"
              placeholder="e.g. 350000"
              class="w-48 border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              @click="saveEstimatedValue"
              :disabled="savingEstimatedValue"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors disabled:opacity-50"
            >
              {{ savingEstimatedValue ? 'Saving…' : 'Save' }}
            </button>
            <span v-if="property.estimated_value" class="text-sm text-gray-500 dark:text-gray-400">
              Current: {{ formatCurrency(property.estimated_value) }}
            </span>
          </div>
        </div>

        <!-- Equity summary cards -->
        <div v-if="equity" class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Estimated Value</p>
            <p class="font-semibold text-gray-900 dark:text-white">
              {{ equity.estimated_value > 0 ? formatCurrency(equity.estimated_value) : '—' }}
            </p>
          </div>
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Total Loan Balance</p>
            <p class="font-semibold text-gray-900 dark:text-white">
              {{ equity.total_loan_balance > 0 ? formatCurrency(equity.total_loan_balance) : '—' }}
            </p>
          </div>
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Equity</p>
            <p
              class="font-semibold"
              :class="parseFloat(equity.equity) >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
            >
              {{ equity.estimated_value > 0 ? formatCurrency(equity.equity) : '—' }}
            </p>
          </div>
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">LTV</p>
            <p class="font-semibold" :class="ltvColor(equity.ltv)">
              {{ equity.estimated_value > 0 && equity.total_loan_balance > 0 ? equity.ltv.toFixed(1) + '%' : '—' }}
            </p>
          </div>
        </div>

        <!-- Loans list -->
        <div class="flex justify-end mb-4">
          <button
            @click="showLoanForm = !showLoanForm"
            class="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
          >
            {{ showLoanForm ? 'Cancel' : '+ Add Loan' }}
          </button>
        </div>

        <!-- Add Loan form -->
        <div v-if="showLoanForm" class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5 mb-4">
          <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">New Loan</h2>
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Label</label>
              <input v-model="newLoan.label" type="text" placeholder="e.g. Primary Mortgage"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Lender</label>
              <input v-model="newLoan.lender" type="text" placeholder="e.g. Wells Fargo"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Original Balance *</label>
              <input v-model="newLoan.original_balance" type="number" step="0.01" placeholder="0.00"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Interest Rate (%) *</label>
              <input v-model="newLoan.interest_rate" type="number" step="0.001" placeholder="6.750"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Loan Term (years)</label>
              <input v-model.number="newLoan.loan_term_years" type="number" placeholder="30"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Origination Date *</label>
              <input v-model="newLoan.origination_date" type="date"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div class="sm:col-span-2">
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Current Balance Override <span class="font-normal text-gray-400">(optional — enter if you have a recent statement balance)</span></label>
              <input v-model="newLoan.balance_override" type="number" step="0.01" placeholder="Leave blank to use calculated balance"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
          <button
            @click="submitNewLoan"
            class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
          >
            Save Loan
          </button>
        </div>

        <div v-if="!equity?.loans?.length" class="text-gray-400 dark:text-gray-500 text-sm">
          No loans tracked for this property. Add your first loan above.
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="loan in equity.loans"
            :key="loan.id"
            class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <p class="font-medium text-gray-900 dark:text-white">{{ loan.label || 'Loan' }}</p>
                  <span v-if="loan.balance_is_override"
                    class="px-1.5 py-0.5 rounded text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300">
                    override
                  </span>
                  <span v-if="!loan.is_active"
                    class="px-1.5 py-0.5 rounded text-xs bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400">
                    paid off
                  </span>
                </div>
                <p v-if="loan.lender" class="text-xs text-gray-500 dark:text-gray-400">{{ loan.lender }}</p>
              </div>
              <div class="flex items-center gap-3 shrink-0">
                <button
                  @click="editingLoanId === loan.id ? (editingLoanId = null) : startEditLoan(loan)"
                  class="text-xs text-gray-400 dark:text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 transition-colors"
                >
                  {{ editingLoanId === loan.id ? 'Cancel' : 'Edit' }}
                </button>
                <button
                  @click="handleDeleteLoan(loan.id)"
                  class="text-xs text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors"
                >
                  Delete
                </button>
              </div>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-3">
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Current Balance</p>
                <p class="font-semibold text-gray-900 dark:text-white text-sm">{{ formatCurrency(loan.current_balance) }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Original Balance</p>
                <p class="font-semibold text-gray-700 dark:text-gray-300 text-sm">{{ formatCurrency(loan.original_balance) }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Rate / Term</p>
                <p class="font-semibold text-gray-700 dark:text-gray-300 text-sm">{{ parseFloat(loan.interest_rate).toFixed(3) }}% / {{ loan.loan_term_years }}yr</p>
              </div>
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Origination</p>
                <p class="font-semibold text-gray-700 dark:text-gray-300 text-sm">{{ loan.origination_date }}</p>
              </div>
            </div>

            <!-- Inline edit form -->
            <div v-if="editingLoanId === loan.id" class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
              <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div>
                  <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Label</label>
                  <input v-model="editLoanForm.label" type="text"
                    class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Lender</label>
                  <input v-model="editLoanForm.lender" type="text"
                    class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Original Balance</label>
                  <input v-model="editLoanForm.original_balance" type="number" step="0.01"
                    class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Interest Rate (%)</label>
                  <input v-model="editLoanForm.interest_rate" type="number" step="0.001"
                    class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Loan Term (years)</label>
                  <input v-model.number="editLoanForm.loan_term_years" type="number"
                    class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Origination Date</label>
                  <input v-model="editLoanForm.origination_date" type="date"
                    class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div class="sm:col-span-2">
                  <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Balance Override <span class="text-gray-400 font-normal">(leave blank to use calculated balance)</span></label>
                  <input v-model="editLoanForm.balance_override" type="number" step="0.01" placeholder="Enter current statement balance if known"
                    class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
              </div>
              <button
                @click="submitEditLoan"
                class="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>
