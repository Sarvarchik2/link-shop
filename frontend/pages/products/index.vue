<template>
  <div class="products-page">
    <AppHeader />
    
    <main class="container py-8">
      <h1 class="page-title mb-8">All Products</h1>
      
      <div v-if="pending" class="text-center py-12">
        <div class="loading-spinner"></div>
        <p class="mt-4 text-gray-400">Loading products...</p>
      </div>
      
      <div v-else class="products-grid">
        <ProductCard v-for="product in products" :key="product.id" :product="product" />
      </div>
    </main>
  </div>
</template>

<script setup>
const { data: products, pending } = await useFetch('http://localhost:8000/products', {
  server: false
})
</script>

<style scoped>
.products-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 80px;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}

@media (min-width: 1200px) {
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
