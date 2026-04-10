<script setup>
import { deleteProperty } from '../api/properties'

const props = defineProps({
  property: { type: Object, required: true },
})

const emit = defineEmits(['deleted'])

async function handleDelete() {
  if (!confirm(`Delete "${props.property.nickname}"? This cannot be undone if it has no linked records.`)) return
  try {
    await deleteProperty(props.property.id)
    emit('deleted', props.property.id)
  } catch (e) {
    const msg = e.response?.data?.detail || 'Delete failed.'
    alert(msg)
  }
}
</script>

<template>
  <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-5 flex flex-col gap-3">
    <div class="flex items-start justify-between gap-2">
      <div>
        <h2 class="font-semibold text-gray-900 dark:text-white">{{ property.nickname }}</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400">{{ property.address }}</p>
      </div>
      <span
        :class="property.is_active
          ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
          : 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'"
        class="text-xs px-2 py-0.5 rounded-full font-medium shrink-0"
      >
        {{ property.is_active ? 'Active' : 'Inactive' }}
      </span>
    </div>

    <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <p v-if="property.purchase_price">
        Purchased for <span class="font-medium text-gray-900 dark:text-gray-200">${{ property.purchase_price }}</span>
      </p>
      <p v-if="property.square_footage">
        {{ property.square_footage.toLocaleString() }} sq ft
      </p>
    </div>

    <div class="flex gap-2 mt-auto pt-2 border-t border-gray-100 dark:border-gray-700">
      <RouterLink
        :to="`/properties/${property.id}`"
        class="flex-1 text-center px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 rounded transition-colors"
      >
        Details
      </RouterLink>
      <RouterLink
        :to="`/properties/${property.id}/insights`"
        class="flex-1 text-center px-3 py-1.5 text-sm bg-blue-50 dark:bg-blue-900 hover:bg-blue-100 dark:hover:bg-blue-800 text-blue-700 dark:text-blue-300 rounded transition-colors"
      >
        Insights
      </RouterLink>
      <button
        @click="handleDelete"
        class="px-3 py-1.5 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900 rounded transition-colors"
      >
        Delete
      </button>
    </div>
  </div>
</template>
