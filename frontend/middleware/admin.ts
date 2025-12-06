export default defineNuxtRouteMiddleware(async (to, from) => {
    const { token, user, fetchUser } = useAuth()

    // If no token, redirect to admin login
    if (!token.value) {
        return navigateTo('/admin/login')
    }

    // If user not loaded yet, try to fetch
    if (!user.value) {
        try {
            await fetchUser()
        } catch (e) {
            // Token invalid, clear and redirect
            token.value = null
            return navigateTo('/admin/login')
        }
    }

    // Check if user is admin
    if (!user.value || user.value.role !== 'admin') {
        return navigateTo('/admin/login')
    }
})
