import client from './client'

export const calculateDeal = (data) =>
  client.post('/deals/calculate', data).then(r => r.data)

export const saveDeal = (data) =>
  client.post('/deals/', data).then(r => r.data)

export const getDeals = (propertyId = null) =>
  client.get('/deals/', { params: propertyId ? { property_id: propertyId } : {} }).then(r => r.data)

export const getDeal = (id) =>
  client.get(`/deals/${id}`).then(r => r.data)

export const deleteDeal = (id) =>
  client.delete(`/deals/${id}`).then(r => r.data)
