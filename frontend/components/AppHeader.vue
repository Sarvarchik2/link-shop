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

        <!-- Navigation (Desktop only) -->
        <nav class="nav-links">
          <NuxtLink to="/" class="nav-link">Home</NuxtLink>
          <NuxtLink to="/products" class="nav-link">Products</NuxtLink>
          <NuxtLink to="/orders" class="nav-link">Orders</NuxtLink>
        </nav>

        <!-- Actions -->
        <div class="header-actions">
          <!-- Desktop only icons -->
          <NuxtLink to="/favorites" class="icon-btn desktop-only">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
          </NuxtLink>
          
          <NuxtLink to="/cart" class="icon-btn desktop-only cart-btn">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="9" cy="21" r="1"></circle>
              <circle cx="20" cy="21" r="1"></circle>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
            <span v-if="totalItems > 0" class="cart-badge">{{ totalItems }}</span>
          </NuxtLink>
          
          <!-- Profile - visible on all screens -->
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
    
    <NuxtLink to="/cart" class="mobile-nav-item cart-nav-item">
      <div class="cart-icon-wrapper">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        <span v-if="totalItems > 0" class="cart-badge-mobile">{{ totalItems }}</span>
      </div>
      <span>Cart</span>
    </NuxtLink>
    
    <NuxtLink to="/orders" class="mobile-nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
      </svg>
      <span>Orders</span>
    </NuxtLink>
    
    <NuxtLink to="/favorites" class="mobile-nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
      </svg>
      <span>Favorites</span>
    </NuxtLink>
  </nav>
</template>

<script setup>
const { totalItems } = useCart()
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
  gap: 12px;
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

/* Hide on mobile */
.desktop-only {
  display: none;
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
  padding-bottom: calc(8px + env(safe-area-inset-bottom));
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
  font-size: 0.65rem;
  font-weight: 600;
  transition: all 0.2s;
}

.mobile-nav-item.router-link-active {
  color: #111;
}

.mobile-nav-item svg {
  stroke-width: 2;
}

.cart-icon-wrapper {
  position: relative;
}

.cart-badge-mobile {
  position: absolute;
  top: -6px;
  right: -8px;
  background: #EF4444;
  color: white;
  font-size: 0.6rem;
  font-weight: 700;
  min-width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

/* Desktop Breakpoint */
@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }
  
  .mobile-nav {
    display: none;
  }
  
  .desktop-only {
    display: flex;
  }
  
  .nav-link::after {
    bottom: -28px;
  }
}

/* Mobile styles */
@media (max-width: 767px) {
  .desktop-header .nav-links {
    display: none;
  }
  
  .header-content {
    height: 60px;
  }
  
  .logo span {
    font-size: 1.1rem;
  }
  
  .logo svg {
    width: 28px;
    height: 28px;
  }
  
  .icon-btn {
    width: 40px;
    height: 40px;
    border-radius: 10px;
  }
  
  .header-actions {
    gap: 8px;
  }
}
</style>
