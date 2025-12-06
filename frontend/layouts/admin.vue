<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="logo">Admin Panel</div>
      <nav class="nav">
        <NuxtLink to="/admin" class="nav-item">Dashboard</NuxtLink>
        <NuxtLink to="/admin/products" class="nav-item">Products</NuxtLink>
        <NuxtLink to="/admin/brands" class="nav-item">Brands</NuxtLink>
        <NuxtLink to="/admin/categories" class="nav-item">Categories</NuxtLink>
        <NuxtLink to="/admin/users" class="nav-item">Users</NuxtLink>
        <NuxtLink to="/admin/orders" class="nav-item">Orders</NuxtLink>
        <NuxtLink to="/" class="nav-item back-home">Back to Shop</NuxtLink>
      </nav>
    </aside>
    <main class="content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f4f6f8;
}
.sidebar {
  width: 260px;
  background: white;
  border-right: 1px solid #eee;
  padding: 24px;
  display: flex;
  flex-direction: column;
}
.logo {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 40px;
  color: #111;
}
.nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.nav-item {
  padding: 12px 16px;
  border-radius: 8px;
  color: #666;
  font-weight: 500;
  transition: all 0.2s;
}
.nav-item:hover, .nav-item.router-link-active {
  background: #f4f6f8;
  color: #111;
}
.back-home {
  margin-top: auto;
  color: #888;
}
.content {
  flex: 1;
  padding: 40px;
  overflow-y: auto;
}
</style>
