# Security Design

## Overview
Comprehensive security architecture using AWS-native services for authentication, authorization, encryption, and threat protection in the PayPal clone system.

## AWS Security Services Integration

### AWS Cognito for Authentication
```yaml
# Cognito User Pool
UserPool:
  Type: AWS::Cognito::UserPool
  Properties:
    UserPoolName: paypal-clone-users
    Policies:
      PasswordPolicy:
        MinimumLength: 12
        RequireUppercase: true
        RequireLowercase: true
        RequireNumbers: true
        RequireSymbols: true
        TemporaryPasswordValidityDays: 1
    
    # MFA Configuration
    MfaConfiguration: OPTIONAL
    EnabledMfas:
      - SMS_MFA
      - SOFTWARE_TOKEN_MFA
    
    # Account Recovery
    AccountRecoverySetting:
      RecoveryMechanisms:
        - Name: verified_email
          Priority: 1
        - Name: verified_phone_number
          Priority: 2
    
    # User Attributes
    Schema:
      - Name: email
        Required: true
        Mutable: false
      - Name: phone_number
        Required: true
        Mutable: true
      - Name: kyc_status
        AttributeDataType: String
        Mutable: true

# Cognito Identity Pool
IdentityPool:
  Type: AWS::Cognito::IdentityPool
  Properties:
    IdentityPoolName: paypal-clone-identity
    AllowUnauthenticatedIdentities: false
    CognitoIdentityProviders:
      - ClientId: !Ref UserPoolClient
        ProviderName: !GetAtt UserPool.ProviderName
```

### AWS WAF for API Protection
```yaml
# WAF Web ACL
WebACL:
  Type: AWS::WAFv2::WebACL
  Properties:
    Name: paypal-clone-waf
    Scope: REGIONAL
    DefaultAction:
      Allow: {}
    
    Rules:
      # Rate limiting rule
      - Name: RateLimitRule
        Priority: 1
        Statement:
          RateBasedStatement:
            Limit: 2000
            AggregateKeyType: IP
        Action:
          Block: {}
        VisibilityConfig:
          SampledRequestsEnabled: true
          CloudWatchMetricsEnabled: true
          MetricName: RateLimitRule
      
      # SQL injection protection
      - Name: SQLInjectionRule
        Priority: 2
        Statement:
          SqliMatchStatement:
            FieldToMatch:
              Body: {}
            TextTransformations:
              - Priority: 0
                Type: URL_DECODE
              - Priority: 1
                Type: HTML_ENTITY_DECODE
        Action:
          Block: {}
        VisibilityConfig:
          SampledRequestsEnabled: true
          CloudWatchMetricsEnabled: true
          MetricName: SQLInjectionRule
      
      # XSS protection
      - Name: XSSRule
        Priority: 3
        Statement:
          XssMatchStatement:
            FieldToMatch:
              Body: {}
            TextTransformations:
              - Priority: 0
                Type: URL_DECODE
              - Priority: 1
                Type: HTML_ENTITY_DECODE
        Action:
          Block: {}
```

## Authentication & Authorization

### JWT Token Implementation
```python
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets

class JWTManager:
    def __init__(self):
        self.secret_key = self._get_secret_from_secrets_manager()
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
    
    def _get_secret_from_secrets_manager(self) -> str:
        """Retrieve JWT secret from AWS Secrets Manager"""
        import boto3
        
        client = boto3.client('secretsmanager', region_name='us-east-1')
        response = client.get_secret_value(SecretId='paypal-clone/jwt-secret')
        return response['SecretString']
    
    def create_access_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        payload = {
            "sub": user_data["user_id"],
            "email": user_data["email"],
            "roles": user_data.get("roles", ["user"]),
            "permissions": user_data.get("permissions", []),
            "kyc_status": user_data.get("kyc_status", "pending"),
            "iat": datetime.utcnow(),
            "exp": expire,
            "jti": secrets.token_urlsafe(32),  # JWT ID for blacklisting
            "token_type": "access"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token"""
        
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        payload = {
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": expire,
            "jti": secrets.token_urlsafe(32),
            "token_type": "refresh"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check if token is blacklisted
            if await self.is_token_blacklisted(payload.get("jti")):
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    async def blacklist_token(self, jti: str, exp: datetime):
        """Add token to blacklist in Redis"""
        
        ttl = int((exp - datetime.utcnow()).total_seconds())
        if ttl > 0:
            await redis.setex(f"blacklist:{jti}", ttl, "1")
    
    async def is_token_blacklisted(self, jti: str) -> bool:
        """Check if token is blacklisted"""
        
        result = await redis.get(f"blacklist:{jti}")
        return result is not None
```

### Role-Based Access Control (RBAC)
```python
from enum import Enum
from typing import List, Set

class Permission(Enum):
    READ_PROFILE = "read:profile"
    WRITE_PROFILE = "write:profile"
    SEND_MONEY = "send:money"
    RECEIVE_MONEY = "receive:money"
    VIEW_TRANSACTIONS = "view:transactions"
    MANAGE_PAYMENT_METHODS = "manage:payment_methods"
    ADMIN_ACCESS = "admin:access"
    FRAUD_REVIEW = "fraud:review"

class Role(Enum):
    USER = "user"
    VERIFIED_USER = "verified_user"
    PREMIUM_USER = "premium_user"
    ADMIN = "admin"
    FRAUD_ANALYST = "fraud_analyst"

# Role-Permission mapping
ROLE_PERMISSIONS = {
    Role.USER: {
        Permission.READ_PROFILE,
        Permission.WRITE_PROFILE,
        Permission.RECEIVE_MONEY,
        Permission.VIEW_TRANSACTIONS
    },
    Role.VERIFIED_USER: {
        Permission.READ_PROFILE,
        Permission.WRITE_PROFILE,
        Permission.SEND_MONEY,
        Permission.RECEIVE_MONEY,
        Permission.VIEW_TRANSACTIONS,
        Permission.MANAGE_PAYMENT_METHODS
    },
    Role.PREMIUM_USER: {
        Permission.READ_PROFILE,
        Permission.WRITE_PROFILE,
        Permission.SEND_MONEY,
        Permission.RECEIVE_MONEY,
        Permission.VIEW_TRANSACTIONS,
        Permission.MANAGE_PAYMENT_METHODS
    },
    Role.ADMIN: {perm for perm in Permission},
    Role.FRAUD_ANALYST: {
        Permission.READ_PROFILE,
        Permission.VIEW_TRANSACTIONS,
        Permission.FRAUD_REVIEW
    }
}

def has_permission(user_roles: List[str], required_permission: Permission) -> bool:
    """Check if user has required permission"""
    
    user_permissions = set()
    for role_str in user_roles:
        try:
            role = Role(role_str)
            user_permissions.update(ROLE_PERMISSIONS.get(role, set()))
        except ValueError:
            continue
    
    return required_permission in user_permissions

# FastAPI dependency for permission checking
def require_permission(permission: Permission):
    def permission_checker(current_user: dict = Depends(get_current_user)):
        if not has_permission(current_user.get("roles", []), permission):
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient permissions. Required: {permission.value}"
            )
        return current_user
    return permission_checker

# Usage in endpoints
@app.post("/api/v1/payments/send")
async def send_payment(
    payment_data: SendPaymentRequest,
    current_user: dict = Depends(require_permission(Permission.SEND_MONEY))
):
    # Payment logic here
    pass
```

## Data Encryption

### AWS KMS Integration
```python
import boto3
from cryptography.fernet import Fernet
import base64

class EncryptionService:
    def __init__(self):
        self.kms = boto3.client('kms', region_name='us-east-1')
        self.key_id = 'arn:aws:kms:us-east-1:123456789:key/12345678-1234-1234-1234-123456789012'
    
    async def encrypt_sensitive_data(self, plaintext: str) -> str:
        """Encrypt sensitive data using AWS KMS"""
        
        try:
            response = self.kms.encrypt(
                KeyId=self.key_id,
                Plaintext=plaintext.encode('utf-8')
            )
            
            # Return base64 encoded ciphertext
            return base64.b64encode(response['CiphertextBlob']).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    async def decrypt_sensitive_data(self, ciphertext: str) -> str:
        """Decrypt sensitive data using AWS KMS"""
        
        try:
            ciphertext_blob = base64.b64decode(ciphertext.encode('utf-8'))
            
            response = self.kms.decrypt(CiphertextBlob=ciphertext_blob)
            
            return response['Plaintext'].decode('utf-8')
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    async def generate_data_key(self) -> tuple:
        """Generate data encryption key for envelope encryption"""
        
        response = self.kms.generate_data_key(
            KeyId=self.key_id,
            KeySpec='AES_256'
        )
        
        return response['Plaintext'], response['CiphertextBlob']

# Envelope encryption for large data
class EnvelopeEncryption:
    def __init__(self, kms_service: EncryptionService):
        self.kms = kms_service
    
    async def encrypt_large_data(self, data: bytes) -> dict:
        """Encrypt large data using envelope encryption"""
        
        # Generate data encryption key
        plaintext_key, encrypted_key = await self.kms.generate_data_key()
        
        # Encrypt data with data key
        fernet = Fernet(base64.urlsafe_b64encode(plaintext_key[:32]))
        encrypted_data = fernet.encrypt(data)
        
        return {
            'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8'),
            'encrypted_key': base64.b64encode(encrypted_key).decode('utf-8')
        }
    
    async def decrypt_large_data(self, encrypted_package: dict) -> bytes:
        """Decrypt large data using envelope encryption"""
        
        # Decrypt data key
        encrypted_key = base64.b64decode(encrypted_package['encrypted_key'])
        response = self.kms.kms.decrypt(CiphertextBlob=encrypted_key)
        plaintext_key = response['Plaintext']
        
        # Decrypt data
        fernet = Fernet(base64.urlsafe_b64encode(plaintext_key[:32]))
        encrypted_data = base64.b64decode(encrypted_package['encrypted_data'])
        
        return fernet.decrypt(encrypted_data)
```

### Database Encryption
```python
# SQLAlchemy with encryption
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

class EncryptedUser(Base):
    __tablename__ = 'users'
    
    user_id = Column(UUID, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    
    # Encrypted sensitive fields
    ssn = Column(EncryptedType(String, secret_key, AesEngine, 'pkcs5'))
    phone = Column(EncryptedType(String, secret_key, AesEngine, 'pkcs5'))
    
    # Hash for password (never encrypt passwords, always hash)
    password_hash = Column(String(255), nullable=False)

# Payment method encryption
class EncryptedPaymentMethod(Base):
    __tablename__ = 'payment_methods'
    
    method_id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.user_id'))
    
    # Encrypted card/account data
    encrypted_data = Column(Text, nullable=False)  # KMS encrypted
    last_four = Column(String(4))  # Safe to store unencrypted
    
    async def set_card_data(self, card_number: str, cvv: str, expiry: str):
        """Encrypt and store card data"""
        
        card_data = {
            'number': card_number,
            'cvv': cvv,
            'expiry': expiry
        }
        
        encryption_service = EncryptionService()
        self.encrypted_data = await encryption_service.encrypt_sensitive_data(
            json.dumps(card_data)
        )
        self.last_four = card_number[-4:]
    
    async def get_card_data(self) -> dict:
        """Decrypt and return card data"""
        
        encryption_service = EncryptionService()
        decrypted_json = await encryption_service.decrypt_sensitive_data(
            self.encrypted_data
        )
        return json.loads(decrypted_json)
```

## Fraud Detection & Prevention

### AWS Fraud Detector Integration
```python
import boto3
from typing import Dict, Any

class FraudDetectionService:
    def __init__(self):
        self.fraud_detector = boto3.client('frauddetector', region_name='us-east-1')
        self.detector_name = 'paypal-clone-fraud-detector'
        self.detector_version = '1.0'
    
    async def evaluate_transaction_risk(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate transaction for fraud risk"""
        
        # Prepare event data for fraud detector
        event_variables = {
            'user_id': transaction_data['sender_id'],
            'amount': str(transaction_data['amount']),
            'currency': transaction_data['currency'],
            'payment_method': transaction_data['payment_method_type'],
            'ip_address': transaction_data.get('ip_address', ''),
            'device_fingerprint': transaction_data.get('device_fingerprint', ''),
            'transaction_time': transaction_data['timestamp'],
            'merchant_category': 'peer_to_peer'
        }
        
        try:
            response = self.fraud_detector.get_event_prediction(
                detectorId=self.detector_name,
                detectorVersionId=self.detector_version,
                eventId=transaction_data['transaction_id'],
                eventTypeName='payment_transaction',
                entities=[
                    {
                        'entityType': 'customer',
                        'entityId': transaction_data['sender_id']
                    }
                ],
                eventVariables=event_variables
            )
            
            # Extract risk score and outcomes
            model_scores = response.get('modelScores', [])
            rule_results = response.get('ruleResults', [])
            
            risk_score = 0
            if model_scores:
                risk_score = max([score['scores']['fraud_score'] for score in model_scores])
            
            # Determine action based on outcomes
            outcomes = response.get('outcomes', [])
            action = 'approve'  # default
            
            for outcome in outcomes:
                if outcome == 'block':
                    action = 'block'
                    break
                elif outcome == 'review':
                    action = 'review'
            
            return {
                'risk_score': risk_score,
                'action': action,
                'rule_results': rule_results,
                'model_scores': model_scores
            }
            
        except Exception as e:
            logger.error(f"Fraud detection failed: {e}")
            # Fail safe - allow transaction but flag for review
            return {
                'risk_score': 50,
                'action': 'review',
                'error': str(e)
            }
    
    async def update_fraud_feedback(self, transaction_id: str, is_fraud: bool):
        """Provide feedback to improve fraud detection model"""
        
        try:
            self.fraud_detector.put_event_feedback(
                eventId=transaction_id,
                eventTypeName='payment_transaction',
                feedbackValue='fraud' if is_fraud else 'legit'
            )
        except Exception as e:
            logger.error(f"Failed to update fraud feedback: {e}")

# Real-time fraud scoring
class RealTimeFraudScoring:
    def __init__(self):
        self.redis = redis.Redis()
        self.fraud_detector = FraudDetectionService()
    
    async def calculate_risk_score(self, user_id: str, transaction_data: dict) -> int:
        """Calculate real-time risk score"""
        
        risk_factors = []
        
        # Check velocity (transaction frequency)
        velocity_score = await self._check_velocity(user_id)
        risk_factors.append(velocity_score)
        
        # Check device/location anomalies
        device_score = await self._check_device_anomaly(user_id, transaction_data)
        risk_factors.append(device_score)
        
        # Check amount anomalies
        amount_score = await self._check_amount_anomaly(user_id, transaction_data['amount'])
        risk_factors.append(amount_score)
        
        # Check time-based patterns
        time_score = await self._check_time_anomaly(user_id, transaction_data['timestamp'])
        risk_factors.append(time_score)
        
        # AWS Fraud Detector score
        aws_fraud_result = await self.fraud_detector.evaluate_transaction_risk(transaction_data)
        risk_factors.append(aws_fraud_result['risk_score'])
        
        # Weighted average of all risk factors
        final_score = sum(risk_factors) / len(risk_factors)
        
        return min(100, max(0, int(final_score)))
    
    async def _check_velocity(self, user_id: str) -> int:
        """Check transaction velocity"""
        
        # Count transactions in last hour
        key = f"velocity:{user_id}:hour"
        count = await self.redis.get(key) or 0
        
        if int(count) > 10:  # More than 10 transactions per hour
            return 80
        elif int(count) > 5:
            return 40
        else:
            return 10
    
    async def _check_device_anomaly(self, user_id: str, transaction_data: dict) -> int:
        """Check for device/location anomalies"""
        
        device_fingerprint = transaction_data.get('device_fingerprint')
        ip_address = transaction_data.get('ip_address')
        
        # Check if device is known
        known_devices_key = f"known_devices:{user_id}"
        is_known_device = await self.redis.sismember(known_devices_key, device_fingerprint)
        
        if not is_known_device:
            return 60  # New device increases risk
        
        # Check IP geolocation (simplified)
        # In production, use actual geolocation service
        return 20  # Known device, lower risk
```

## Security Monitoring

### AWS GuardDuty Integration
```python
import boto3

class SecurityMonitoring:
    def __init__(self):
        self.guardduty = boto3.client('guardduty', region_name='us-east-1')
        self.cloudtrail = boto3.client('cloudtrail', region_name='us-east-1')
    
    async def check_security_findings(self):
        """Check GuardDuty findings"""
        
        try:
            # Get detector ID
            detectors = self.guardduty.list_detectors()
            if not detectors['DetectorIds']:
                return []
            
            detector_id = detectors['DetectorIds'][0]
            
            # Get findings
            findings = self.guardduty.list_findings(
                DetectorId=detector_id,
                FindingCriteria={
                    'Criterion': {
                        'severity': {
                            'Gte': 4.0  # Medium severity and above
                        },
                        'updatedAt': {
                            'Gte': int((datetime.utcnow() - timedelta(hours=1)).timestamp() * 1000)
                        }
                    }
                }
            )
            
            return findings['FindingIds']
            
        except Exception as e:
            logger.error(f"Failed to check security findings: {e}")
            return []
    
    async def log_security_event(self, event_type: str, user_id: str, details: dict):
        """Log security events for audit"""
        
        security_event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'details': details,
            'source_ip': details.get('ip_address'),
            'user_agent': details.get('user_agent')
        }
        
        # Store in DynamoDB for analysis
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('security_events')
        
        await table.put_item(Item=security_event)
        
        # Send to CloudWatch for monitoring
        cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        
        await cloudwatch.put_metric_data(
            Namespace='PayPalClone/Security',
            MetricData=[
                {
                    'MetricName': f'SecurityEvent_{event_type}',
                    'Value': 1,
                    'Unit': 'Count',
                    'Dimensions': [
                        {
                            'Name': 'EventType',
                            'Value': event_type
                        }
                    ]
                }
            ]
        )
```

## Compliance & Audit

### PCI DSS Compliance
```python
class PCIComplianceService:
    def __init__(self):
        self.encryption_service = EncryptionService()
    
    async def mask_card_number(self, card_number: str) -> str:
        """Mask card number for PCI compliance"""
        
        if len(card_number) < 8:
            return "*" * len(card_number)
        
        # Show first 6 and last 4 digits
        return card_number[:6] + "*" * (len(card_number) - 10) + card_number[-4:]
    
    async def log_card_access(self, user_id: str, card_id: str, action: str):
        """Log card data access for audit"""
        
        audit_log = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'card_id': card_id,
            'action': action,
            'compliance_requirement': 'PCI_DSS'
        }
        
        # Store in secure audit log
        await self.store_audit_log(audit_log)
    
    async def validate_pci_environment(self) -> dict:
        """Validate PCI DSS environment requirements"""
        
        checks = {
            'encryption_at_rest': await self._check_encryption_at_rest(),
            'encryption_in_transit': await self._check_encryption_in_transit(),
            'access_controls': await self._check_access_controls(),
            'network_segmentation': await self._check_network_segmentation(),
            'vulnerability_scanning': await self._check_vulnerability_scanning()
        }
        
        return {
            'compliant': all(checks.values()),
            'checks': checks
        }
```

## Security Headers & CORS

### FastAPI Security Configuration
```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://paypal-clone.com", "https://app.paypal-clone.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["paypal-clone.com", "*.paypal-clone.com"]
)
```