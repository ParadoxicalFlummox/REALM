import { createRouter, createWebHistory } from 'vue-router'
import PropertiesView from '../views/PropertiesView.vue'
import PropertyDetailView from '../views/PropertyDetailView.vue'
import InsightsView from '../views/InsightsView.vue'
import DealAnalyzerView from '../views/DealAnalyzerView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: PropertiesView },
    { path: '/properties/:id', component: PropertyDetailView },
    { path: '/properties/:id/insights', component: InsightsView },
    { path: '/deals', component: DealAnalyzerView },       // standalone calculator
    { path: '/deals/:id', component: DealAnalyzerView },   // load a saved deal
  ],
})
