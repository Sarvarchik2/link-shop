<template>
  <div class="cart-page">
    <AppHeader />
    
    <main class="container py-8">
      <div class="flex items-center gap-4 mb-8">
        <button @click="$router.back()" class="back-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <h1 class="page-title mb-0">Shopping Cart</h1>
      </div>

      <div v-if="cart.items.length === 0" class="empty-cart">
        <div class="empty-icon">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
        </div>
        <h2 class="empty-title">Your cart is empty</h2>
        <p class="empty-text">Add some products to get started</p>
        <NuxtLink to="/" class="btn-shop">Continue Shopping</NuxtLink>
      </div>

      <div v-else class="cart-content">
        <div class="cart-items">
          <div v-for="item in cart.items" :key="item.id" class="cart-item">
            <div class="item-image">
              <img :src="item.image_url" :alt="item.name" />
            </div>
            <div class="item-details">
              <h3 class="item-name">{{ item.name }}</h3>
              <p class="item-category">{{ item.category }}</p>
              <p class="item-price">${{ item.price.toFixed(2) }}</p>
            </div>
            <div class="item-actions">
              <div class="quantity-control">
                <button @click="cart.updateQuantity(item.id, item.quantity - 1)" class="qty-btn">-</button>
                <span class="qty-value">{{ item.quantity }}</span>
                <button @click="cart.updateQuantity(item.id, item.quantity + 1)" class="qty-btn">+</button>
              </div>
              <button @click="cart.removeItem(item.id)" class="btn-remove">Remove</button>
            </div>
          </div>
        </div>

        <div class="cart-summary">
          <h2 class="summary-title">Order Summary</h2>
          <div class="summary-row">
            <span>Subtotal</span>
            <span>${{ cart.totalPrice.toFixed(2) }}</span>
          </div>
          <div class="summary-row">
            <span>Shipping</span>
            <span>Free</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-total">
            <span>Total</span>
            <span>${{ cart.totalPrice.toFixed(2) }}</span>
          </div>
          <button @click="handleCheckout" class="btn-checkout">Proceed to Checkout</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const cart = useCart()
const { token } = useAuth()

const handleCheckout = async () => {
  if (!token.value) {
    alert('Please login to checkout')
    navigateTo('/login')
    return
  }

  try {
    const items = cart.items.map(item => ({
      product_id: item.id,
      quantity: item.quantity
    }))

    await $fetch('http://localhost:8000/orders', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: { items }
    })

    cart.clearCart()
    alert('Order placed successfully!')
    navigateTo('/orders')
  } catch (e) {
    console.error(e)
    alert('Failed to place order')
  }
}
</script>

<style scoped>
.cart-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
}

.back-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: white;
  border: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #111;
  color: white;
}

.empty-cart {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  color: #D1D5DB;
  margin-bottom: 24px;
}

.empty-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 12px;
}

.empty-text {
  color: #6B7280;
  margin-bottom: 32px;
}

.btn-shop {
  display: inline-block;
  padding: 14px 32px;
  background: #111;
  color: white;
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-shop:hover {
  background: #000;
  transform: translateY(-2px);
}

.cart-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cart-item {
  background: white;
  border-radius: 20px;
  padding: 20px;
  display: grid;
  grid-template-columns: 100px 1fr auto;
  gap: 20px;
  align-items: center;
}

.item-image {
  width: 100px;
  height: 100px;
  background: #F9FAFB;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
}

.item-details {
  flex: 1;
}

.item-name {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.item-category {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 8px;
}

.item-price {
  font-size: 1.125rem;
  font-weight: 800;
  color: #111;
}

.item-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-end;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #F9FAFB;
  border-radius: 10px;
  padding: 4px;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: white;
  border: none;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.2s;
}

.qty-btn:hover {
  background: #111;
  color: white;
}

.qty-value {
  min-width: 32px;
  text-align: center;
  font-weight: 600;
}

.btn-remove {
  color: #EF4444;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
}

.btn-remove:hover {
  text-decoration: underline;
}

.cart-summary {
  background: white;
  border-radius: 20px;
  padding: 24px;
  height: fit-content;
  position: sticky;
  top: 100px;
}

.summary-title {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 24px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  color: #6B7280;
}

.summary-divider {
  height: 1px;
  background: #E5E7EB;
  margin: 20px 0;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 24px;
}

.btn-checkout {
  width: 100%;
  padding: 16px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-checkout:hover {
  background: #000;
  transform: translateY(-2px);
}

@media (min-width: 1024px) {
  .cart-content {
    grid-template-columns: 2fr 1fr;
  }
}

@media (max-width: 640px) {
  .cart-item {
    grid-template-columns: 80px 1fr;
    gap: 12px;
  }
  
  .item-actions {
    grid-column: 1 / -1;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
