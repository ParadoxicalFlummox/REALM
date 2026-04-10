<script setup>
import { ref } from 'vue'
// App.vue is the root — it's always rendered.
// RouterLink = a nav link that doesn't reload the page.
// RouterView = a slot that renders whichever view matches the current URL.
// import.meta.env.VITE_* exposes variables from the frontend .env file.
const companyName = import.meta.env.VITE_COMPANY_NAME || 'TAPRE'
const isDark = ref(localStorage.getItem('theme') === 'dark')

function toggleDark() {
  isDark.value = !isDark.value
  // Tailwind watches for .dark on <html> meaning this is what triggers all dark: classes
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// Apply the saved preferences on load
if (isDark.value) document.documentElement.classList.add('dark')
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col">
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
      <button @click="toggleDark" class="ml-auto text-sm text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
        {{ isDark ? '☀️ Light' : '🌙 Dark' }}
      </button>
    </nav>

    <main class="max-w-5xl mx-auto px-6 py-8 flex-1 w-full">
      <RouterView />
    </main>

    <footer class="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-6 py-4 text-center text-xs text-gray-400 dark:text-gray-500">
      Powered by <span class="font-semibold text-gray-500 dark:text-gray-400">TAPRE</span>
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
