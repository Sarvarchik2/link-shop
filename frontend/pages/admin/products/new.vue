<template>
  <div class="add-product-page">
    <div class="page-header">
      <NuxtLink to="/admin/products" class="back-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </NuxtLink>
      <h1 class="page-title">Add New Product</h1>
    </div>
    
    <div class="form-card">
      <form @submit.prevent="handleSubmit">
        <div class="form-section">
          <h2 class="section-title">Basic Information</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label class="label">Product Name</label>
              <input v-model="form.name" required class="input" placeholder="e.g. Ray-Ban Wayfarer" />
            </div>
            
            <div class="form-group">
              <label class="label">Price ($)</label>
              <input v-model.number="form.price" type="number" step="0.01" required class="input" placeholder="0.00" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="label">Brand</label>
              <select v-model="form.brand" required class="input">
                <option value="">Select Brand</option>
                <option v-for="brand in brands" :key="brand.id" :value="brand.name">{{ brand.name }}</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="label">Category</label>
              <select v-model="form.category" required class="input">
                <option value="">Select Category</option>
                <option v-for="category in categories" :key="category.id" :value="category.name">{{ category.name }}</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="label">Description</label>
            <textarea v-model="form.description" rows="4" required class="input" placeholder="Product description..."></textarea>
          </div>
        </div>

        <div class="form-section">
          <h2 class="section-title">Images</h2>
          
          <div class="form-group">
            <label class="label">Main Image URL</label>
            <input v-model="form.image_url" required class="input" placeholder="https://..." />
          </div>

          <div class="form-group">
            <label class="label">Additional Images (one per line)</label>
            <textarea 
              v-model="additionalImages" 
              rows="3" 
              class="input" 
              placeholder="https://image1.jpg&#10;https://image2.jpg&#10;https://image3.jpg"
            ></textarea>
            <p class="help-text">Enter each image URL on a new line</p>
          </div>
        </div>

        <div class="form-section">
          <h2 class="section-title">Inventory & Sizes</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label class="label">Stock Quantity</label>
              <input v-model.number="form.stock" type="number" min="0" required class="input" placeholder="0" />
              <p class="help-text">Set to 0 for out of stock</p>
            </div>
            
            <div class="form-group">
              <label class="label">Available Sizes</label>
              <div class="sizes-input">
                <label v-for="size in availableSizes" :key="size" class="size-checkbox">
                  <input type="checkbox" :value="size" v-model="selectedSizes" />
                  <span>{{ size }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <NuxtLink to="/admin/products" class="btn btn-secondary">Cancel</NuxtLink>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Product' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const { token } = useAuth()
const loading = ref(false)
const { data: brands } = await useFetch('http://localhost:8000/brands', { server: false })
const { data: categories } = await useFetch('http://localhost:8000/categories', { server: false })

const availableSizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
const selectedSizes = ref([])
const additionalImages = ref('')

const form = reactive({
  name: '',
  brand: '',
  category: '',
  price: 0,
  image_url: '',
  description: '',
  stock: 0,
  images: null,
  sizes: null
})

const handleSubmit = async () => {
  loading.value = true
  try {
    // Prepare images array
    const imagesArray = [form.image_url]
    if (additionalImages.value.trim()) {
      const additionalUrls = additionalImages.value.split('\n').filter(url => url.trim())
      imagesArray.push(...additionalUrls)
    }
    
    // Prepare form data
    const productData = {
      ...form,
      images: JSON.stringify(imagesArray),
      sizes: selectedSizes.value.length > 0 ? JSON.stringify(selectedSizes.value) : null
    }
    
    await $fetch('http://localhost:8000/products', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: productData
    })
    
    navigateTo('/admin/products')
  } catch (e) {
    console.error(e)
    alert('Failed to create product')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.add-product-page {
  padding: 32px;
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.back-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: white;
  border: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  color: #111;
}

.back-btn:hover {
  background: #111;
  color: white;
}

.page-title {
  font-size: 2rem;
  font-weight: 900;
  color: #111;
  margin: 0;
}

.form-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.form-section {
  margin-bottom: 40px;
  padding-bottom: 40px;
  border-bottom: 1px solid #E5E7EB;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  background: #F9FAFB;
}

.input:focus {
  outline: none;
  border-color: #111;
  background: white;
}

.help-text {
  font-size: 0.75rem;
  color: #9CA3AF;
  margin-top: 4px;
}

.sizes-input {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.size-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.size-checkbox:hover {
  border-color: #111;
}

.size-checkbox input:checked + span {
  font-weight: 700;
}

.size-checkbox input {
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid #E5E7EB;
}

.btn {
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
  display: inline-block;
  font-size: 1rem;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #000;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #F3F4F6;
  color: #111;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

@media (max-width: 768px) {
  .add-product-page {
    padding: 20px;
  }
  
  .form-card {
    padding: 24px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}
</style>
