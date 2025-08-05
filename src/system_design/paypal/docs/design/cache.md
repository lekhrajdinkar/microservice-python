# Cache Design

## Overview
AWS ElastiCache Redis-based caching strategy for high-performance data access, session management, and real-time operations.

## AWS ElastiCache Redis Architecture

### Cluster Configuration
```yaml
# ElastiCache Redis Cluster
RedisCluster:
  CacheNodeType: cache.r7g.xlarge
  Engine: redis
  EngineVersion: "7.0"
  NumCacheNodes: 3
  
  # Cluster Mode
  ReplicationGroupDescription: "PayPal Clone Redis Cluster"
  NumNodeGroups: 3
  ReplicasPerNodeGroup: 2
  
  # Security
  AtRestEncryptionEnabled: true
  TransitEncryptionEnabled: true
  AuthToken: !Ref RedisAuthToken
  
  # Backup
  SnapshotRetentionLimit: 7
  SnapshotWindow: "03:00-05:00"
  
  # Multi-AZ
  MultiAZEnabled: true
  AutomaticFailoverEnabled: true
```

## Caching Patterns

### 1. Cache-Aside Pattern
**User Profile Caching**
```python
async def get_user_profile(user_id: str):
    cache_key = f"user_profile:{user_id}"
    
    # Try cache first
    cached_profile = await redis.get(cache_key)
    if cached_profile:
        return json.loads(cached_profile)
    
    # Cache miss - fetch from database
    profile = await db.fetch_user_profile(user_id)
    
    # Store in cache with TTL
    await redis.setex(
        cache_key, 
        3600,  # 1 hour TTL
        json.dumps(profile)
    )
    
    return profile
```

### 2. Write-Through Pattern
**Wallet Balance Updates**
```python
async def update_wallet_balance(wallet_id: str, new_balance: float):
    cache_key = f"wallet_balance:{wallet_id}"
    
    # Update database first
    await db.update_wallet_balance(wallet_id, new_balance)
    
    # Update cache immediately
    await redis.setex(
        cache_key,
        1800,  # 30 minutes TTL
        str(new_balance)
    )
    
    # Publish balance change event
    await redis.publish(
        f"balance_updates:{wallet_id}",
        json.dumps({"balance": new_balance, "timestamp": time.time()})
    )
```

### 3. Write-Behind Pattern
**Audit Log Buffering**
```python
async def buffer_audit_log(event_data: dict):
    buffer_key = f"audit_buffer:{event_data['service']}"
    
    # Add to Redis list (buffer)
    await redis.lpush(buffer_key, json.dumps(event_data))
    
    # Set expiry if new buffer
    await redis.expire(buffer_key, 300)  # 5 minutes
    
    # Trigger batch write if buffer is full
    buffer_size = await redis.llen(buffer_key)
    if buffer_size >= 100:
        await flush_audit_buffer(buffer_key)
```

## Cache Data Models

### Session Management
```python
# User session cache
session_data = {
    "key_pattern": "session:{session_id}",
    "ttl": 3600,  # 1 hour
    "data": {
        "user_id": "uuid",
        "email": "user@example.com",
        "roles": ["user", "verified"],
        "permissions": ["read", "write", "transfer"],
        "last_activity": "2024-01-01T12:00:00Z",
        "ip_address": "192.168.1.1",
        "device_info": "Mozilla/5.0..."
    }
}

# JWT token blacklist
blacklisted_tokens = {
    "key_pattern": "blacklist:{token_jti}",
    "ttl": 86400,  # 24 hours (token expiry)
    "data": {
        "user_id": "uuid",
        "blacklisted_at": "timestamp",
        "reason": "logout"
    }
}
```

### Transaction Caching
```python
# Active transaction cache
transaction_cache = {
    "key_pattern": "txn:{transaction_id}",
    "ttl": 1800,  # 30 minutes
    "data": {
        "transaction_id": "uuid",
        "sender_id": "uuid",
        "receiver_id": "uuid",
        "amount": 100.00,
        "currency": "USD",
        "status": "processing",
        "created_at": "timestamp",
        "payment_method": "card_ending_1234"
    }
}

# Transaction status updates
transaction_status = {
    "key_pattern": "txn_status:{transaction_id}",
    "ttl": 3600,  # 1 hour
    "data": {
        "status": "completed",
        "updated_at": "timestamp",
        "completion_time": "timestamp"
    }
}
```

### Rate Limiting
```python
# API rate limiting
rate_limit_data = {
    "key_pattern": "rate_limit:{user_id}:{endpoint}",
    "ttl": 60,  # 1 minute window
    "data": {
        "count": 10,
        "window_start": "timestamp",
        "limit": 100
    }
}

# Sliding window rate limiting
sliding_window = {
    "key_pattern": "sliding:{user_id}:{endpoint}",
    "ttl": 3600,  # 1 hour
    "data_structure": "sorted_set",  # Redis ZSET
    "score": "timestamp",
    "member": "request_id"
}
```

### Fraud Detection Cache
```python
# User risk score cache
risk_scores = {
    "key_pattern": "risk_score:{user_id}",
    "ttl": 300,  # 5 minutes
    "data": {
        "score": 75,
        "factors": ["new_device", "unusual_amount"],
        "last_updated": "timestamp",
        "expires_at": "timestamp"
    }
}

# Device fingerprinting
device_cache = {
    "key_pattern": "device:{device_fingerprint}",
    "ttl": 86400,  # 24 hours
    "data": {
        "user_id": "uuid",
        "first_seen": "timestamp",
        "last_seen": "timestamp",
        "trusted": true,
        "location": "US-CA-San Francisco"
    }
}
```

## Real-time Features with Redis

### WebSocket Connection Management
```python
# Active WebSocket connections
websocket_connections = {
    "key_pattern": "ws_conn:{user_id}",
    "ttl": 7200,  # 2 hours
    "data_structure": "set",
    "members": ["connection_id_1", "connection_id_2"]
}

# Connection metadata
connection_metadata = {
    "key_pattern": "ws_meta:{connection_id}",
    "ttl": 7200,  # 2 hours
    "data": {
        "user_id": "uuid",
        "connected_at": "timestamp",
        "last_ping": "timestamp",
        "client_info": "mobile_app_v1.2"
    }
}
```

### Pub/Sub for Real-time Notifications
```python
# Redis Pub/Sub channels
channels = {
    "user_notifications": "notifications:{user_id}",
    "transaction_updates": "transactions:{transaction_id}",
    "balance_changes": "balance:{wallet_id}",
    "fraud_alerts": "fraud:{user_id}",
    "system_announcements": "system:announcements"
}

# Publisher example
async def publish_transaction_update(transaction_id: str, status: str):
    channel = f"transactions:{transaction_id}"
    message = {
        "type": "status_update",
        "transaction_id": transaction_id,
        "status": status,
        "timestamp": time.time()
    }
    
    await redis.publish(channel, json.dumps(message))
```

## Cache Invalidation Strategies

### Time-based Expiration (TTL)
```python
# Different TTL strategies
cache_ttl_config = {
    "user_profile": 3600,      # 1 hour - relatively static
    "wallet_balance": 300,     # 5 minutes - frequently changing
    "exchange_rates": 60,      # 1 minute - real-time data
    "fraud_scores": 300,       # 5 minutes - security sensitive
    "session_data": 1800,      # 30 minutes - security balance
    "rate_limits": 60          # 1 minute - sliding window
}
```

### Event-driven Invalidation
```python
# Cache invalidation on events
async def handle_user_profile_update(user_id: str):
    # Invalidate user profile cache
    await redis.delete(f"user_profile:{user_id}")
    
    # Invalidate related caches
    await redis.delete(f"user_permissions:{user_id}")
    await redis.delete(f"user_preferences:{user_id}")

async def handle_transaction_completion(transaction_id: str):
    # Update transaction cache
    await redis.delete(f"txn:{transaction_id}")
    
    # Invalidate wallet balance caches
    transaction = await get_transaction(transaction_id)
    await redis.delete(f"wallet_balance:{transaction['sender_wallet']}")
    await redis.delete(f"wallet_balance:{transaction['receiver_wallet']}")
```

### Cache Warming
```python
# Proactive cache warming
async def warm_user_cache(user_id: str):
    """Warm cache with frequently accessed user data"""
    
    # Warm user profile
    await get_user_profile(user_id)
    
    # Warm wallet balances
    wallets = await get_user_wallets(user_id)
    for wallet in wallets:
        await get_wallet_balance(wallet['wallet_id'])
    
    # Warm recent transactions
    await get_recent_transactions(user_id, limit=10)
```

## Performance Optimization

### Connection Pooling
```python
# Redis connection pool
redis_pool = redis.ConnectionPool(
    host=redis_cluster_endpoint,
    port=6379,
    password=redis_auth_token,
    ssl=True,
    ssl_cert_reqs=None,
    max_connections=50,
    retry_on_timeout=True,
    socket_keepalive=True,
    socket_keepalive_options={}
)

redis_client = redis.Redis(connection_pool=redis_pool)
```

### Pipeline Operations
```python
# Batch operations with pipeline
async def batch_cache_operations(operations: list):
    pipe = redis.pipeline()
    
    for op in operations:
        if op['type'] == 'set':
            pipe.setex(op['key'], op['ttl'], op['value'])
        elif op['type'] == 'get':
            pipe.get(op['key'])
        elif op['type'] == 'delete':
            pipe.delete(op['key'])
    
    results = await pipe.execute()
    return results
```

### Memory Optimization
```python
# Memory-efficient data structures
memory_config = {
    "maxmemory_policy": "allkeys-lru",
    "maxmemory": "4gb",
    "hash_max_ziplist_entries": 512,
    "hash_max_ziplist_value": 64,
    "list_max_ziplist_size": -2,
    "set_max_intset_entries": 512,
    "zset_max_ziplist_entries": 128
}
```

## Monitoring and Alerting

### CloudWatch Metrics
```python
# Custom cache metrics
cache_metrics = {
    "cache_hit_rate": "percentage",
    "cache_miss_rate": "percentage", 
    "average_response_time": "milliseconds",
    "memory_utilization": "percentage",
    "connection_count": "count",
    "evicted_keys": "count_per_second"
}
```

### Cache Health Checks
```python
async def cache_health_check():
    """Monitor cache health and performance"""
    
    try:
        # Test basic operations
        test_key = "health_check"
        await redis.setex(test_key, 60, "ok")
        result = await redis.get(test_key)
        await redis.delete(test_key)
        
        # Check cluster info
        cluster_info = await redis.cluster_info()
        
        # Check memory usage
        memory_info = await redis.info("memory")
        
        return {
            "status": "healthy",
            "response_time": "< 1ms",
            "memory_usage": memory_info.get("used_memory_human"),
            "cluster_state": cluster_info.get("cluster_state")
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
```

## Disaster Recovery

### Cross-Region Replication
```yaml
# Global Datastore for cross-region replication
GlobalDatastore:
  GlobalReplicationGroupDescription: "PayPal Clone Global Cache"
  PrimaryReplicationGroupId: !Ref PrimaryRedisCluster
  
  # Secondary regions
  Members:
    - ReplicationGroupId: !Ref SecondaryRedisCluster
      ReplicationGroupRegion: us-west-2
      Role: SECONDARY
```

### Backup Strategy
- Automated daily snapshots
- Point-in-time recovery
- Cross-region backup replication
- 7-day retention policy