<template>
  <div class="auth-page container flex justify-center items-center h-screen">
    <div class="card p-8 w-full max-w-md">
      <h1 class="text-2xl font-bold mb-6 text-center">Admin Login</h1>
      <form @submit.prevent="handleLogin" class="grid gap-4">
        <div>
          <label class="block text-sm font-medium mb-1">Username</label>
          <input v-model="username" type="text" required class="input w-full" placeholder="admin" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Password</label>
          <input v-model="password" type="password" required class="input w-full" placeholder="••••••••" />
        </div>
        <button type="submit" class="btn btn-primary w-full">Login to Dashboard</button>
      </form>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: false
})

const username = ref('')
const password = ref('')
const { login, user, token } = useAuth()

const handleLogin = async () => {
  try {
    await login(username.value, password.value, false)
    
    if (user.value && user.value.role === 'admin') {
      navigateTo('/admin')
    } else {
      useToast().error('Access denied. Admin privileges required.')
      token.value = null
      user.value = null
    }
  } catch (e) {
    console.error(e)
    useToast().error('Invalid username or password')
  }
}
</script>

<style scoped>
.h-screen { min-height: 100vh; display: flex; align-items: center; }
.auth-page { background: #FAFAFA; }
.card {
  background: white;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}
.input {
  padding: 12px;
  border: 1px solid #eee;
  border-radius: 12px;
  background: #f9f9f9;
  transition: all 0.2s;
  font-size: 1rem;
}
.input:focus {
  outline: none;
  border-color: #111;
  background: white;
}
.btn {
  padding: 14px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-size: 1rem;
}
.btn-primary {
  background: #111;
  color: white;
}
.btn-primary:hover {
  background: #000;
  transform: translateY(-1px);
}
</style>
