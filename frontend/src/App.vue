<script setup>
import { ref } from 'vue'

// Company name: localStorage override → .env → default
const storedName = localStorage.getItem('companyName')
const companyName = ref(storedName || import.meta.env.VITE_COMPANY_NAME || 'TAP·re')

// Dark mode
const isDark = ref(localStorage.getItem('theme') === 'dark')
if (isDark.value) document.documentElement.classList.add('dark')

function toggleDark() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// Settings panel
const showSettings = ref(false)
const editingName = ref('')

function openSettings() {
  editingName.value = companyName.value
  showSettings.value = true
}

function saveSettings() {
  const name = editingName.value.trim()
  companyName.value = name || import.meta.env.VITE_COMPANY_NAME || 'TAP·re'
  localStorage.setItem('companyName', companyName.value)
  showSettings.value = false
}

function resetName() {
  const defaultName = import.meta.env.VITE_COMPANY_NAME || 'TAP·re'
  companyName.value = defaultName
  localStorage.removeItem('companyName')
  editingName.value = defaultName
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col">

    <!-- Nav -->
    <nav class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex items-center gap-6">
      <RouterLink to="/" class="font-bold text-lg text-gray-900 dark:text-white tracking-tight">
        {{ companyName }}
      </RouterLink>
      <RouterLink
        to="/properties"
        class="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
        active-class="text-gray-900 dark:text-white font-medium"
      >
        Properties
      </RouterLink>
      <RouterLink
        to="/deals"
        class="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
        active-class="text-gray-900 dark:text-white font-medium"
      >
        Deal Analyzer
      </RouterLink>

      <!-- Gear button -->
      <div class="ml-auto relative">
        <button
          @click="openSettings"
          class="p-1.5 rounded-md text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          title="Settings"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
        </button>

        <!-- Settings panel -->
        <div
          v-if="showSettings"
          class="absolute right-0 top-full mt-2 w-72 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50 p-4 flex flex-col gap-4"
        >
          <h3 class="text-sm font-semibold text-gray-900 dark:text-white">Settings</h3>

          <!-- Dark mode toggle -->
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-700 dark:text-gray-300">Dark mode</span>
            <button
              @click="toggleDark"
              class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors focus:outline-none"
              :class="isDark ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'"
            >
              <span
                class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
                :class="isDark ? 'translate-x-4' : 'translate-x-1'"
              />
            </button>
          </div>

          <!-- Company name -->
          <div class="flex flex-col gap-1.5">
            <label class="text-sm text-gray-700 dark:text-gray-300">Display name</label>
            <input
              v-model="editingName"
              type="text"
              placeholder="Your company name"
              class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              @keyup.enter="saveSettings"
            />
            <div class="flex gap-2 justify-end">
              <button
                @click="resetName"
                class="text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
              >Reset to default</button>
              <button
                @click="saveSettings"
                class="px-3 py-1 text-xs font-medium bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
              >Save</button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Backdrop to close settings on outside click -->
    <div v-if="showSettings" @click="showSettings = false" class="fixed inset-0 z-40" />

    <main class="max-w-5xl mx-auto px-6 py-8 flex-1 w-full">
      <RouterView />
    </main>

    <footer class="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-6 py-4 text-center text-xs text-gray-400 dark:text-gray-500">
      Powered by <span class="font-semibold text-gray-500 dark:text-gray-400">TAP·re</span>
      &mdash;
      <a
        href="https://github.com/ParadoxicalFlummox/TAPRE"
        target="_blank"
        rel="noopener noreferrer"
        class="hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
      >
        Source
      </a>
    </footer>
  </div>
</template>
