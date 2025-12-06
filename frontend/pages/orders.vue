<template>
  <div class="orders-page container py-8">
    <div class="flex items-center gap-4 mb-8">
      <button @click="$router.back()" class="p-2 hover:bg-gray-100 rounded-full">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
      </button>
      <h1 class="text-2xl font-bold mb-0">Your Order</h1>
    </div>

    <!-- Search -->
    <div class="relative mb-6">
      <input type="text" placeholder="Search your order ID" class="w-full bg-gray-50 border-none rounded-full py-4 px-12 text-gray-600 focus:ring-2 focus:ring-black" />
      <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    </div>

    <!-- Tabs -->
    <div class="flex gap-4 overflow-x-auto pb-4 mb-6 scrollbar-hide">
      <button 
        v-for="status in statuses" 
        :key="status"
        class="whitespace-nowrap px-4 py-2 rounded-full font-bold text-sm transition-colors"
        :class="selectedStatus === status ? 'bg-black text-white' : 'text-gray-400 hover:text-black'"
        @click="selectedStatus = status"
      >
        {{ status }}
      </button>
    </div>

    <!-- Order List -->
    <div v-if="pending" class="text-center py-12">Loading orders...</div>
    <div v-else-if="filteredOrders.length === 0" class="text-center py-12 text-gray-500">
      No orders found.
    </div>
    <div v-else class="space-y-6">
      <div v-for="order in filteredOrders" :key="order.id" class="bg-white rounded-2xl p-4 shadow-sm border border-gray-50">
        <div class="flex justify-between items-start mb-4">
          <div class="text-xs text-gray-400">#{{ order.id }}</div>
          <span class="status-badge" :class="order.status.toLowerCase().replace(' ', '-')">{{ order.status }}</span>
        </div>

        <div v-for="item in order.items" :key="item.product_id" class="flex gap-4 mb-4 last:mb-0">
          <div class="w-20 h-20 bg-gray-50 rounded-xl flex items-center justify-center p-2 flex-shrink-0">
            <img :src="item.product_image" class="w-full h-full object-contain mix-blend-multiply" />
          </div>
          <div class="flex-1">
            <h3 class="font-bold text-sm mb-1">{{ item.product_name }}</h3>
            <div class="text-xs text-gray-400 mb-2">Quantity: {{ item.quantity }}</div>
            <div class="font-bold text-sm">${{ item.price.toFixed(2) }}</div>
          </div>
        </div>

        <div class="border-t pt-3 mt-2 flex justify-between items-center">
          <span class="text-sm font-medium text-gray-500">Total Amount</span>
          <span class="font-bold text-lg">${{ order.total_price.toFixed(2) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

const { token } = useAuth()
const { data: orders, pending } = await useFetch('http://localhost:8000/orders/me', {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})

const statuses = ['All Status', 'Pending', 'Processing', 'Shipping', 'Delivery', 'Done', 'Cancel']
const selectedStatus = ref('All Status')

const filteredOrders = computed(() => {
  if (!orders.value) return []
  if (selectedStatus.value === 'All Status') return orders.value
  return orders.value.filter(o => o.status.toLowerCase() === selectedStatus.value.toLowerCase())
})
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  background: #f5f5f5;
  color: #666;
}
.status-badge.pending { background: #FFF3E0; color: #EF6C00; }
.status-badge.shipping { background: #FFF8E1; color: #FBC02D; }
.status-badge.delivery { background: #E8F5E9; color: #2E7D32; }
.status-badge.cancel { background: #FFEBEE; color: #C62828; }
.status-badge.done { background: #E3F2FD; color: #1565C0; }
</style>
