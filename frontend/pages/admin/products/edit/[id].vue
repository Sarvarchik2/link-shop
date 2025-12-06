<template>
  <div class="edit-product-page">
    <div class="page-header">
      <NuxtLink to="/admin/products" class="back-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </NuxtLink>
      <h1 class="page-title">Edit Product</h1>
    </div>

    <div v-if="pending" class="loading-state">Loading...</div>

    <div v-else class="form-card">
      <form @submit.prevent="handleSubmit">
        <div class="form-section">
          <h2 class="section-title">Basic Information</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label class="label">Product Name</label>
              <input v-model="form.name" required class="input" />
            </div>
            
            <div class="form-group">
              <label class="label">Price ($)</label>
              <input v-model.number="form.price" type="number" step="0.01" required class="input" />
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
            <textarea v-model="form.description" rows="4" required class="input"></textarea>
          </div>
        </div>

        <div class="form-section">
          <h2 class="section-title">Images</h2>
          
          <!-- Image Upload Area -->
          <div class="images-upload-area">
            <!-- Uploaded Images Preview -->
            <div class="images-preview" v-if="uploadedImages.length > 0">
              <div 
                v-for="(img, index) in uploadedImages" 
                :key="index" 
                class="image-preview-item"
                :class="{ 'main-image': index === 0 }"
              >
                <img :src="img" alt="Product image" />
                <div class="image-actions">
                  <button v-if="index !== 0" type="button" @click="setMainImage(index)" class="btn-set-main" title="Set as main">
                    ⭐
                  </button>
                  <button type="button" @click="removeImage(index)" class="btn-remove-image" title="Remove">
                    ✕
                  </button>
                </div>
                <span v-if="index === 0" class="main-badge">Main</span>
              </div>
            </div>
            
            <!-- Upload Button -->
            <div class="upload-zone" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
              <input 
                ref="fileInput" 
                type="file" 
                accept="image/*" 
                multiple 
                @change="handleFileSelect" 
                class="hidden-input" 
              />
              <div class="upload-content">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                <span class="upload-text">Click or drag images to upload</span>
                <span class="upload-hint">PNG, JPG up to 5MB</span>
              </div>
            </div>
            
            <!-- OR URL Input -->
            <div class="url-input-section">
              <span class="divider-text">or add by URL</span>
              <div class="url-input-row">
                <input v-model="imageUrl" class="input" placeholder="https://example.com/image.jpg" />
                <button type="button" @click="addImageUrl" class="btn-add-url" :disabled="!imageUrl">Add</button>
              </div>
            </div>
          </div>
          
          <p v-if="uploadingImages" class="uploading-text">⏳ Uploading images...</p>
        </div>

        <div class="form-section">
          <h2 class="section-title">Sizes</h2>
          
          <div class="sizes-list">
            <div v-for="(size, index) in sizes" :key="index" class="size-row">
              <input v-model="size.name" class="input size-name-input" placeholder="Size name (e.g. M, 42, One Size)" />
              <input v-model.number="size.stock" type="number" min="0" class="input stock-input" placeholder="Stock" />
              <button type="button" @click="removeSize(index)" class="btn-remove">✕</button>
            </div>
          </div>
          
          <button type="button" @click="addSize" class="btn-add">
            + Add Size
          </button>
          <p class="help-text">Add available sizes with their stock quantities</p>
        </div>

        <div class="form-section">
          <h2 class="section-title">Colors</h2>
          
          <div class="colors-list">
            <div v-for="(color, index) in colors" :key="index" class="color-row">
              <input v-model="color.name" class="input color-name-input" placeholder="Color name" />
              <input v-model="color.hex" type="color" class="color-picker" />
              <input v-model.number="color.stock" type="number" min="0" class="input stock-input" placeholder="Stock" />
              <button type="button" @click="removeColor(index)" class="btn-remove">✕</button>
            </div>
          </div>
          
          <button type="button" @click="addColor" class="btn-add">+ Add Color</button>
          <p class="help-text">Add available colors with their stock quantities</p>
        </div>

        <div class="form-actions">
          <NuxtLink to="/admin/products" class="btn btn-secondary">Cancel</NuxtLink>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Updating...' : 'Update Product' }}
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

const route = useRoute()
const { token } = useAuth()
const productId = route.params.id
const loading = ref(false)
const uploadingImages = ref(false)

const { data: product, pending } = await useFetch(`http://localhost:8000/products/${productId}`, {
  server: false
})

const { data: brands } = await useFetch('http://localhost:8000/brands', { server: false })
const { data: categories } = await useFetch('http://localhost:8000/categories', { server: false })

const fileInput = ref(null)
const uploadedImages = ref([])
const imageUrl = ref('')

const sizes = ref([])
const colors = ref([])

// Size functions
const addSize = () => {
  sizes.value.push({ name: '', stock: 0 })
}

const removeSize = (index) => {
  sizes.value.splice(index, 1)
}

// Color functions
const addColor = () => {
  colors.value.push({ name: '', hex: '#000000', stock: 0 })
}

const removeColor = (index) => {
  colors.value.splice(index, 1)
}

// Image functions
const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = async (event) => {
  const files = event.target.files
  if (files.length > 0) {
    await uploadFiles(files)
  }
}

const handleDrop = async (event) => {
  const files = event.dataTransfer.files
  if (files.length > 0) {
    await uploadFiles(files)
  }
}

const uploadFiles = async (files) => {
  uploadingImages.value = true
  
  for (const file of files) {
    if (file.type.startsWith('image/')) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await $fetch('http://localhost:8000/upload', {
          method: 'POST',
          body: formData
        })
        
        uploadedImages.value.push(response.url)
      } catch (e) {
        console.error('Failed to upload image:', e)
      }
    }
  }
  
  uploadingImages.value = false
}

const addImageUrl = () => {
  if (imageUrl.value.trim()) {
    uploadedImages.value.push(imageUrl.value.trim())
    imageUrl.value = ''
  }
}

const removeImage = (index) => {
  uploadedImages.value.splice(index, 1)
}

const setMainImage = (index) => {
  const [img] = uploadedImages.value.splice(index, 1)
  uploadedImages.value.unshift(img)
}

const form = ref({
  name: '',
  brand: '',
  category: '',
  price: 0,
  description: ''
})

watch(product, (newProduct) => {
  if (newProduct) {
    form.value = {
      name: newProduct.name,
      brand: newProduct.brand,
      category: newProduct.category,
      price: newProduct.price,
      description: newProduct.description || ''
    }
    
    // Parse images
    try {
      uploadedImages.value = newProduct.images ? JSON.parse(newProduct.images) : [newProduct.image_url]
    } catch {
      uploadedImages.value = newProduct.image_url ? [newProduct.image_url] : []
    }
    
    // Parse sizes - now expecting array of objects with name and stock
    try {
      const parsedSizes = newProduct.sizes ? JSON.parse(newProduct.sizes) : []
      // Handle both old format (array of strings) and new format (array of objects)
      sizes.value = parsedSizes.map(s => {
        if (typeof s === 'string') {
          return { name: s, stock: 0 }
        }
        return s
      })
    } catch {
      sizes.value = []
    }
    
    // Parse colors
    try {
      colors.value = newProduct.colors ? JSON.parse(newProduct.colors) : []
    } catch {
      colors.value = []
    }
  }
}, { immediate: true })

const toast = useToast()

const handleSubmit = async () => {
  if (uploadedImages.value.length === 0) {
    toast.warning('Please add at least one image')
    return
  }
  
  loading.value = true
  try {
    // Prepare sizes (filter empty)
    const validSizes = sizes.value.filter(s => s.name.trim())
    
    // Prepare colors (filter empty)
    const validColors = colors.value.filter(c => c.name.trim())
    
    // Calculate total stock
    const totalStock = validSizes.reduce((acc, s) => acc + (s.stock || 0), 0) +
                       validColors.reduce((acc, c) => acc + (c.stock || 0), 0)
    
    const productData = {
      ...form.value,
      image_url: uploadedImages.value[0],
      images: JSON.stringify(uploadedImages.value),
      sizes: validSizes.length > 0 ? JSON.stringify(validSizes) : null,
      colors: validColors.length > 0 ? JSON.stringify(validColors) : null,
      stock: totalStock || 0
    }
    
    await $fetch(`http://localhost:8000/products/${productId}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: productData
    })
    
    toast.success('Product updated successfully!')
    navigateTo('/admin/products')
  } catch (e) {
    console.error(e)
    toast.error('Failed to update product')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.edit-product-page {
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

.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #6B7280;
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
  margin-top: 8px;
}

/* Images Upload */
.images-upload-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.images-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}

.image-preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #E5E7EB;
}

.image-preview-item.main-image {
  border-color: #10B981;
}

.image-preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-actions {
  position: absolute;
  top: 6px;
  right: 6px;
  display: flex;
  gap: 4px;
}

.btn-set-main,
.btn-remove-image {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-set-main {
  background: #FEF3C7;
}

.btn-remove-image {
  background: #FEE2E2;
  color: #DC2626;
}

.main-badge {
  position: absolute;
  bottom: 6px;
  left: 6px;
  background: #10B981;
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
}

.upload-zone {
  border: 2px dashed #D1D5DB;
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #FAFAFA;
}

.upload-zone:hover {
  border-color: #111;
  background: #F5F5F5;
}

.hidden-input {
  display: none;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #6B7280;
}

.upload-text {
  font-weight: 600;
}

.upload-hint {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.url-input-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.divider-text {
  text-align: center;
  font-size: 0.875rem;
  color: #9CA3AF;
}

.url-input-row {
  display: flex;
  gap: 12px;
}

.url-input-row .input {
  flex: 1;
}

.btn-add-url {
  padding: 12px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add-url:disabled {
  background: #D1D5DB;
  cursor: not-allowed;
}

.uploading-text {
  text-align: center;
  color: #6B7280;
  font-size: 0.875rem;
}

/* Sizes & Colors */
.sizes-list,
.colors-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.size-row,
.color-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.size-name-input,
.color-name-input {
  flex: 1;
}

.color-picker {
  width: 50px;
  height: 44px;
  padding: 4px;
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  cursor: pointer;
}

.stock-input {
  width: 100px;
}

.btn-remove {
  width: 44px;
  height: 44px;
  background: #FEE2E2;
  border: none;
  border-radius: 8px;
  color: #DC2626;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-remove:hover {
  background: #FECACA;
}

.btn-add {
  padding: 12px 20px;
  background: #F3F4F6;
  border: 2px dashed #D1D5DB;
  border-radius: 12px;
  color: #6B7280;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  width: 100%;
}

.btn-add:hover {
  background: #E5E7EB;
  border-color: #9CA3AF;
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
  .edit-product-page {
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
  
  .images-preview {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
