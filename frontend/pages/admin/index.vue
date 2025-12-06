<template>
  <div class="dashboard-page">
    <div class="dashboard-header">
      <h1 class="page-title">Dashboard</h1>
      <p class="page-subtitle">Welcome back! Here's what's happening with your store.</p>
    </div>

    <div v-if="pending" class="loading-state">
      <div class="spinner"></div>
      <p>Loading stats...</p>
    </div>

    <div v-else class="dashboard-content">
      <!-- Stats Cards -->
      <div class="stats-grid">
        <!-- Total Revenue -->
        <div class="stat-card revenue-card">
          <div class="stat-header">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
            </div>
            <span class="stat-change positive">+12%</span>
          </div>
          <div class="stat-value">${{ stats?.total_sales?.toFixed(2) || '0.00' }}</div>
          <div class="stat-label">Total Revenue</div>
        </div>

        <!-- Total Orders -->
        <div class="stat-card orders-card">
          <div class="stat-header">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
            </div>
            <span class="stat-change positive">+5</span>
          </div>
          <div class="stat-value">{{ stats?.total_orders || 0 }}</div>
          <div class="stat-label">Total Orders</div>
        </div>

        <!-- Total Users -->
        <div class="stat-card users-card">
          <div class="stat-header">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <span class="stat-change positive">+2</span>
          </div>
          <div class="stat-value">{{ stats?.total_users || 0 }}</div>
          <div class="stat-label">Total Users</div>
        </div>

        <!-- Total Products -->
        <div class="stat-card products-card">
          <div class="stat-header">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
            </div>
            <span class="stat-label-small">4 categories</span>
          </div>
          <div class="stat-value">{{ stats?.total_products || 0 }}</div>
          <div class="stat-label">Total Products</div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <h2 class="section-title">Quick Actions</h2>
        <div class="actions-grid">
          <NuxtLink to="/admin/products/new" class="action-card">
            <div class="action-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </div>
            <div class="action-text">
              <div class="action-title">Add Product</div>
              <div class="action-subtitle">Create new product</div>
            </div>
          </NuxtLink>

          <NuxtLink to="/admin/orders" class="action-card">
            <div class="action-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 11 12 14 22 4"></polyline>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
              </svg>
            </div>
            <div class="action-text">
              <div class="action-title">Manage Orders</div>
              <div class="action-subtitle">View all orders</div>
            </div>
          </NuxtLink>

          <NuxtLink to="/admin/users" class="action-card">
            <div class="action-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="action-text">
              <div class="action-title">View Users</div>
              <div class="action-subtitle">Manage customers</div>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const { token } = useAuth()
const { data: stats, pending } = await useFetch('http://localhost:8000/admin/stats', {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})
</script>

<style scoped>
.dashboard-page {
  padding: 32px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 1rem;
  color: #6B7280;
  margin: 0;
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
  color: #6B7280;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.08);
}

.revenue-card {
  background: linear-gradient(135deg, #111 0%, #374151 100%);
  color: white;
}

.revenue-card .stat-icon {
  background: rgba(255,255,255,0.2);
}

.revenue-card .stat-change {
  background: rgba(255,255,255,0.2);
  color: white;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #111;
}

.stat-change {
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
}

.stat-change.positive {
  background: #D1FAE5;
  color: #065F46;
}

.stat-label-small {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 8px;
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
}

.revenue-card .stat-label {
  color: rgba(255,255,255,0.8);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 24px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  border: 2px solid #E5E7EB;
  transition: all 0.2s;
}

.action-card:hover {
  border-color: #111;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.08);
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-text {
  flex: 1;
}

.action-title {
  font-size: 1rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 4px;
}

.action-subtitle {
  font-size: 0.875rem;
  color: #6B7280;
}

@media (max-width: 768px) {
  .dashboard-page {
    padding: 20px;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-value {
    font-size: 2rem;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
