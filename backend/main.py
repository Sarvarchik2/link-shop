from typing import Optional, List
import os
import uuid
import base64
from fastapi import FastAPI, HTTPException, Query, Depends, status, UploadFile, File
from fastapi.staticfiles import StaticFiles
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# --- Configuration ---
SECRET_KEY = "your-secret-key-here" # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Models ---

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str = Field(index=True, unique=True)
    password_hash: str
    first_name: str = ""
    last_name: str = ""
    role: str = "user" # user, admin

class UserCreate(SQLModel):
    phone: str
    password: str
    first_name: str
    last_name: str

class UserRead(SQLModel):
    id: int
    phone: str
    first_name: str
    last_name: str
    role: str

class Token(SQLModel):
    access_token: str
    token_type: str

class Brand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    logo_url: str

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    image_url: Optional[str] = None

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    image_url: str
    images: Optional[str] = None  # JSON string of image URLs
    category: str
    brand: str
    rating: float = 0.0
    reviews_count: int = 0
    is_favorite: bool = False
    stock: int = 0  # Quantity in stock
    sizes: Optional[str] = None  # JSON string of available sizes
    colors: Optional[str] = None  # JSON string of available colors with stock

class ProductCreate(SQLModel):
    name: str
    description: str
    price: float
    image_url: str
    images: Optional[str] = None
    category: str
    brand: str
    stock: int = 0
    sizes: Optional[str] = None
    colors: Optional[str] = None

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    price: float
    selected_color: Optional[str] = None  # Color name
    selected_size: Optional[str] = None   # Size

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    status: str = "pending"
    total_price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Delivery info
    delivery_address: Optional[str] = None
    delivery_city: Optional[str] = None
    delivery_phone: Optional[str] = None
    recipient_name: Optional[str] = None
    # Payment
    payment_method: str = "cash"  # cash, card
    notes: Optional[str] = None

class OrderRead(SQLModel):
    id: int
    user_id: int
    status: str
    total_price: float
    created_at: datetime
    delivery_address: Optional[str] = None
    delivery_city: Optional[str] = None
    delivery_phone: Optional[str] = None
    recipient_name: Optional[str] = None
    payment_method: str = "cash"
    notes: Optional[str] = None

class OrderItemCreate(SQLModel):
    product_id: int
    quantity: int
    selected_color: Optional[str] = None
    selected_size: Optional[str] = None

class OrderCreate(SQLModel):
    items: List[OrderItemCreate]
    delivery_address: str
    delivery_city: str
    delivery_phone: str
    recipient_name: str
    payment_method: str = "cash"
    notes: Optional[str] = None

class OrderItemDetail(SQLModel):
    product_id: int
    quantity: int
    price: float
    product_name: str
    product_image: str
    selected_color: Optional[str] = None
    selected_size: Optional[str] = None

class OrderReadWithItems(OrderRead):
    items: List[OrderItemDetail]

class UserInfo(SQLModel):
    id: int
    phone: str
    first_name: str
    last_name: str

class OrderReadWithUser(OrderRead):
    user: Optional[UserInfo] = None
    items: Optional[List[OrderItemDetail]] = None

class OrdersByStatus(SQLModel):
    pending: int = 0
    processing: int = 0
    shipping: int = 0
    delivered: int = 0
    cancelled: int = 0

class DashboardStats(SQLModel):
    total_sales: float  # Only from non-cancelled orders
    total_orders: int
    total_users: int
    total_products: int
    orders_by_status: OrdersByStatus
    today_sales: float = 0.0
    today_orders: int = 0
    week_sales: float = 0.0
    week_orders: int = 0
    month_sales: float = 0.0
    month_orders: int = 0

class OrderStatusUpdate(SQLModel):
    status: str

# --- Database ---
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# --- Auth Helper Functions ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    with Session(engine) as session:
        statement = select(User).where(User.phone == phone)
        user = session.exec(statement).first()
        if user is None:
            raise credentials_exception
        return user

async def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

# --- App ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Image upload endpoint
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Generate unique filename
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Return URL
    return {"url": f"http://localhost:8000/uploads/{filename}"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        # Seed Brands
        if not session.exec(select(Brand)).first():
            brands = [
                Brand(name="Ray-Ban", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Ray-Ban_logo.svg/2560px-Ray-Ban_logo.svg.png"),
                Brand(name="Oakley", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Oakley_logo.svg/2560px-Oakley_logo.svg.png"),
                Brand(name="Prada", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Prada-Logo.svg/2560px-Prada-Logo.svg.png"),
                Brand(name="Gucci", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Gucci_Logo.svg/2560px-Gucci_Logo.svg.png"),
            ]
            for b in brands: session.add(b)
            session.commit()

        # Seed Categories
        if not session.exec(select(Category)).first():
            categories = [
                Category(name="Sunglasses", image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"),
                Category(name="Smart Glasses", image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop"),
                Category(name="Eyeglasses", image_url="https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop"),
                Category(name="Luxury", image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"),
            ]
            for c in categories: session.add(c)
            session.commit()

        # Seed Products
        if not session.exec(select(Product)).first():
            import json
            seed_products = [
                Product(
                    name="Ray-Ban Meta Wayfarer", 
                    description="Classic Wayfarer style with smart features. Built-in camera and speakers for the ultimate smart glasses experience.", 
                    price=299.00, 
                    image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop"
                    ]),
                    category="Smart Glasses", 
                    brand="Ray-Ban", 
                    rating=4.5, 
                    reviews_count=120,
                    stock=15,
                    sizes=json.dumps(["S", "M", "L"]),
                    colors=json.dumps([
                        {"name": "Black", "hex": "#000000", "stock": 8},
                        {"name": "Tortoise", "hex": "#8B4513", "stock": 5},
                        {"name": "Blue", "hex": "#1E40AF", "stock": 2}
                    ])
                ),
                Product(
                    name="Ray-Ban Meta Headliner", 
                    description="Round shape for a retro look. Perfect for everyday wear with advanced audio technology.", 
                    price=329.00, 
                    image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop",
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop"
                    ]),
                    category="Smart Glasses", 
                    brand="Ray-Ban", 
                    rating=4.7, 
                    reviews_count=85,
                    stock=8,
                    sizes=json.dumps(["M", "L"]),
                    colors=json.dumps([
                        {"name": "Matte Black", "hex": "#1a1a1a", "stock": 5},
                        {"name": "Shiny Black", "hex": "#000000", "stock": 3}
                    ])
                ),
                Product(
                    name="Oakley Holbrook", 
                    description="Timeless, classic design fused with modern Oakley technology. Durable and stylish.", 
                    price=150.00, 
                    image_url="https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop",
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop"
                    ]),
                    category="Sunglasses", 
                    brand="Oakley", 
                    rating=4.8, 
                    reviews_count=210,
                    stock=25,
                    sizes=json.dumps(["S", "M", "L", "XL"]),
                    colors=json.dumps([
                        {"name": "Matte Black", "hex": "#1a1a1a", "stock": 10},
                        {"name": "Polished Black", "hex": "#000000", "stock": 8},
                        {"name": "Brown Tortoise", "hex": "#654321", "stock": 7}
                    ])
                ),
                Product(
                    name="Prada Symbole", 
                    description="Geometric design with a bold look. Luxury eyewear at its finest.", 
                    price=450.00, 
                    image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"
                    ]),
                    category="Luxury", 
                    brand="Prada", 
                    rating=4.9, 
                    reviews_count=45,
                    stock=0,
                    sizes=json.dumps(["M", "L"]),
                    colors=json.dumps([
                        {"name": "Black", "hex": "#000000", "stock": 0},
                        {"name": "Gold", "hex": "#FFD700", "stock": 0}
                    ])
                ),
                Product(
                    name="Gucci GG0061S", 
                    description="Round metal sunglasses with a vintage feel. Iconic Gucci style.", 
                    price=380.00, 
                    image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop",
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=2080&auto=format&fit=crop"
                    ]),
                    category="Luxury", 
                    brand="Gucci", 
                    rating=4.6, 
                    reviews_count=60,
                    stock=12,
                    sizes=json.dumps(["S", "M"]),
                    colors=json.dumps([
                        {"name": "Gold", "hex": "#FFD700", "stock": 6},
                        {"name": "Silver", "hex": "#C0C0C0", "stock": 6}
                    ])
                ),
                Product(
                    name="Ray-Ban Aviator", 
                    description="The timeless style that started it all. Classic aviator design.", 
                    price=163.00, 
                    image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1572635196237-14b3f281503f?q=80&w=2080&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1577803645773-f96470509666?q=80&w=2080&auto=format&fit=crop"
                    ]),
                    category="Sunglasses", 
                    brand="Ray-Ban", 
                    rating=4.6, 
                    reviews_count=200,
                    stock=30,
                    sizes=json.dumps(["S", "M", "L"]),
                    colors=json.dumps([
                        {"name": "Gold/Green", "hex": "#FFD700", "stock": 15},
                        {"name": "Silver/Blue", "hex": "#C0C0C0", "stock": 10},
                        {"name": "Black", "hex": "#000000", "stock": 5}
                    ])
                ),
            ]
            for p in seed_products: session.add(p)
            session.commit()
        
        # Seed Admin
        admin = session.exec(select(User).where(User.phone == "admin")).first()
        if not admin:
            admin_user = User(phone="admin", password_hash=get_password_hash("admin123"), role="admin")
            session.add(admin_user)
            session.commit()

# --- Endpoints ---

@app.post("/register", response_model=Token)
def register(user: UserCreate):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.phone == user.phone)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        hashed_password = get_password_hash(user.password)
        db_user = User(
            phone=user.phone, 
            password_hash=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        access_token = create_access_token(data={"sub": db_user.phone})
        return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.phone == form_data.username)).first()
        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect phone or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.phone})
        return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/products", response_model=List[Product])
def get_products(category: Optional[str] = None, brand: Optional[str] = None):
    with Session(engine) as session:
        statement = select(Product)
        if category:
            statement = statement.where(Product.category == category)
        if brand:
            statement = statement.where(Product.brand == brand)
        results = session.exec(statement).all()
        return results

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

@app.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    with Session(engine) as session:
        db_product = Product.from_orm(product)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, current_user: User = Depends(get_current_admin)):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
        return {"ok": True}

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductCreate, current_user: User = Depends(get_current_admin)):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product.name = product_update.name
        product.description = product_update.description
        product.price = product_update.price
        product.image_url = product_update.image_url
        product.category = product_update.category
        product.brand = product_update.brand
        product.stock = product_update.stock
        product.sizes = product_update.sizes
        product.colors = product_update.colors
        product.images = product_update.images
        
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


@app.post("/products/{product_id}/favorite", response_model=Product)
def toggle_favorite(product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.is_favorite = not product.is_favorite
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

# --- Brand & Category Endpoints ---

@app.get("/brands", response_model=List[Brand])
def get_brands():
    with Session(engine) as session:
        return session.exec(select(Brand)).all()

@app.post("/brands", response_model=Brand)
def create_brand(brand: Brand):
    with Session(engine) as session:
        session.add(brand)
        session.commit()
        session.refresh(brand)
        return brand

@app.delete("/brands/{brand_id}")
def delete_brand(brand_id: int, current_user: User = Depends(get_current_admin)):
    with Session(engine) as session:
        brand = session.get(Brand, brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        session.delete(brand)
        session.commit()
        return {"ok": True}

@app.get("/categories", response_model=List[Category])
def get_categories():
    with Session(engine) as session:
        return session.exec(select(Category)).all()

@app.post("/categories", response_model=Category)
def create_category(category: Category):
    with Session(engine) as session:
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, current_user: User = Depends(get_current_admin)):
    with Session(engine) as session:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        session.delete(category)
        session.commit()
        return {"ok": True}

# --- Order Endpoints ---

@app.post("/orders", response_model=OrderRead)
def create_order(order_create: OrderCreate, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        total_price = 0.0
        order_items = []
        
        for item in order_create.items:
            product = session.get(Product, item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
            item_total = product.price * item.quantity
            total_price += item_total
            
            order_items.append(OrderItem(
                product_id=item.product_id, 
                quantity=item.quantity, 
                price=product.price,
                selected_color=item.selected_color,
                selected_size=item.selected_size
            ))

        db_order = Order(
            user_id=current_user.id, 
            total_price=total_price, 
            status="pending",
            delivery_address=order_create.delivery_address,
            delivery_city=order_create.delivery_city,
            delivery_phone=order_create.delivery_phone,
            recipient_name=order_create.recipient_name,
            payment_method=order_create.payment_method,
            notes=order_create.notes
        )
        session.add(db_order)
        session.commit()
        session.refresh(db_order)

        for order_item in order_items:
            order_item.order_id = db_order.id
            session.add(order_item)
        
        session.commit()
        session.refresh(db_order)
        
        return OrderRead(
            id=db_order.id,
            user_id=db_order.user_id,
            status=db_order.status,
            total_price=db_order.total_price,
            created_at=db_order.created_at,
            delivery_address=db_order.delivery_address,
            delivery_city=db_order.delivery_city,
            delivery_phone=db_order.delivery_phone,
            recipient_name=db_order.recipient_name,
            payment_method=db_order.payment_method,
            notes=db_order.notes
        )

@app.get("/orders/me", response_model=List[OrderReadWithItems])
def get_my_orders(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        orders = session.exec(select(Order).where(Order.user_id == current_user.id).order_by(Order.created_at.desc())).all()
        result = []
        for order in orders:
            # Fetch items for this order
            items = session.exec(select(OrderItem).where(OrderItem.order_id == order.id)).all()
            item_details = []
            for item in items:
                product = session.get(Product, item.product_id)
                item_details.append(OrderItemDetail(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                    product_name=product.name if product else "Unknown Product",
                    product_image=product.image_url if product else "",
                    selected_color=item.selected_color,
                    selected_size=item.selected_size
                ))
            
            result.append(OrderReadWithItems(
                id=order.id,
                user_id=order.user_id,
                status=order.status,
                total_price=order.total_price,
                created_at=order.created_at,
                items=item_details
            ))
        return result

# --- Admin Endpoints ---

@app.get("/admin/stats", response_model=DashboardStats)
def get_admin_stats(current_user: User = Depends(get_current_admin)):
    with Session(engine) as session:
        total_users = len(session.exec(select(User)).all())
        total_products = len(session.exec(select(Product)).all())
        orders = session.exec(select(Order)).all()
        total_orders = len(orders)
        
        # Calculate revenue excluding cancelled orders
        total_sales = sum(order.total_price for order in orders if order.status != 'cancelled')
        
        # Orders by status
        orders_by_status = OrdersByStatus(
            pending=sum(1 for o in orders if o.status == 'pending'),
            processing=sum(1 for o in orders if o.status == 'processing'),
            shipping=sum(1 for o in orders if o.status == 'shipping'),
            delivered=sum(1 for o in orders if o.status == 'delivered'),
            cancelled=sum(1 for o in orders if o.status == 'cancelled')
        )
        
        # Time-based stats
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        today_orders_list = [o for o in orders if o.created_at >= today_start and o.status != 'cancelled']
        week_orders_list = [o for o in orders if o.created_at >= week_start and o.status != 'cancelled']
        month_orders_list = [o for o in orders if o.created_at >= month_start and o.status != 'cancelled']
        
        today_sales = sum(o.total_price for o in today_orders_list)
        today_orders_count = len(today_orders_list)
        
        week_sales = sum(o.total_price for o in week_orders_list)
        week_orders_count = len(week_orders_list)
        
        month_sales = sum(o.total_price for o in month_orders_list)
        month_orders_count = len(month_orders_list)
        
        return DashboardStats(
            total_sales=total_sales, 
            total_orders=total_orders, 
            total_users=total_users, 
            total_products=total_products,
            orders_by_status=orders_by_status,
            today_sales=today_sales,
            today_orders=today_orders_count,
            week_sales=week_sales,
            week_orders=week_orders_count,
            month_sales=month_sales,
            month_orders=month_orders_count
        )

@app.get("/admin/users", response_model=List[UserRead])
def get_all_users(current_user: User = Depends(get_current_admin)):
    with Session(engine) as session:
        return session.exec(select(User)).all()

@app.get("/admin/orders", response_model=List[OrderReadWithUser])
def get_all_orders(current_user: User = Depends(get_current_admin)):
    with Session(engine) as session:
        orders = session.exec(select(Order).order_by(Order.created_at.desc())).all()
        result = []
        for order in orders:
            user = session.get(User, order.user_id)
            # Get order items
            items = session.exec(select(OrderItem).where(OrderItem.order_id == order.id)).all()
            item_details = []
            for item in items:
                product = session.get(Product, item.product_id)
                item_details.append(OrderItemDetail(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                    product_name=product.name if product else "Unknown",
                    product_image=product.image_url if product else "",
                    selected_color=item.selected_color,
                    selected_size=item.selected_size
                ))
            
            result.append(OrderReadWithUser(
                id=order.id,
                user_id=order.user_id,
                status=order.status,
                total_price=order.total_price,
                created_at=order.created_at,
                delivery_address=order.delivery_address,
                delivery_city=order.delivery_city,
                delivery_phone=order.delivery_phone,
                recipient_name=order.recipient_name,
                payment_method=order.payment_method,
                notes=order.notes,
                user=UserInfo(
                    id=user.id,
                    phone=user.phone,
                    first_name=user.first_name,
                    last_name=user.last_name
                ) if user else None,
                items=item_details
            ))
        return result

@app.put("/admin/orders/{order_id}", response_model=OrderRead)
def update_order_status(order_id: int, status_update: OrderStatusUpdate, current_user: User = Depends(get_current_admin)):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.status = status_update.status
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
