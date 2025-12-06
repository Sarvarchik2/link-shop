<template>
  <!-- Desktop Header -->
  <header class="header desktop-header">
    <div class="container">
      <div class="header-content">
        <!-- Logo -->
        <NuxtLink to="/" class="logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <span>EYEWEAR</span>
        </NuxtLink>

        <!-- Navigation -->
        <nav class="nav-links">
          <NuxtLink to="/" class="nav-link">Home</NuxtLink>
          <NuxtLink to="/products" class="nav-link">Products</NuxtLink>
          <NuxtLink to="/orders" class="nav-link">Orders</NuxtLink>
          <NuxtLink to="/favorites" class="nav-link">Favorites</NuxtLink>
        </nav>

        <!-- Actions -->
        <div class="header-actions">
          <button class="icon-btn">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </button>
          
          <NuxtLink to="/favorites" class="icon-btn">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
          </NuxtLink>
          
          <NuxtLink to="/cart" class="icon-btn cart-btn">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="9" cy="21" r="1"></circle>
              <circle cx="20" cy="21" r="1"></circle>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
            <span v-if="cart.totalItems > 0" class="cart-badge">{{ cart.totalItems }}</span>
          </NuxtLink>
          
          <NuxtLink to="/profile" class="icon-btn profile-btn">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </NuxtLink>
        </div>
      </div>
    </div>
  </header>

  <!-- Mobile Bottom Navigation -->
  <nav class="mobile-nav">
    <NuxtLink to="/" class="mobile-nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
      <span>Home</span>
    </NuxtLink>
    
    <NuxtLink to="/products" class="mobile-nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
        <line x1="1" y1="10" x2="23" y2="10"></line>
      </svg>
      <span>Products</span>
    </NuxtLink>
    
    <NuxtLink to="/orders" class="mobile-nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="9" cy="21" r="1"></circle>
        <circle cx="20" cy="21" r="1"></circle>
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
      </svg>
      <span>Orders</span>
    </NuxtLink>
    
    <NuxtLink to="/favorites" class="mobile-nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
      </svg>
      <span>Favorites</span>
    </NuxtLink>
    
    <NuxtLink to="/profile" class="mobile-nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
      </svg>
      <span>Profile</span>
    </NuxtLink>
  </nav>
</template>

<script setup>
const cart = useCart()
</script>

<style scoped>
/* Desktop Header */
.desktop-header {
  background: white;
  border-bottom: 1px solid #f0f0f0;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 80px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 900;
  font-size: 1.25rem;
  color: #111;
  letter-spacing: 1px;
}

.nav-links {
  display: none;
  gap: 40px;
}

.nav-link {
  font-weight: 600;
  font-size: 0.95rem;
  color: #666;
  transition: color 0.2s;
  position: relative;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #111;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 2px;
  background: #111;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.icon-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  color: #111;
}

.icon-btn:hover {
  background: #111;
  color: white;
  transform: translateY(-2px);
}

.cart-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #EF4444;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

/* Mobile Navigation */
.mobile-nav {
  display: flex;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #f0f0f0;
  padding: 8px 0;
  z-index: 100;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
}

.mobile-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px;
  color: #999;
  font-size: 0.7rem;
  font-weight: 600;
  transition: all 0.2s;
}

.mobile-nav-item.router-link-active {
  color: #111;
}

.mobile-nav-item svg {
  stroke-width: 2.5;
}

/* Desktop Breakpoint */
@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }
  
  .mobile-nav {
    display: none;
  }
  
  .nav-link::after {
    bottom: -28px;
  }
}

/* Hide on mobile */
@media (max-width: 767px) {
  .desktop-header .nav-links {
    display: none;
  }
  
  .header-content {
    height: 64px;
  }
  
  .logo span {
    font-size: 1.1rem;
  }
  
  .icon-btn {
    width: 40px;
    height: 40px;
  }
}
</style>
