import client from './client'

export const getInsights = (propertyId, { startDate, endDate, targetProfit, numTenants } = {}) =>
  client.get(`/dashboard/insights/${propertyId}`, {
    params: {
      start_date: startDate || undefined,
      end_date: endDate || undefined,
      target_profit: targetProfit || undefined,
      num_tenants: numTenants || undefined,
    },
  }).then(r => r.data)
