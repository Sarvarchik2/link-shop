<template>
  <div class="home-page">
    <AppHeader />
    
    <main class="container py-8">
      <!-- Hero Section -->
      <div class="hero-card mb-8">
        <div class="hero-content">
          <div class="badge">NEW ARRIVAL</div>
          <h1 class="hero-title">Ray-Ban Meta<br/>Smart Glasses</h1>
          <p class="hero-price">Starting from $299</p>
          <button class="hero-btn">Shop Now</button>
        </div>
        <div class="hero-image">
          <img src="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=800&auto=format&fit=crop" alt="Smart Glasses" />
        </div>
      </div>

      <!-- Brand Filters -->
      <section class="mb-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="section-title">Shop by Brand</h2>
          <button class="text-sm font-semibold text-gray-500 hover:text-black">View All →</button>
        </div>
        <div class="brand-grid">
          <button 
            v-for="brand in brands" 
            :key="brand.id"
            class="brand-card"
            :class="{ active: selectedBrand === brand.name }"
            @click="selectedBrand = selectedBrand === brand.name ? null : brand.name"
          >
            <div class="brand-logo-wrapper">
              <img :src="brand.logo_url" :alt="brand.name" class="brand-logo-img" />
            </div>
            <span class="brand-name-text">{{ brand.name }}</span>
          </button>
        </div>
      </section>

      <!-- Products Grid -->
      <section class="mb-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="section-title">
            {{ selectedBrand ? `${selectedBrand} Collection` : 'Featured Products' }}
          </h2>
          <div class="flex gap-2">
            <button class="filter-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line></svg>
              Filters
            </button>
            <button class="filter-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
              Sort
            </button>
          </div>
        </div>
        <div v-if="pending" class="text-center py-12 text-gray-400">
          <div class="loading-spinner"></div>
          <p class="mt-4">Loading products...</p>
        </div>
        <div v-else class="products-grid">
          <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
const selectedBrand = ref(null)
const { data: brands } = await useFetch('http://localhost:8000/brands', { server: false })
const { data: products, pending } = await useFetch('http://localhost:8000/products', {
  server: false
})

const filteredProducts = computed(() => {
  if (!products.value) return []
  if (!selectedBrand.value) return products.value
  return products.value.filter(p => p.brand === selectedBrand.value)
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #FAFAFA;
}

.hero-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 32px;
  padding: 48px;
  color: white;
  position: relative;
  overflow: hidden;
  min-height: 400px;
  display: flex;
  align-items: center;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.hero-content {
  z-index: 2;
  max-width: 500px;
}

.badge {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  color: white;
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-block;
  margin-bottom: 20px;
  border: 1px solid rgba(255,255,255,0.2);
  letter-spacing: 1px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 16px;
  letter-spacing: -1px;
}

.hero-price {
  font-size: 1.25rem;
  font-weight: 500;
  opacity: 0.9;
  margin-bottom: 32px;
}

.hero-btn {
  background: white;
  color: #111;
  padding: 16px 40px;
  border-radius: 50px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(255,255,255,0.2);
}

.hero-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255,255,255,0.3);
}

.hero-image {
  position: absolute;
  right: -50px;
  top: 50%;
  transform: translateY(-50%) rotate(-10deg);
  width: 50%;
  height: 120%;
  opacity: 0.3;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111;
  letter-spacing: -0.5px;
}

.brand-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.brand-card {
  background: white;
  border: 2px solid #f0f0f0;
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.brand-card:hover {
  border-color: #111;
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

.brand-card.active {
  background: #111;
  border-color: #111;
  color: white;
}

.brand-logo-wrapper {
  width: 80px;
  height: 80px;
  background: #f9f9f9;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.brand-card.active .brand-logo-wrapper {
  background: white;
}

.brand-logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand-name-text {
  font-weight: 700;
  font-size: 0.95rem;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  background: white;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: #111;
  background: #111;
  color: white;
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
  .hero-card {
    padding: 32px 24px;
    min-height: 300px;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-image {
    opacity: 0.15;
    width: 70%;
  }
  
  .brand-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
}

@media (min-width: 1200px) {
  .hero-image {
    opacity: 0.5;
  }
  
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
