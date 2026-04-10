import { createRouter, createWebHistory } from 'vue-router'
import PortfolioView from '../views/PortfolioView.vue'
import PropertiesView from '../views/PropertiesView.vue'
import PropertyDetailView from '../views/PropertyDetailView.vue'
import InsightsView from '../views/InsightsView.vue'
import DealAnalyzerView from '../views/DealAnalyzerView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: PortfolioView },              // portfolio dashboard
    { path: '/properties', component: PropertiesView },   // properties list
    { path: '/properties/:id', component: PropertyDetailView },
    { path: '/properties/:id/insights', component: InsightsView },
    { path: '/deals', component: DealAnalyzerView },       // standalone calculator
    { path: '/deals/:id', component: DealAnalyzerView },   // load a saved deal
  ],
})
