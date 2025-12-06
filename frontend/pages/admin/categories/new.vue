<template>
  <div class="add-category-page">
    <div class="flex items-center gap-4 mb-8">
      <NuxtLink to="/admin/categories" class="text-gray-500 hover:text-black">
        ← Back
      </NuxtLink>
      <h1 class="page-title mb-0">Add New Category</h1>
    </div>
    
    <div class="card max-w-lg">
      <form @submit.prevent="handleSubmit" class="grid gap-6">
        <div>
          <label class="label">Category Name</label>
          <input v-model="form.name" required class="input" placeholder="e.g. Sunglasses" />
        </div>

        <div>
          <label class="label">Image URL</label>
          <input v-model="form.image_url" required class="input" placeholder="https://..." />
        </div>

        <div class="flex justify-end gap-4 mt-4">
          <NuxtLink to="/admin/categories" class="btn btn-outline">Cancel</NuxtLink>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Category' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin'
})

const { token } = useAuth()
const loading = ref(false)
const form = reactive({
  name: '',
  image_url: ''
})

const handleSubmit = async () => {
  loading.value = true
  try {
    await $fetch('http://localhost:8000/categories', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: form
    })
    useToast().success('Category created successfully!')
    navigateTo('/admin/categories')
  } catch (e) {
    useToast().error('Failed to create category')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-title {
  font-size: 1.5rem;
  font-weight: 800;
}
.card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}
.input {
  width: 100%;
  padding: 12px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #f9f9f9;
  transition: all 0.2s;
}
.input:focus {
  outline: none;
  border-color: #111;
  background: white;
}
.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
.btn-primary {
  background: #111;
  color: white;
  border: none;
}
.btn-primary:disabled {
  opacity: 0.7;
}
.btn-outline {
  background: transparent;
  border: 1px solid #ddd;
  color: #333;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}
</style>
