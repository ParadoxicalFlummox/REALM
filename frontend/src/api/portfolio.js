import client from './client'

export const getPortfolioSummary = () =>
  client.get('/portfolio/summary').then(r => r.data)
