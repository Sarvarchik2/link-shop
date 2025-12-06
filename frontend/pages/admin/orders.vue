<template>
  <div class="orders-page">
    <h1 class="page-title">Orders</h1>
    
    <div v-if="!orders || orders.length === 0" class="empty-state">
      <p>No orders found.</p>
    </div>
    
    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header" @click="toggleOrder(order.id)">
          <div class="order-main-info">
            <span class="order-id">#{{ order.id }}</span>
            <span class="order-date">{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="order-customer">
            <span class="customer-name">{{ order.user?.first_name }} {{ order.user?.last_name }}</span>
            <span class="customer-phone">{{ order.user?.phone }}</span>
          </div>
          <div class="order-total">${{ order.total_price.toFixed(2) }}</div>
          <select 
            :value="order.status" 
            @click.stop
            @change="updateStatus(order.id, $event.target.value)"
            class="status-select"
            :class="order.status"
          >
            <option value="pending">Pending</option>
            <option value="processing">Processing</option>
            <option value="shipping">Shipping</option>
            <option value="delivered">Delivered</option>
            <option value="cancelled">Cancelled</option>
          </select>
          <button class="expand-btn" :class="{ expanded: expandedOrder === order.id }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </div>
        
        <div v-if="expandedOrder === order.id" class="order-details">
          <!-- Delivery Info -->
          <div class="detail-section">
            <h3 class="detail-title">📍 Delivery Info</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Recipient</span>
                <span class="detail-value">{{ order.recipient_name || 'N/A' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Phone</span>
                <span class="detail-value">{{ order.delivery_phone || 'N/A' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">City</span>
                <span class="detail-value">{{ order.delivery_city || 'N/A' }}</span>
              </div>
              <div class="detail-item full-width">
                <span class="detail-label">Address</span>
                <span class="detail-value">{{ order.delivery_address || 'N/A' }}</span>
              </div>
            </div>
          </div>
          
          <!-- Payment Info -->
          <div class="detail-section">
            <h3 class="detail-title">💳 Payment</h3>
            <div class="payment-badge" :class="order.payment_method">
              {{ order.payment_method === 'cash' ? 'Cash on Delivery' : 'Card Payment' }}
            </div>
          </div>
          
          <!-- Order Items -->
          <div class="detail-section">
            <h3 class="detail-title">📦 Items ({{ order.items?.length || 0 }})</h3>
            <div class="items-list">
              <div v-for="(item, idx) in order.items" :key="idx" class="order-item">
                <img :src="item.product_image" :alt="item.product_name" class="item-image" />
                <div class="item-info">
                  <span class="item-name">{{ item.product_name }}</span>
                  <div class="item-options" v-if="item.selected_color || item.selected_size">
                    <span v-if="item.selected_color" class="item-option color">{{ item.selected_color }}</span>
                    <span v-if="item.selected_size" class="item-option size">{{ item.selected_size }}</span>
                  </div>
                  <span class="item-meta">Qty: {{ item.quantity }} × ${{ item.price.toFixed(2) }}</span>
                </div>
                <span class="item-total">${{ (item.quantity * item.price).toFixed(2) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Notes -->
          <div v-if="order.notes" class="detail-section">
            <h3 class="detail-title">📝 Notes</h3>
            <p class="notes-text">{{ order.notes }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const { token } = useAuth()
const expandedOrder = ref(null)

const { data: orders, refresh } = await useFetch('http://localhost:8000/admin/orders', {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})

const toggleOrder = (orderId) => {
  expandedOrder.value = expandedOrder.value === orderId ? null : orderId
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const updateStatus = async (id, newStatus) => {
  try {
    await $fetch(`http://localhost:8000/admin/orders/${id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: { status: newStatus }
    })
    refresh()
    useToast().success('Order status updated!')
  } catch (e) {
    useToast().error('Failed to update status')
  }
}
</script>

<style scoped>
.orders-page {
  padding: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .orders-page {
    padding: 32px;
  }
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 24px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  color: #9CA3AF;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.order-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  cursor: pointer;
  transition: background 0.2s;
}

.order-header:hover {
  background: #F9FAFB;
}

.order-main-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 100px;
}

.order-id {
  font-weight: 700;
  font-size: 1rem;
}

.order-date {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.order-customer {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.customer-name {
  font-weight: 600;
}

.customer-phone {
  font-size: 0.875rem;
  color: #6B7280;
}

.order-total {
  font-size: 1.125rem;
  font-weight: 700;
  min-width: 100px;
  text-align: right;
}

.status-select {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  min-width: 120px;
}

.status-select.pending { background: #FFF3E0; color: #EF6C00; }
.status-select.processing { background: #E3F2FD; color: #1565C0; }
.status-select.shipping { background: #FFF8E1; color: #F9A825; }
.status-select.delivered { background: #E8F5E9; color: #2E7D32; }
.status-select.cancelled { background: #FFEBEE; color: #C62828; }

.expand-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #F3F4F6;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.expand-btn.expanded {
  transform: rotate(180deg);
}

.order-details {
  padding: 0 20px 20px;
  border-top: 1px solid #E5E7EB;
  background: #FAFAFA;
}

.detail-section {
  padding: 20px 0;
  border-bottom: 1px solid #E5E7EB;
}

.detail-section:last-child {
  border-bottom: none;
}

.detail-title {
  font-size: 0.875rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #374151;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-label {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.detail-value {
  font-weight: 500;
  color: #111;
}

.payment-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
}

.payment-badge.cash {
  background: #FEF3C7;
  color: #92400E;
}

.payment-badge.card {
  background: #DBEAFE;
  color: #1E40AF;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: white;
  border-radius: 12px;
}

.item-image {
  width: 50px;
  height: 50px;
  object-fit: contain;
  border-radius: 8px;
  background: #F9FAFB;
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name {
  font-weight: 600;
  font-size: 0.875rem;
}

.item-options {
  display: flex;
  gap: 6px;
  margin: 4px 0;
}

.item-option {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.item-option.color {
  background: #E0E7FF;
  color: #3730A3;
}

.item-option.size {
  background: #FEE2E2;
  color: #991B1B;
}

.item-meta {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.item-total {
  font-weight: 700;
}

.notes-text {
  padding: 12px;
  background: white;
  border-radius: 8px;
  font-size: 0.875rem;
  color: #6B7280;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
    margin-bottom: 16px;
  }
  
  .order-card {
    border-radius: 12px;
  }
  
  .order-header {
    flex-wrap: wrap;
    gap: 12px;
    padding: 16px;
  }
  
  .order-main-info {
    min-width: auto;
    flex: 1;
  }
  
  .order-id {
    font-size: 0.9rem;
  }
  
  .order-customer {
    order: 3;
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
    padding-top: 12px;
    border-top: 1px solid #F3F4F6;
  }
  
  .order-total {
    min-width: auto;
    font-size: 1rem;
    text-align: left;
  }
  
  .status-select {
    min-width: 100px;
    font-size: 0.7rem;
    padding: 6px 12px;
  }
  
  .expand-btn {
    width: 32px;
    height: 32px;
  }
  
  .order-details {
    padding: 0 16px 16px;
  }
  
  .detail-section {
    padding: 16px 0;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .order-item {
    padding: 10px;
  }
  
  .item-image {
    width: 40px;
    height: 40px;
  }
  
  .item-name {
    font-size: 0.8rem;
  }
}
</style>
