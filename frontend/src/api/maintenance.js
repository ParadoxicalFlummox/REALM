import client from './client'

export const getMaintenanceCategories = () =>
  client.get('/maintenance/categories').then(r => r.data)

export const getMaintenanceRecords = (propertyId) =>
  client.get('/maintenance/', { params: { property_id: propertyId } }).then(r => r.data)

export const createMaintenanceRecord = (data) =>
  client.post('/maintenance/', data).then(r => r.data)

export const updateMaintenanceRecord = (id, data) =>
  client.patch(`/maintenance/${id}`, data).then(r => r.data)

export const deleteMaintenanceRecord = (id) =>
  client.delete(`/maintenance/${id}`).then(r => r.data)
