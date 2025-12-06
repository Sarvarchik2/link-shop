export default defineNuxtRouteMiddleware((to, from) => {
    const { user, token } = useAuth()

    // If no token, redirect to login
    if (!token.value) {
        return navigateTo('/admin/login')
    }

    // If user is loaded and not admin, redirect
    if (user.value && user.value.role !== 'admin') {
        return navigateTo('/')
    }
})
