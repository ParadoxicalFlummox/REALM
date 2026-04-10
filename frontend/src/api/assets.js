import client from './client'

export const getAssets = (offset = 0, limit = 50) =>
  client.get('/assets/', { params: { offset, limit } }).then(r => r.data)

export const getAsset = (id) =>
  client.get(`/assets/${id}`).then(r => r.data)

export const getAssetCategories = () =>
  client.get('/assets/categories').then(r => r.data)

export const createAsset = (data) =>
  client.post('/assets/', data).then(r => r.data)

export const updateAsset = (id, data) =>
  client.patch(`/assets/${id}`, data).then(r => r.data)

export const deleteAsset = (id) =>
  client.delete(`/assets/${id}`).then(r => r.data)
