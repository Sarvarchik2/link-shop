<template>
  <div class="product-page">
    <AppHeader />
    
    <main class="container py-8">
      <div v-if="pending" class="text-center py-12">
        <div class="loading-spinner"></div>
        <p class="mt-4 text-gray-400">Loading...</p>
      </div>

      <div v-else-if="product" class="product-content">
        <div class="product-gallery">
          <div class="main-image">
            <img :src="selectedImage || product.image_url" :alt="product.name" />
          </div>
          <div v-if="productImages.length > 1" class="thumbnail-images">
            <div 
              v-for="(img, index) in productImages" 
              :key="index" 
              class="thumbnail"
              :class="{ active: selectedImage === img }"
              @click="selectedImage = img"
            >
              <img :src="img" :alt="`${product.name} ${index + 1}`" />
            </div>
          </div>
        </div>

        <div class="product-details">
          <div class="product-category">{{ product.category }}</div>
          <h1 class="product-title">{{ product.name }}</h1>

          <div class="product-price-section">
            <div class="product-price">${{ product.price.toFixed(2) }}</div>
            <div v-if="product.stock === 0" class="stock-badge out-of-stock">SOLD OUT</div>
            <div v-else-if="product.stock <= 5" class="stock-badge low-stock">Only {{ product.stock }} left!</div>
            <div v-else class="stock-badge in-stock">In Stock ({{ product.stock }})</div>
          </div>

          <div v-if="productSizes.length > 0" class="size-selector">
            <h3 class="section-title">Select Size</h3>
            <div class="sizes">
              <button 
                v-for="size in productSizes" 
                :key="size" 
                class="size-btn"
                :class="{ active: selectedSize === size }"
                @click="selectedSize = size"
              >
                {{ size }}
              </button>
            </div>
          </div>

          <div class="product-description">
            <h3 class="section-title">Description</h3>
            <p>{{ product.description }}</p>
          </div>

          <div class="product-meta">
            <div class="meta-item">
              <span class="meta-label">Brand:</span>
              <span class="meta-value">{{ product.brand }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Category:</span>
              <span class="meta-value">{{ product.category }}</span>
            </div>
          </div>

          <div class="product-actions">
            <button 
              @click="addToCart" 
              class="btn-add-cart"
              :disabled="product.stock === 0"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
              {{ product.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}
            </button>
            <button @click="toggleFavorite" class="btn-favorite" :class="{ active: product.is_favorite }">
              <svg width="20" height="20" viewBox="0 0 24 24" :fill="product.is_favorite ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const route = useRoute()
const cart = useCart()
const { user } = useAuth()

const { data: product, pending, refresh } = await useFetch(`http://localhost:8000/products/${route.params.id}`, {
  server: false
})

const selectedImage = ref(null)
const selectedSize = ref(null)

const productImages = computed(() => {
  if (!product.value) return []
  try {
    const images = product.value.images ? JSON.parse(product.value.images) : []
    return images.length > 0 ? images : [product.value.image_url]
  } catch {
    return [product.value.image_url]
  }
})

const productSizes = computed(() => {
  if (!product.value) return []
  try {
    return product.value.sizes ? JSON.parse(product.value.sizes) : []
  } catch {
    return []
  }
})

const addToCart = () => {
  if (product.value && product.value.stock > 0) {
    cart.addItem(product.value)
    alert('Added to cart!')
  }
}

const toggleFavorite = async () => {
  // Check if user is logged in
  if (!user.value) {
    alert('Please login to add items to favorites')
    navigateTo('/login')
    return
  }
  
  try {
    await $fetch(`http://localhost:8000/products/${route.params.id}/favorite`, { method: 'POST' })
    refresh()
  } catch (e) {
    console.error(e)
  }
}
</script>

<style scoped>
.product-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.product-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.product-gallery {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.main-image {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
}

.thumbnail-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 12px;
}

.thumbnail {
  background: white;
  border-radius: 12px;
  padding: 12px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.thumbnail:hover,
.thumbnail.active {
  border-color: #111;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.product-category {
  font-size: 0.875rem;
  color: #9CA3AF;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.product-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #111;
  line-height: 1.2;
}

.product-price-section {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.product-price {
  font-size: 2.5rem;
  font-weight: 800;
  color: #111;
}

.stock-badge {
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
}

.in-stock {
  background: #D1FAE5;
  color: #065F46;
}

.low-stock {
  background: #FEF3C7;
  color: #92400E;
}

.out-of-stock {
  background: #FEE2E2;
  color: #991B1B;
}

.size-selector {
  padding: 24px 0;
  border-top: 1px solid #E5E7EB;
  border-bottom: 1px solid #E5E7EB;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #111;
}

.sizes {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.size-btn {
  min-width: 60px;
  padding: 12px 20px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  background: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.size-btn:hover {
  border-color: #111;
}

.size-btn.active {
  background: #111;
  color: white;
  border-color: #111;
}

.product-description {
  padding: 24px 0;
}

.product-description p {
  color: #6B7280;
  line-height: 1.6;
}

.product-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.meta-item {
  display: flex;
  gap: 8px;
}

.meta-label {
  font-weight: 600;
  color: #6B7280;
}

.meta-value {
  color: #111;
  font-weight: 500;
}

.product-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.btn-add-cart {
  flex: 1;
  padding: 16px 32px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  transition: all 0.2s;
}

.btn-add-cart:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
}

.btn-add-cart:disabled {
  background: #9CA3AF;
  cursor: not-allowed;
}

.btn-favorite {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: white;
  border: 2px solid #E5E7EB;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: #9CA3AF;
}

.btn-favorite:hover,
.btn-favorite.active {
  border-color: #EF4444;
  color: #EF4444;
  background: #FEF2F2;
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

@media (min-width: 768px) {
  .product-content {
    grid-template-columns: 1fr 1fr;
  }
  
  .product-title {
    font-size: 3rem;
  }
}

@media (max-width: 767px) {
  .main-image {
    padding: 24px;
  }
  
  .product-title {
    font-size: 1.75rem;
  }
  
  .product-price {
    font-size: 2rem;
  }
  
  .btn-add-cart {
    padding: 14px 24px;
  }
}
</style>
