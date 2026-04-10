import client from './client'

export const getTransactions = (offset = 0, limit = 50) =>
  client.get('/transactions/', { params: { offset, limit } }).then(r => r.data)

export const getTransaction = (id) =>
  client.get(`/transactions/${id}`).then(r => r.data)

export const createTransaction = (data) =>
  client.post('/transactions/', data).then(r => r.data)

export const updateTransaction = (id, data) =>
  client.patch(`/transactions/${id}`, data).then(r => r.data)

export const deleteTransaction = (id) =>
  client.delete(`/transactions/${id}`).then(r => r.data)

export const getTaxCategories = () =>
  client.get('/transactions/tax-categories').then(r => r.data)
