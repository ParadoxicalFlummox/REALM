import client from './client'

export const getLoans = (propertyId) =>
  client.get('/loans/', { params: { property_id: propertyId } }).then(r => r.data)

export const createLoan = (data) =>
  client.post('/loans/', data).then(r => r.data)

export const updateLoan = (id, data) =>
  client.patch(`/loans/${id}`, data).then(r => r.data)

export const deleteLoan = (id) =>
  client.delete(`/loans/${id}`).then(r => r.data)

export const getEquity = (propertyId) =>
  client.get(`/properties/${propertyId}/equity`).then(r => r.data)
