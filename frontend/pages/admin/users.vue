<template>
  <div class="users-page">
    <h1 class="page-title">Users</h1>
    
    <div class="card">
      <table class="w-full">
        <thead>
          <tr class="text-left border-b">
            <th class="pb-4 font-semibold text-gray-500">ID</th>
            <th class="pb-4 font-semibold text-gray-500">Phone</th>
            <th class="pb-4 font-semibold text-gray-500">Role</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" class="border-b last:border-0">
            <td class="py-4">{{ user.id }}</td>
            <td class="py-4 font-medium">{{ user.phone }}</td>
            <td class="py-4">
              <span class="role-badge" :class="user.role">{{ user.role }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'admin'
})

const { token } = useAuth()
const { data: users } = await useFetch('http://localhost:8000/admin/users', {
  headers: { Authorization: `Bearer ${token.value}` },
  server: false
})
</script>

<style scoped>
.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 32px;
}
.card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.role-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}
.role-badge.admin {
  background: #E3F2FD;
  color: #1976D2;
}
.role-badge.user {
  background: #F5F5F5;
  color: #666;
}
</style>
