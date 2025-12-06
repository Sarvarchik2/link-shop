<template>
  <div class="orders-page">
    <h1 class="page-title">Orders</h1>
    
    <div class="card">
      <div v-if="!orders || orders.length === 0" class="text-center py-8 text-gray-500">
        No orders found.
      </div>
      <table v-else class="w-full">
        <thead>
          <tr class="text-left border-b">
            <th class="pb-4 font-semibold text-gray-500">Order ID</th>
            <th class="pb-4 font-semibold text-gray-500">User ID</th>
            <th class="pb-4 font-semibold text-gray-500">Date</th>
            <th class="pb-4 font-semibold text-gray-500">Total</th>
            <th class="pb-4 font-semibold text-gray-500">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id" class="border-b last:border-0">
            <td class="py-4 font-medium">#{{ order.id }}</td>
            <td class="py-4">{{ order.user_id }}</td>
            <td class="py-4 text-gray-500">{{ new Date(order.created_at).toLocaleDateString() }}</td>
            <td class="py-4 font-bold">${{ order.total_price.toFixed(2) }}</td>
            <td class="py-4">
              <select 
                :value="order.status" 
                @change="updateStatus(order.id, $event.target.value)"
                class="status-select"
                :class="order.status.toLowerCase().replace(' ', '-')"
              >
                <option value="pending">Pending</option>
                <option value="processing">Processing</option>
                <option value="shipping">Shipping</option>
                <option value="delivery">Delivery</option>
                <option value="done">Done</option>
                <option value="cancel">Cancel</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin'
})

const { token } = useAuth()
const { data: orders, refresh } = await useFetch('http://localhost:8000/admin/orders', {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})

const updateStatus = async (id, newStatus) => {
  try {
    await $fetch(`http://localhost:8000/admin/orders/${id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: { status: newStatus }
    })
    refresh()
  } catch (e) {
    alert('Failed to update status')
  }
}
</script>

<style scoped>
.page-title {
  font-size: 2rem;
  font-weight: 800;
}
.card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.status-select {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  appearance: none; /* Remove default arrow in some browsers if desired, or keep it */
}
/* Status Colors */
.status-select.pending { background: #FFF3E0; color: #EF6C00; }
.status-select.processing { background: #E3F2FD; color: #1565C0; }
.status-select.shipping { background: #FFF8E1; color: #FBC02D; }
.status-select.delivery { background: #E8F5E9; color: #2E7D32; }
.status-select.done { background: #E8F5E9; color: #2E7D32; }
.status-select.cancel { background: #FFEBEE; color: #C62828; }
</style>
