<template>
  <div class="products-page">
    <div class="flex justify-between items-center mb-8">
      <h1 class="page-title mb-0">Products</h1>
      <NuxtLink to="/admin/products/new" class="btn btn-primary">
        + Add Product
      </NuxtLink>
    </div>
    
    <div v-if="!products || products.length === 0" class="empty-state">
      <p>No products found</p>
    </div>
    
    <div v-else class="products-grid">
      <div v-for="product in products" :key="product.id" class="product-card">
        <div class="product-image">
          <img :src="product.image_url" :alt="product.name" />
        </div>
        <div class="product-info">
          <div class="product-category">{{ product.category }}</div>
          <h3 class="product-name">{{ product.name }}</h3>
          <div class="product-brand">{{ product.brand }}</div>
          <div class="product-footer">
            <div class="product-price">${{ product.price.toFixed(2) }}</div>
            <div class="product-actions">
              <NuxtLink :to="`/admin/products/edit/${product.id}`" class="btn-edit">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
              </NuxtLink>
              <button @click="deleteProduct(product.id)" class="btn-delete">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
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
const { data: products, refresh } = await useFetch('http://localhost:8000/products', {
  server: false
})

const deleteProduct = async (id) => {
  if (!confirm('Are you sure you want to delete this product?')) return
  try {
    await $fetch(`http://localhost:8000/products/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    refresh()
  } catch (e) {
    alert('Failed to delete product')
  }
}
</script>

<style scoped>
.page-title {
  font-size: 2rem;
  font-weight: 800;
}

.btn {
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover {
  background: #000;
  transform: translateY(-1px);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #9CA3AF;
  font-size: 1.125rem;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.product-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.08);
}

.product-image {
  background: #F9FAFB;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
}

.product-info {
  padding: 20px;
}

.product-category {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.product-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 4px;
  line-height: 1.3;
}

.product-brand {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 16px;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.product-price {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.btn-edit,
.btn-delete {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  text-decoration: none;
}

.btn-edit {
  background: #EFF6FF;
  color: #3B82F6;
}

.btn-edit:hover {
  background: #3B82F6;
  color: white;
}

.btn-delete {
  background: #FEF2F2;
  color: #EF4444;
}

.btn-delete:hover {
  background: #EF4444;
  color: white;
  transform: scale(1.05);
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .product-card {
    border-radius: 16px;
  }
  
  .product-info {
    padding: 16px;
  }
}

@media (min-width: 1200px) {
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
