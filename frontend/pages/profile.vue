<template>
  <div class="profile-page">
    <AppHeader />
    
    <main class="container py-8">
      <div class="profile-content">
        <div class="profile-header">
          <div class="user-info">
            <h1 class="user-name">{{ user?.first_name }} {{ user?.last_name }}</h1>
            <p class="user-phone">{{ user?.phone }}</p>
          </div>
        </div>

        <div class="menu-section">
          <NuxtLink to="/orders" class="menu-item">
            <div class="menu-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
            </div>
            <div class="menu-text">
              <div class="menu-title">My Orders</div>
              <div class="menu-subtitle">View your order history</div>
            </div>
            <svg class="menu-arrow" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </NuxtLink>

          <NuxtLink to="/favorites" class="menu-item">
            <div class="menu-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
            </div>
            <div class="menu-text">
              <div class="menu-title">Favorites</div>
              <div class="menu-subtitle">Your wishlist items</div>
            </div>
            <svg class="menu-arrow" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </NuxtLink>

          <button @click="handleLogout" class="menu-item logout-btn">
            <div class="menu-icon logout-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
            </div>
            <div class="menu-text">
              <div class="menu-title logout-text">Log Out</div>
            </div>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

const { user, logout } = useAuth()

const handleLogout = () => {
  logout()
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24px;
  padding: 40px 32px;
  margin-bottom: 24px;
  color: white;
}

.user-info {
  text-align: center;
}

.user-name {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 8px;
}

.user-phone {
  font-size: 1rem;
  opacity: 0.9;
}

.menu-section {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  color: #111;
  background: white;
  border: none;
  width: 100%;
  text-align: left;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:hover {
  background: #F9FAFB;
}

.menu-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: #111;
}

.logout-icon {
  background: #FEF2F2;
  color: #EF4444;
}

.menu-text {
  flex: 1;
}

.menu-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 2px;
}

.menu-subtitle {
  font-size: 0.875rem;
  color: #6B7280;
}

.logout-text {
  color: #EF4444;
}

.menu-arrow {
  color: #9CA3AF;
}

@media (max-width: 640px) {
  .profile-header {
    padding: 32px 24px;
  }
  
  .user-name {
    font-size: 1.5rem;
  }
  
  .menu-item {
    padding: 16px 20px;
  }
  
  .menu-icon {
    width: 44px;
    height: 44px;
  }
}
</style>
