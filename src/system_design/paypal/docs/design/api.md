# API Specifications

## Overview
RESTful API design with FastAPI, following AWS API Gateway patterns and best practices for scalable payment system.

## API Gateway Architecture

### AWS API Gateway Configuration
```yaml
# API Gateway REST API
PayPalCloneAPI:
  Type: AWS::ApiGateway::RestApi
  Properties:
    Name: paypal-clone-api
    Description: PayPal Clone Payment System API
    EndpointConfiguration:
      Types:
        - REGIONAL
    Policy:
      Statement:
        - Effect: Allow
          Principal: "*"
          Action: execute-api:Invoke
          Resource: "*"
          Condition:
            IpAddress:
              aws:SourceIp: 
                - "10.0.0.0/8"
                - "172.16.0.0/12"
```

### Rate Limiting & Throttling
```yaml
# Usage Plan
APIUsagePlan:
  Type: AWS::ApiGateway::UsagePlan
  Properties:
    UsagePlanName: paypal-clone-usage-plan
    Description: Usage plan for PayPal Clone API
    Throttle:
      BurstLimit: 2000
      RateLimit: 1000
    Quota:
      Limit: 1000000
      Period: DAY
```

## Authentication & Authorization

### JWT Token Structure
```python
# JWT payload structure
jwt_payload = {
    "sub": "user_id",           # Subject (user ID)
    "email": "user@example.com",
    "roles": ["user", "verified"],
    "permissions": ["read", "write", "transfer"],
    "iat": 1640995200,          # Issued at
    "exp": 1640998800,          # Expires at
    "jti": "token_id",          # JWT ID for blacklisting
    "device_id": "device_fingerprint"
}

# FastAPI dependency for authentication
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return await get_user_by_id(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## API Endpoints

### User Management API

#### User Registration
```python
@app.post("/api/v1/users/register", response_model=UserResponse)
async def register_user(user_data: UserRegistration):
    """
    Register a new user account
    
    - **email**: Valid email address
    - **password**: Strong password (min 8 chars)
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **phone**: Phone number for verification
    """
    
    # Validate input
    if await user_exists(user_data.email):
        raise HTTPException(status_code=409, detail="User already exists")
    
    # Create user
    user = await create_user(user_data)
    
    # Send verification email
    await send_verification_email(user.email)
    
    return UserResponse(
        user_id=user.user_id,
        email=user.email,
        status="pending_verification",
        created_at=user.created_at
    )

# Request/Response models
class UserRegistration(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')

class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    status: str
    created_at: datetime
```

#### User Authentication
```python
@app.post("/api/v1/auth/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """
    Authenticate user and return JWT token
    
    - **email**: User's email address
    - **password**: User's password
    - **device_info**: Optional device information
    """
    
    # Validate credentials
    user = await authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check account status
    if user.status != "active":
        raise HTTPException(status_code=403, detail="Account not active")
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(user.user_id), "email": user.email}
    )
    
    # Log login event
    await log_audit_event("user_login", user.user_id, credentials.device_info)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=3600,
        user_id=user.user_id
    )

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    device_info: Optional[dict] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_id: UUID
```

### Payment API

#### Send Payment
```python
@app.post("/api/v1/payments/send", response_model=PaymentResponse)
async def send_payment(
    payment_data: SendPaymentRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Send money to another user
    
    - **receiver_email**: Recipient's email address
    - **amount**: Payment amount (positive decimal)
    - **currency**: Currency code (USD, EUR, etc.)
    - **description**: Optional payment description
    - **payment_method_id**: Payment method to use
    """
    
    # Validate receiver
    receiver = await get_user_by_email(payment_data.receiver_email)
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    # Validate payment method
    payment_method = await get_payment_method(
        payment_data.payment_method_id, 
        current_user.user_id
    )
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment method not found")
    
    # Check balance/limits
    await validate_payment_limits(current_user.user_id, payment_data.amount)
    
    # Fraud check
    fraud_score = await check_fraud_risk(current_user.user_id, payment_data)
    if fraud_score > 80:
        raise HTTPException(status_code=403, detail="Payment blocked - high risk")
    
    # Process payment
    transaction = await process_payment(
        sender_id=current_user.user_id,
        receiver_id=receiver.user_id,
        amount=payment_data.amount,
        currency=payment_data.currency,
        payment_method_id=payment_data.payment_method_id,
        description=payment_data.description
    )
    
    return PaymentResponse(
        transaction_id=transaction.transaction_id,
        status=transaction.status,
        amount=transaction.amount,
        currency=transaction.currency,
        created_at=transaction.created_at
    )

class SendPaymentRequest(BaseModel):
    receiver_email: EmailStr
    amount: Decimal = Field(..., gt=0, max_digits=15, decimal_places=2)
    currency: str = Field(..., regex=r'^[A-Z]{3}$')
    description: Optional[str] = Field(None, max_length=500)
    payment_method_id: UUID

class PaymentResponse(BaseModel):
    transaction_id: UUID
    status: str
    amount: Decimal
    currency: str
    created_at: datetime
```

#### Payment Status
```python
@app.get("/api/v1/payments/{transaction_id}", response_model=TransactionDetail)
async def get_payment_status(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """
    Get payment transaction details
    
    - **transaction_id**: Transaction UUID
    """
    
    transaction = await get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Check authorization
    if (transaction.sender_id != current_user.user_id and 
        transaction.receiver_id != current_user.user_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return TransactionDetail(
        transaction_id=transaction.transaction_id,
        sender_id=transaction.sender_id,
        receiver_id=transaction.receiver_id,
        amount=transaction.amount,
        currency=transaction.currency,
        status=transaction.status,
        description=transaction.description,
        fees=transaction.fees,
        created_at=transaction.created_at,
        completed_at=transaction.completed_at
    )
```

### Wallet API

#### Get Wallet Balance
```python
@app.get("/api/v1/wallets", response_model=List[WalletBalance])
async def get_wallet_balances(
    current_user: User = Depends(get_current_user)
):
    """
    Get all wallet balances for the current user
    """
    
    wallets = await get_user_wallets(current_user.user_id)
    
    wallet_balances = []
    for wallet in wallets:
        balance = await get_wallet_balance(wallet.wallet_id)
        wallet_balances.append(WalletBalance(
            wallet_id=wallet.wallet_id,
            currency=wallet.currency,
            balance=balance.balance,
            available_balance=balance.available_balance,
            frozen_balance=balance.frozen_balance
        ))
    
    return wallet_balances

class WalletBalance(BaseModel):
    wallet_id: UUID
    currency: str
    balance: Decimal
    available_balance: Decimal
    frozen_balance: Decimal
```

#### Add Funds
```python
@app.post("/api/v1/wallets/{wallet_id}/add-funds", response_model=TransactionResponse)
async def add_funds(
    wallet_id: UUID,
    fund_request: AddFundsRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Add funds to wallet from external payment method
    
    - **amount**: Amount to add
    - **payment_method_id**: External payment method
    """
    
    # Validate wallet ownership
    wallet = await get_wallet(wallet_id)
    if wallet.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Process fund addition
    transaction = await add_wallet_funds(
        wallet_id=wallet_id,
        amount=fund_request.amount,
        payment_method_id=fund_request.payment_method_id
    )
    
    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        status=transaction.status,
        amount=transaction.amount
    )

class AddFundsRequest(BaseModel):
    amount: Decimal = Field(..., gt=0, max_digits=15, decimal_places=2)
    payment_method_id: UUID
```

### Transaction History API

#### Get Transaction History
```python
@app.get("/api/v1/transactions", response_model=TransactionHistoryResponse)
async def get_transaction_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """
    Get paginated transaction history
    
    - **page**: Page number (starts from 1)
    - **limit**: Items per page (max 100)
    - **status**: Filter by transaction status
    - **start_date**: Filter from date
    - **end_date**: Filter to date
    """
    
    transactions, total_count = await get_user_transactions(
        user_id=current_user.user_id,
        page=page,
        limit=limit,
        status=status,
        start_date=start_date,
        end_date=end_date
    )
    
    return TransactionHistoryResponse(
        transactions=transactions,
        pagination=PaginationInfo(
            page=page,
            limit=limit,
            total_count=total_count,
            total_pages=math.ceil(total_count / limit)
        )
    )

class TransactionHistoryResponse(BaseModel):
    transactions: List[TransactionSummary]
    pagination: PaginationInfo

class PaginationInfo(BaseModel):
    page: int
    limit: int
    total_count: int
    total_pages: int
```

## WebSocket API

### Real-time Connection
```python
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time updates
    
    - **user_id**: User ID for connection
    """
    
    # Authenticate WebSocket connection
    token = websocket.query_params.get("token")
    user = await authenticate_websocket_token(token, user_id)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    await websocket.accept()
    
    # Register connection
    await register_websocket_connection(user_id, websocket)
    
    try:
        while True:
            # Handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            await handle_websocket_message(user_id, message, websocket)
            
    except WebSocketDisconnect:
        await unregister_websocket_connection(user_id, websocket)
```

## Error Handling

### Standard Error Responses
```python
# Error response model
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None
    timestamp: datetime
    request_id: str

# Custom exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            message=get_error_message(exc.status_code),
            timestamp=datetime.utcnow(),
            request_id=request.headers.get("X-Request-ID", str(uuid.uuid4()))
        ).dict()
    )

# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="Validation Error",
            message="Request validation failed",
            details={"errors": exc.errors()},
            timestamp=datetime.utcnow(),
            request_id=request.headers.get("X-Request-ID", str(uuid.uuid4()))
        ).dict()
    )
```

## API Documentation

### OpenAPI Configuration
```python
# FastAPI app configuration
app = FastAPI(
    title="PayPal Clone API",
    description="Scalable payment processing system API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# API tags for organization
tags_metadata = [
    {"name": "Authentication", "description": "User authentication and authorization"},
    {"name": "Users", "description": "User management operations"},
    {"name": "Payments", "description": "Payment processing operations"},
    {"name": "Wallets", "description": "Wallet and balance management"},
    {"name": "Transactions", "description": "Transaction history and details"},
    {"name": "WebSocket", "description": "Real-time communication"}
]
```

## Rate Limiting

### API Rate Limits
```python
# Rate limiting configuration
rate_limits = {
    "authentication": "10/minute",
    "payments": "100/hour", 
    "wallet_operations": "200/hour",
    "transaction_history": "1000/hour",
    "general_api": "500/hour"
}

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    endpoint = request.url.path
    
    # Check rate limit
    if await is_rate_limited(client_ip, endpoint):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded"}
        )
    
    response = await call_next(request)
    return response
```

## API Versioning

### Version Strategy
```python
# API versioning with path prefix
v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

# Version-specific endpoints
@v1_router.post("/payments/send")
async def send_payment_v1():
    # Version 1 implementation
    pass

@v2_router.post("/payments/send")
async def send_payment_v2():
    # Version 2 with enhanced features
    pass
```