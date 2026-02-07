# Database Design

## Overview
AWS-first database architecture using managed services for high availability, scalability, and operational efficiency.

## Database Services

### PostgreSQL - AWS RDS
**Primary transactional database for ACID compliance**

#### User Service Schema
```sql
-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles
CREATE TABLE user_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    date_of_birth DATE,
    address JSONB,
    kyc_status VARCHAR(20) DEFAULT 'pending',
    kyc_documents JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Account Service Schema
```sql
-- Accounts
CREATE TABLE accounts (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    account_type VARCHAR(20) NOT NULL,
    account_number VARCHAR(50) UNIQUE NOT NULL,
    routing_number VARCHAR(20),
    bank_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payment methods
CREATE TABLE payment_methods (
    method_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    method_type VARCHAR(20) NOT NULL, -- 'card', 'bank', 'wallet'
    encrypted_data TEXT NOT NULL,
    last_four VARCHAR(4),
    expiry_date DATE,
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Transaction Service Schema
```sql
-- Transactions
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID REFERENCES users(user_id),
    receiver_id UUID REFERENCES users(user_id),
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    transaction_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    payment_method_id UUID REFERENCES payment_methods(method_id),
    description TEXT,
    fees DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Transaction events for audit trail
CREATE TABLE transaction_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID REFERENCES transactions(transaction_id),
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Wallet Service Schema
```sql
-- Wallets
CREATE TABLE wallets (
    wallet_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    currency VARCHAR(3) NOT NULL,
    balance DECIMAL(15,2) DEFAULT 0.00,
    available_balance DECIMAL(15,2) DEFAULT 0.00,
    frozen_balance DECIMAL(15,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, currency)
);

-- Balance history
CREATE TABLE balance_history (
    history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wallet_id UUID REFERENCES wallets(wallet_id),
    transaction_id UUID REFERENCES transactions(transaction_id),
    amount DECIMAL(15,2) NOT NULL,
    balance_before DECIMAL(15,2) NOT NULL,
    balance_after DECIMAL(15,2) NOT NULL,
    operation_type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### DynamoDB - Document Storage
**High-performance NoSQL for audit logs and flexible data**

#### Audit Service Tables
```python
# Audit logs table
audit_logs = {
    "TableName": "audit_logs",
    "KeySchema": [
        {"AttributeName": "partition_key", "KeyType": "HASH"},  # service_name#date
        {"AttributeName": "sort_key", "KeyType": "RANGE"}      # timestamp#event_id
    ],
    "AttributeDefinitions": [
        {"AttributeName": "partition_key", "AttributeType": "S"},
        {"AttributeName": "sort_key", "AttributeType": "S"},
        {"AttributeName": "user_id", "AttributeType": "S"},
        {"AttributeName": "transaction_id", "AttributeType": "S"}
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "user_id-index",
            "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}]
        },
        {
            "IndexName": "transaction_id-index", 
            "KeySchema": [{"AttributeName": "transaction_id", "KeyType": "HASH"}]
        }
    ]
}

# Fraud detection data
fraud_data = {
    "TableName": "fraud_detection",
    "KeySchema": [
        {"AttributeName": "user_id", "KeyType": "HASH"},
        {"AttributeName": "timestamp", "KeyType": "RANGE"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "user_id", "AttributeType": "S"},
        {"AttributeName": "timestamp", "AttributeType": "S"}
    ]
}
```

### ElastiCache Redis - Caching Layer
**In-memory caching for high-performance data access**

#### Cache Patterns
```python
# User session cache
user_sessions = {
    "key_pattern": "session:{user_id}",
    "ttl": 3600,  # 1 hour
    "data": {
        "user_id": "uuid",
        "email": "user@example.com",
        "permissions": ["read", "write"],
        "last_activity": "timestamp"
    }
}

# Transaction cache
transaction_cache = {
    "key_pattern": "txn:{transaction_id}",
    "ttl": 1800,  # 30 minutes
    "data": {
        "status": "processing",
        "amount": 100.00,
        "currency": "USD"
    }
}

# Rate limiting
rate_limits = {
    "key_pattern": "rate_limit:{user_id}:{endpoint}",
    "ttl": 60,  # 1 minute
    "data": {
        "count": 10,
        "window_start": "timestamp"
    }
}
```

## AWS RDS Configuration

### Multi-AZ Deployment
```yaml
# RDS Configuration
DBInstance:
  DBInstanceClass: db.r6g.xlarge
  Engine: postgres
  EngineVersion: "15.4"
  MultiAZ: true
  StorageType: gp3
  AllocatedStorage: 100
  StorageEncrypted: true
  BackupRetentionPeriod: 7
  DeletionProtection: true
  
  # Performance Insights
  EnablePerformanceInsights: true
  PerformanceInsightsRetentionPeriod: 7
  
  # Monitoring
  MonitoringInterval: 60
  MonitoringRoleArn: !GetAtt RDSEnhancedMonitoringRole.Arn
```

### Read Replicas
```yaml
# Read replica for reporting
ReadReplica:
  SourceDBInstanceIdentifier: !Ref PrimaryDB
  DBInstanceClass: db.r6g.large
  PubliclyAccessible: false
  MultiAZ: false
```

## DynamoDB Configuration

### Table Settings
```yaml
# Audit logs table
AuditLogsTable:
  BillingMode: ON_DEMAND
  PointInTimeRecoveryEnabled: true
  SSESpecification:
    SSEEnabled: true
    KMSMasterKeyId: alias/dynamodb-key
  StreamSpecification:
    StreamViewType: NEW_AND_OLD_IMAGES
  
  # Global tables for multi-region
  Replicas:
    - Region: us-west-2
    - Region: eu-west-1
```

## Data Consistency Patterns

### ACID Transactions (PostgreSQL)
```python
# Transaction with rollback
async def transfer_money(sender_id, receiver_id, amount):
    async with db.transaction():
        # Debit sender
        await debit_wallet(sender_id, amount)
        # Credit receiver  
        await credit_wallet(receiver_id, amount)
        # Create transaction record
        await create_transaction_record(sender_id, receiver_id, amount)
```

### Eventual Consistency (DynamoDB)
```python
# Audit log with eventual consistency
async def log_audit_event(event_data):
    # Write to DynamoDB (eventually consistent)
    await dynamodb.put_item(
        TableName='audit_logs',
        Item=event_data
    )
    
    # Publish to SQS for downstream processing
    await sqs.send_message(
        QueueUrl=audit_queue_url,
        MessageBody=json.dumps(event_data)
    )
```

## Backup and Recovery

### RDS Automated Backups
- Point-in-time recovery up to 35 days
- Automated snapshots
- Cross-region backup replication

### DynamoDB Backup
- Continuous backups with point-in-time recovery
- On-demand backups
- Cross-region replication

### Disaster Recovery
- RTO: 15 minutes
- RPO: 5 minutes
- Multi-region failover capability

## Performance Optimization

### Database Indexing
```sql
-- Performance indexes
CREATE INDEX CONCURRENTLY idx_transactions_user_date 
ON transactions(sender_id, created_at DESC);

CREATE INDEX CONCURRENTLY idx_transactions_status 
ON transactions(status) WHERE status IN ('pending', 'processing');

CREATE INDEX CONCURRENTLY idx_wallets_user_currency 
ON wallets(user_id, currency);
```

### Connection Pooling
```python
# SQLAlchemy async pool configuration
engine = create_async_engine(
    database_url,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

## Monitoring and Alerts

### CloudWatch Metrics
- Database connections
- CPU utilization
- Read/write IOPS
- Query performance

### Performance Insights
- Top SQL statements
- Wait events
- Database load

### Custom Metrics
- Transaction throughput
- Wallet balance changes
- Fraud detection scores