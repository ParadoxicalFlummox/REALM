<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { calculateDeal, saveDeal, getDeals, deleteDeal } from '../api/deals'
import { getProperties, getProperty } from '../api/properties'

const route = useRoute()

// If navigated from a property's Deals tab, property_id comes as a query param
const linkedPropertyId = route.query.property_id ? parseInt(route.query.property_id) : null
// If navigating to /deals/:id, load that saved deal
const savedDealId = route.params.id ? parseInt(route.params.id) : null

const properties = ref([])
const results = ref(null)
const savedDeals = ref([])
const calculating = ref(false)
const saving = ref(false)
const error = ref(null)
const saveError = ref(null)
const saveName = ref('')
const showSaveField = ref(false)

const form = reactive({
  address: '',
  property_id: linkedPropertyId || '',

  // Purchase
  purchase_price: '',
  down_payment: '',
  closing_costs: '',
  rehab_cost: '',

  // Loan
  interest_rate: '',
  loan_term_years: 30,

  // Income / expenses
  monthly_rent: '',
  vacancy_rate: '5.0',
  monthly_property_tax: '',
  insurance: '',
  hoa: '',
  maintenance: '',
  capex: '',
  utilities: '',
  lawn_snow: '',
})

onMounted(async () => {
  properties.value = await getProperties()
  savedDeals.value = await getDeals(linkedPropertyId)

  // If linked to a property, pre-fill address and purchase price
  if (linkedPropertyId) {
    const prop = await getProperty(linkedPropertyId)
    form.address = prop.address
    if (prop.purchase_price && parseFloat(prop.purchase_price) > 0) {
      form.purchase_price = prop.purchase_price
    }
  }
})

function buildPayload() {
  return {
    name: saveName.value || null,
    address: form.address,
    property_id: form.property_id || null,
    purchase_price: form.purchase_price,
    down_payment: form.down_payment,
    closing_costs: form.closing_costs || '0',
    rehab_cost: form.rehab_cost || '0',
    interest_rate: form.interest_rate,
    loan_term_years: parseInt(form.loan_term_years),
    monthly_rent: form.monthly_rent,
    vacancy_rate: form.vacancy_rate || '5.0',
    monthly_property_tax: form.monthly_property_tax || '0',
    insurance: form.insurance || '0',
    hoa: form.hoa || '0',
    maintenance: form.maintenance || '0',
    capex: form.capex || '0',
    utilities: form.utilities || '0',
    lawn_snow: form.lawn_snow || '0',
  }
}

async function calculate() {
  if (!form.purchase_price || !form.down_payment || !form.interest_rate || !form.monthly_rent) {
    error.value = 'Purchase price, down payment, interest rate, and monthly rent are required.'
    return
  }
  error.value = null
  calculating.value = true
  try {
    results.value = await calculateDeal(buildPayload())
    showSaveField.value = false
  } catch (e) {
    error.value = e.response?.data?.detail || 'Calculation failed.'
  } finally {
    calculating.value = false
  }
}

async function save() {
  saving.value = true
  saveError.value = null
  try {
    const saved = await saveDeal({ ...buildPayload(), name: saveName.value || null })
    savedDeals.value.unshift(saved)
    showSaveField.value = false
    saveName.value = ''
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Failed to save deal.'
  } finally {
    saving.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('Delete this saved deal?')) return
  try {
    await deleteDeal(id)
    savedDeals.value = savedDeals.value.filter(d => d.id !== id)
  } catch (e) {
    alert('Failed to delete deal.')
  }
}

const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })
function fmt(val) { return currency.format(parseFloat(val)) }
function fmtPct(val) { return parseFloat(val).toFixed(2) + '%' }
function fmtDscr(val) { return parseFloat(val).toFixed(2) }
</script>

<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Deal Analyzer</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        Plug in the numbers — get cash flow, NOI, and DSCR instantly.
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Input Form -->
      <div class="space-y-5">

        <!-- Address + Property Link -->
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
          <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">Deal Info</h2>
          <div class="space-y-3">
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Address *</label>
              <input v-model="form.address" type="text" placeholder="123 Oak St, City, State"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Link to Property <span class="text-gray-400">(optional)</span></label>
              <select v-model="form.property_id"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">— standalone deal —</option>
                <option v-for="p in properties" :key="p.id" :value="p.id">{{ p.nickname }}</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Purchase -->
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
          <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">Purchase</h2>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Purchase Price *</label>
              <input v-model="form.purchase_price" type="number" step="1000" placeholder="250000"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Down Payment *</label>
              <input v-model="form.down_payment" type="number" step="1000" placeholder="50000"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Closing Costs</label>
              <input v-model="form.closing_costs" type="number" step="100" placeholder="5000"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Rehab Cost</label>
              <input v-model="form.rehab_cost" type="number" step="500" placeholder="0"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
        </div>

        <!-- Loan -->
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
          <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">Loan</h2>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Interest Rate % *</label>
              <input v-model="form.interest_rate" type="number" step="0.125" placeholder="6.750"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Term (years)</label>
              <select v-model="form.loan_term_years"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option :value="30">30 years</option>
                <option :value="20">20 years</option>
                <option :value="15">15 years</option>
                <option :value="10">10 years</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Income & Expenses -->
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
          <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">Monthly Income & Expenses</h2>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Monthly Rent *</label>
              <input v-model="form.monthly_rent" type="number" step="50" placeholder="1800"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Vacancy Rate %</label>
              <input v-model="form.vacancy_rate" type="number" step="0.5" placeholder="5.0"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Property Tax / mo</label>
              <input v-model="form.monthly_property_tax" type="number" step="10" placeholder="250"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Insurance / mo</label>
              <input v-model="form.insurance" type="number" step="10" placeholder="100"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">HOA / mo</label>
              <input v-model="form.hoa" type="number" step="10" placeholder="0"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Maintenance / mo</label>
              <input v-model="form.maintenance" type="number" step="10" placeholder="100"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">CapEx / mo</label>
              <input v-model="form.capex" type="number" step="10" placeholder="100"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Utilities / mo</label>
              <input v-model="form.utilities" type="number" step="10" placeholder="0"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Lawn / Snow / mo</label>
              <input v-model="form.lawn_snow" type="number" step="10" placeholder="0"
                class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
        </div>

        <p v-if="error" class="text-red-600 dark:text-red-400 text-sm">{{ error }}</p>

        <button
          @click="calculate"
          :disabled="calculating"
          class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium text-sm rounded transition-colors"
        >
          {{ calculating ? 'Calculating...' : 'Calculate' }}
        </button>
      </div>

      <!-- Results Panel -->
      <div class="space-y-5">
        <div v-if="!results" class="bg-white dark:bg-gray-800 border border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-10 text-center">
          <p class="text-gray-400 dark:text-gray-500 text-sm">Fill in the inputs and click Calculate to see results.</p>
        </div>

        <template v-else>
          <!-- Key metrics -->
          <div class="grid grid-cols-1 gap-4">
            <!-- Cash flow — most prominent -->
            <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
              <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Monthly Cash Flow</p>
              <p
                class="text-3xl font-bold"
                :class="parseFloat(results.monthly_cash_flow) >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
              >
                {{ fmt(results.monthly_cash_flow) }}
              </p>
              <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
                {{ fmt(results.annual_cash_flow) }} / year
              </p>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <!-- NOI -->
              <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Monthly NOI</p>
                <p class="text-xl font-bold text-gray-900 dark:text-white">{{ fmt(results.monthly_noi) }}</p>
                <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">before debt service</p>
              </div>

              <!-- DSCR -->
              <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">DSCR</p>
                <p
                  class="text-xl font-bold"
                  :class="parseFloat(results.dscr) >= 1.25 ? 'text-green-600 dark:text-green-400' : parseFloat(results.dscr) >= 1.0 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400'"
                >
                  {{ fmtDscr(results.dscr) }}
                </p>
                <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
                  {{ parseFloat(results.dscr) >= 1.25 ? 'Lender-healthy' : parseFloat(results.dscr) >= 1.0 ? 'Covering debt' : 'Below break-even' }}
                </p>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <!-- Mortgage -->
              <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Monthly Mortgage</p>
                <p class="text-xl font-bold text-gray-900 dark:text-white">{{ fmt(results.monthly_mortgage) }}</p>
              </div>

              <!-- Cash-on-cash -->
              <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Cash-on-Cash Return</p>
                <p
                  class="text-xl font-bold"
                  :class="parseFloat(results.cash_on_cash_return) >= 8 ? 'text-green-600 dark:text-green-400' : 'text-gray-900 dark:text-white'"
                >
                  {{ fmtPct(results.cash_on_cash_return) }}
                </p>
              </div>
            </div>

            <!-- Break-even + Tax -->
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Break-Even Occupancy</p>
                <p class="text-xl font-bold text-gray-900 dark:text-white">{{ fmtPct(results.break_even_occupancy) }}</p>
                <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">min occupancy to cover costs</p>
              </div>
              <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Annual Property Tax</p>
                <p class="text-xl font-bold text-gray-900 dark:text-white">{{ fmt(results.annual_property_tax) }}</p>
                <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">est. tax deduction (consult CPA)</p>
              </div>
            </div>
          </div>

          <!-- Save section -->
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
            <div v-if="!showSaveField">
              <button
                @click="showSaveField = true"
                class="w-full py-2 text-sm font-medium text-blue-600 dark:text-blue-400 border border-blue-300 dark:border-blue-700 rounded hover:bg-blue-50 dark:hover:bg-blue-900 transition-colors"
              >
                Save this Analysis
              </button>
            </div>
            <div v-else class="space-y-3">
              <div>
                <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Analysis Name <span class="text-gray-400">(optional)</span></label>
                <input v-model="saveName" type="text" placeholder="e.g. 123 Oak — 20% down scenario"
                  class="w-full border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <p v-if="saveError" class="text-red-600 dark:text-red-400 text-xs">{{ saveError }}</p>
              <div class="flex gap-2">
                <button
                  @click="save"
                  :disabled="saving"
                  class="flex-1 py-2 text-sm font-medium bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded transition-colors"
                >
                  {{ saving ? 'Saving...' : 'Confirm Save' }}
                </button>
                <button
                  @click="showSaveField = false"
                  class="px-4 py-2 text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Saved Deals -->
    <div v-if="savedDeals.length > 0" class="mt-10">
      <h2 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Saved Analyses</h2>
      <div class="space-y-3">
        <div
          v-for="deal in savedDeals"
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
                {{ fmt(deal.monthly_cash_flow) }}/mo
              </p>
            </div>
            <div class="text-center">
              <p class="text-xs text-gray-400 dark:text-gray-500">NOI</p>
              <p class="font-semibold text-gray-900 dark:text-white">{{ fmt(deal.monthly_noi) }}/mo</p>
            </div>
            <div class="text-center">
              <p class="text-xs text-gray-400 dark:text-gray-500">DSCR</p>
              <p class="font-semibold text-gray-900 dark:text-white">{{ fmtDscr(deal.dscr) }}</p>
            </div>
            <button
              @click="handleDelete(deal.id)"
              class="text-xs text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
