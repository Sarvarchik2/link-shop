<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <h1 class="register-title">Create Account</h1>
          <p class="register-subtitle">Join us today</p>
        </div>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">First Name</label>
              <input 
                v-model="firstName" 
                type="text" 
                required 
                class="form-input" 
                placeholder="John" 
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Last Name</label>
              <input 
                v-model="lastName" 
                type="text" 
                required 
                class="form-input" 
                placeholder="Doe" 
              />
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label">Phone Number</label>
            <input 
              v-model="phone" 
              type="tel" 
              required 
              class="form-input" 
              placeholder="+998901234567" 
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Password</label>
            <input 
              v-model="password" 
              type="password" 
              required 
              class="form-input" 
              placeholder="••••••••" 
            />
          </div>
          
          <button type="submit" class="btn-submit">Sign Up</button>
          
          <div class="form-footer">
            <span class="footer-text">Already have an account?</span>
            <NuxtLink to="/login" class="footer-link">Sign in</NuxtLink>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: false
})

const firstName = ref('')
const lastName = ref('')
const phone = ref('')
const password = ref('')
const { register } = useAuth()

const handleRegister = async () => {
  try {
  await register(phone.value, password.value, firstName.value, lastName.value)
  } catch (e) {
    useToast().error('Registration failed. Phone number might already be registered.')
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: #FAFAFA;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 540px;
}

.register-card {
  background: white;
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.register-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.register-subtitle {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  letter-spacing: 0.025em;
}

.form-input {
  padding: 16px 20px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s;
  background: #F9FAFB;
  color: #111;
}

.form-input::placeholder {
  color: #9CA3AF;
}

.form-input:focus {
  outline: none;
  border-color: #111;
  background: white;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.05);
}

.btn-submit {
  padding: 18px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 8px;
}

.btn-submit:hover {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.btn-submit:active {
  transform: translateY(0);
}

.form-footer {
  text-align: center;
  margin-top: 8px;
}

.footer-text {
  color: #6B7280;
  font-size: 0.875rem;
}

.footer-link {
  color: #111;
  font-weight: 600;
  margin-left: 4px;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-link:hover {
  text-decoration: underline;
}

@media (max-width: 640px) {
  .register-card {
    padding: 32px 24px;
  }
  
  .register-title {
    font-size: 2rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
