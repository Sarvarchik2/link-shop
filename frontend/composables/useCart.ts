export const useCart = () => {
    const items = useState<any[]>('cart_items', () => [])

    const addItem = (product: any) => {
        const existing = items.value.find(i => i.id === product.id)
        if (existing) {
            existing.quantity++
        } else {
            items.value.push({ ...product, quantity: 1 })
        }
    }

    const removeItem = (productId: number) => {
        items.value = items.value.filter(i => i.id !== productId)
    }

    const updateQuantity = (productId: number, delta: number) => {
        const item = items.value.find(i => i.id === productId)
        if (item) {
            item.quantity += delta
            if (item.quantity <= 0) {
                removeItem(productId)
            }
        }
    }

    const totalItems = computed(() => items.value.reduce((acc, item) => acc + item.quantity, 0))
    const totalPrice = computed(() => items.value.reduce((acc, item) => acc + (item.price * item.quantity), 0))

    const clearCart = () => {
        items.value = []
    }

    return {
        items,
        addItem,
        removeItem,
        updateQuantity,
        totalItems,
        totalPrice,
        clearCart
    }
}
