export const useAuth = () => {
    const token = useCookie('auth_token')
    const user = useState('user', () => null)

    const login = async (phone: string, password: string) => {
        try {
            const formData = new FormData()
            formData.append('username', phone)
            formData.append('password', password)

            const data: any = await $fetch('http://localhost:8000/token', {
                method: 'POST',
                body: formData
            })
            token.value = data.access_token
            await fetchUser()
            navigateTo('/')
        } catch (e) {
            console.error(e)
            alert('Login failed')
        }
    }

    const register = async (phone: string, password: string, first_name: string, last_name: string) => {
        try {
            const data: any = await $fetch('http://localhost:8000/register', {
                method: 'POST',
                body: { phone, password, first_name, last_name }
            })
            token.value = data.access_token
            await fetchUser()
            navigateTo('/')
        } catch (e) {
            console.error(e)
            alert('Registration failed')
        }
    }

    const fetchUser = async () => {
        if (!token.value) return
        try {
            user.value = await $fetch('http://localhost:8000/users/me', {
                headers: { Authorization: `Bearer ${token.value}` }
            })
        } catch (e) {
            token.value = null
            user.value = null
        }
    }

    const logout = () => {
        token.value = null
        user.value = null
        navigateTo('/login')
    }

    return { token, user, login, register, logout, fetchUser }
}
