export const useAuth = () => {
    const token = useCookie('auth_token')
    const user = useState('user', () => null)

    const login = async (phone: string, password: string, redirect: boolean = true) => {
        const formData = new FormData()
        formData.append('username', phone)
        formData.append('password', password)

        const data: any = await $fetch('http://localhost:8000/token', {
            method: 'POST',
            body: formData
        })
        token.value = data.access_token
        await fetchUser()
        useToast().success('Welcome back!')
        if (redirect) {
            navigateTo('/')
        }
    }

    const register = async (phone: string, password: string, first_name: string, last_name: string) => {
        const data: any = await $fetch('http://localhost:8000/register', {
            method: 'POST',
            body: { phone, password, first_name, last_name }
        })
        token.value = data.access_token
        await fetchUser()
        useToast().success('Welcome! Account created successfully')
        navigateTo('/')
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
