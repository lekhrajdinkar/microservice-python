# Scalable System Design

## Overview
Designing a horizontally scalable payment system using AWS-native services with auto-scaling, load balancing, and distributed architecture patterns.

## Horizontal Scaling Architecture

### Kubernetes Auto-scaling
```yaml
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-service-hpa
  namespace: paypal-clone
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60

---
# Vertical Pod Autoscaler
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: payment-service-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: payment-service
      maxAllowed:
        cpu: 2
        memory: 4Gi
      minAllowed:
        cpu: 100m
        memory: 128Mi
```

### Cluster Auto-scaling
```yaml
# EKS Cluster Autoscaler
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      containers:
      - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.21.0
        name: cluster-autoscaler
        resources:
          limits:
            cpu: 100m
            memory: 300Mi
          requests:
            cpu: 100m
            memory: 300Mi
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/paypal-clone-cluster
        - --balance-similar-node-groups
        - --scale-down-enabled=true
        - --scale-down-delay-after-add=10m
        - --scale-down-unneeded-time=10m
        - --max-node-provision-time=15m
```

## Load Balancing Strategy

### Application Load Balancer
```python
# FastAPI with load balancer health checks
from fastapi import FastAPI, Request
import psutil
import asyncio

app = FastAPI()

class LoadBalancerHealthCheck:
    def __init__(self):
        self.healthy = True
        self.max_cpu_percent = 90
        self.max_memory_percent = 85
        self.max_active_connections = 1000
        self.active_connections = 0
    
    async def health_check(self) -> dict:
        """Comprehensive health check for load balancer"""
        
        # System resource checks
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        # Application-specific checks
        db_healthy = await self._check_database_health()
        cache_healthy = await self._check_cache_health()
        
        # Determine overall health
        is_healthy = (
            cpu_percent < self.max_cpu_percent and
            memory_percent < self.max_memory_percent and
            self.active_connections < self.max_active_connections and
            db_healthy and
            cache_healthy
        )
        
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "active_connections": self.active_connections,
                "database_healthy": db_healthy,
                "cache_healthy": cache_healthy
            }
        }
    
    async def _check_database_health(self) -> bool:
        """Check database connectivity"""
        try:
            async with database.transaction():
                await database.fetch_one("SELECT 1")
            return True
        except Exception:
            return False
    
    async def _check_cache_health(self) -> bool:
        """Check Redis cache connectivity"""
        try:
            await redis.ping()
            return True
        except Exception:
            return False

health_checker = LoadBalancerHealthCheck()

@app.get("/health")
async def health_endpoint():
    """Health check endpoint for load balancer"""
    health_status = await health_checker.health_check()
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return JSONResponse(content=health_status, status_code=status_code)

@app.middleware("http")
async def track_connections(request: Request, call_next):
    """Track active connections for load balancing decisions"""
    
    health_checker.active_connections += 1
    try:
        response = await call_next(request)
        return response
    finally:
        health_checker.active_connections -= 1
```

### Database Connection Pooling
```python
# Scalable database connection management
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import QueuePool

class ScalableDatabaseManager:
    def __init__(self):
        self.primary_engine = None
        self.read_replicas = []
        self.connection_pools = {}
        self.setup_connection_pools()
    
    def setup_connection_pools(self):
        """Setup connection pools for different database roles"""
        
        # Primary database pool (writes)
        self.primary_engine = create_async_engine(
            PRIMARY_DB_URL,
            poolclass=QueuePool,
            pool_size=20,          # Base connections
            max_overflow=50,       # Additional connections under load
            pool_pre_ping=True,    # Validate connections
            pool_recycle=3600,     # Recycle connections every hour
            pool_timeout=30,       # Timeout for getting connection
            echo=False
        )
        
        # Read replica pools
        for i, replica_url in enumerate(READ_REPLICA_URLS):
            engine = create_async_engine(
                replica_url,
                poolclass=QueuePool,
                pool_size=15,
                max_overflow=30,
                pool_pre_ping=True,
                pool_recycle=3600,
                pool_timeout=30
            )
            self.read_replicas.append(engine)
    
    async def get_read_session(self) -> AsyncSession:
        """Get read session with load balancing"""
        
        # Simple round-robin for read replicas
        replica_index = hash(asyncio.current_task()) % len(self.read_replicas)
        engine = self.read_replicas[replica_index]
        
        return AsyncSession(engine, expire_on_commit=False)
    
    async def get_write_session(self) -> AsyncSession:
        """Get write session (always primary)"""
        
        return AsyncSession(self.primary_engine, expire_on_commit=False)
    
    async def execute_read_query(self, query, params=None):
        """Execute read query with automatic retry on replica failure"""
        
        for attempt in range(len(self.read_replicas) + 1):  # +1 for primary fallback
            try:
                if attempt < len(self.read_replicas):
                    # Try read replica
                    engine = self.read_replicas[attempt]
                    async with AsyncSession(engine) as session:
                        result = await session.execute(query, params or {})
                        return result.fetchall()
                else:
                    # Fallback to primary
                    async with AsyncSession(self.primary_engine) as session:
                        result = await session.execute(query, params or {})
                        return result.fetchall()
                        
            except Exception as e:
                logger.warning(f"Database read attempt {attempt + 1} failed: {e}")
                if attempt == len(self.read_replicas):  # Last attempt
                    raise e
                continue

db_manager = ScalableDatabaseManager()
```

## Caching Strategy for Scale

### Multi-Level Caching
```python
class MultiLevelCache:
    def __init__(self):
        # L1: In-memory cache (fastest, smallest)
        self.l1_cache = {}
        self.l1_max_size = 1000
        self.l1_ttl = 60  # 1 minute
        
        # L2: Redis cache (fast, larger)
        self.redis = redis.Redis(
            host=REDIS_CLUSTER_ENDPOINT,
            port=6379,
            password=REDIS_AUTH_TOKEN,
            ssl=True,
            connection_pool_kwargs={
                'max_connections': 50,
                'retry_on_timeout': True
            }
        )
        
        # L3: Database (slowest, authoritative)
        self.db = db_manager
    
    async def get(self, key: str, fetch_func=None):
        """Multi-level cache get with automatic population"""
        
        # L1 Cache check
        l1_result = self._get_from_l1(key)
        if l1_result is not None:
            return l1_result
        
        # L2 Cache check
        l2_result = await self._get_from_l2(key)
        if l2_result is not None:
            # Populate L1 cache
            self._set_to_l1(key, l2_result)
            return l2_result
        
        # L3 Database fetch
        if fetch_func:
            db_result = await fetch_func()
            if db_result is not None:
                # Populate both cache levels
                await self._set_to_l2(key, db_result, ttl=300)  # 5 minutes
                self._set_to_l1(key, db_result)
                return db_result
        
        return None
    
    async def set(self, key: str, value, ttl: int = 300):
        """Set value in all cache levels"""
        
        # Set in all levels
        self._set_to_l1(key, value)
        await self._set_to_l2(key, value, ttl)
    
    async def invalidate(self, key: str):
        """Invalidate key from all cache levels"""
        
        # Remove from L1
        self.l1_cache.pop(key, None)
        
        # Remove from L2
        await self.redis.delete(key)
    
    def _get_from_l1(self, key: str):
        """Get from L1 in-memory cache"""
        
        if key in self.l1_cache:
            value, expiry = self.l1_cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.l1_cache[key]
        return None
    
    def _set_to_l1(self, key: str, value):
        """Set to L1 in-memory cache with LRU eviction"""
        
        # LRU eviction if cache is full
        if len(self.l1_cache) >= self.l1_max_size:
            oldest_key = min(self.l1_cache.keys(), 
                           key=lambda k: self.l1_cache[k][1])
            del self.l1_cache[oldest_key]
        
        expiry = time.time() + self.l1_ttl
        self.l1_cache[key] = (value, expiry)
    
    async def _get_from_l2(self, key: str):
        """Get from L2 Redis cache"""
        
        try:
            result = await self.redis.get(key)
            if result:
                return json.loads(result)
        except Exception as e:
            logger.warning(f"L2 cache get failed: {e}")
        return None
    
    async def _set_to_l2(self, key: str, value, ttl: int):
        """Set to L2 Redis cache"""
        
        try:
            await self.redis.setex(key, ttl, json.dumps(value, default=str))
        except Exception as e:
            logger.warning(f"L2 cache set failed: {e}")

# Usage in services
cache = MultiLevelCache()

async def get_user_profile(user_id: str) -> dict:
    """Get user profile with multi-level caching"""
    
    cache_key = f"user_profile:{user_id}"
    
    async def fetch_from_db():
        async with db_manager.get_read_session() as session:
            result = await session.execute(
                text("SELECT * FROM users WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            return result.fetchone()._asdict() if result.fetchone() else None
    
    return await cache.get(cache_key, fetch_from_db)
```

## Message Queue Scaling

### SQS Auto-scaling
```python
class ScalableMessageProcessor:
    def __init__(self):
        self.sqs = boto3.client('sqs', region_name='us-east-1')
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        self.queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789/payment-processing'
        self.min_workers = 2
        self.max_workers = 20
        self.current_workers = self.min_workers
        self.worker_tasks = []
    
    async def auto_scale_workers(self):
        """Auto-scale message processing workers based on queue depth"""
        
        while True:
            try:
                # Get queue metrics
                queue_depth = await self._get_queue_depth()
                avg_processing_time = await self._get_avg_processing_time()
                
                # Calculate optimal worker count
                optimal_workers = self._calculate_optimal_workers(
                    queue_depth, avg_processing_time
                )
                
                # Scale workers
                await self._scale_workers(optimal_workers)
                
                # Wait before next scaling decision
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Auto-scaling error: {e}")
                await asyncio.sleep(60)
    
    async def _get_queue_depth(self) -> int:
        """Get current queue depth from SQS"""
        
        response = await self.sqs.get_queue_attributes(
            QueueUrl=self.queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
        )
        
        return int(response['Attributes']['ApproximateNumberOfMessages'])
    
    async def _get_avg_processing_time(self) -> float:
        """Get average message processing time from CloudWatch"""
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=10)
        
        response = await self.cloudwatch.get_metric_statistics(
            Namespace='PayPalClone/MessageProcessing',
            MetricName='ProcessingTime',
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average']
        )
        
        if response['Datapoints']:
            return response['Datapoints'][-1]['Average']
        return 5.0  # Default 5 seconds
    
    def _calculate_optimal_workers(self, queue_depth: int, avg_processing_time: float) -> int:
        """Calculate optimal number of workers"""
        
        # Target: Process all messages within 5 minutes
        target_processing_time = 300  # 5 minutes
        
        # Calculate workers needed
        messages_per_worker_per_second = 1 / avg_processing_time
        total_capacity_needed = queue_depth / target_processing_time
        optimal_workers = int(total_capacity_needed / messages_per_worker_per_second)
        
        # Apply constraints
        optimal_workers = max(self.min_workers, optimal_workers)
        optimal_workers = min(self.max_workers, optimal_workers)
        
        return optimal_workers
    
    async def _scale_workers(self, target_workers: int):
        """Scale worker count to target"""
        
        if target_workers > self.current_workers:
            # Scale up
            new_workers = target_workers - self.current_workers
            for _ in range(new_workers):
                task = asyncio.create_task(self._message_worker())
                self.worker_tasks.append(task)
            
            logger.info(f"Scaled up to {target_workers} workers")
            
        elif target_workers < self.current_workers:
            # Scale down
            workers_to_remove = self.current_workers - target_workers
            for _ in range(workers_to_remove):
                if self.worker_tasks:
                    task = self.worker_tasks.pop()
                    task.cancel()
            
            logger.info(f"Scaled down to {target_workers} workers")
        
        self.current_workers = target_workers
    
    async def _message_worker(self):
        """Individual message processing worker"""
        
        while True:
            try:
                # Receive messages from SQS
                response = await self.sqs.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=20,  # Long polling
                    MessageAttributeNames=['All']
                )
                
                messages = response.get('Messages', [])
                
                for message in messages:
                    start_time = time.time()
                    
                    try:
                        # Process message
                        await self._process_message(message)
                        
                        # Delete message after successful processing
                        await self.sqs.delete_message(
                            QueueUrl=self.queue_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
                        
                        # Record processing time
                        processing_time = (time.time() - start_time) * 1000
                        await self._record_processing_time(processing_time)
                        
                    except Exception as e:
                        logger.error(f"Message processing failed: {e}")
                        # Message will be retried or sent to DLQ
                
            except asyncio.CancelledError:
                logger.info("Worker cancelled")
                break
            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(5)  # Brief pause before retry
    
    async def _process_message(self, message: dict):
        """Process individual message"""
        
        message_body = json.loads(message['Body'])
        message_type = message_body.get('type')
        
        if message_type == 'payment_processing':
            await self._process_payment_message(message_body)
        elif message_type == 'notification':
            await self._process_notification_message(message_body)
        else:
            logger.warning(f"Unknown message type: {message_type}")
    
    async def _record_processing_time(self, processing_time: float):
        """Record processing time metric"""
        
        await self.cloudwatch.put_metric_data(
            Namespace='PayPalClone/MessageProcessing',
            MetricData=[
                {
                    'MetricName': 'ProcessingTime',
                    'Value': processing_time,
                    'Unit': 'Milliseconds'
                }
            ]
        )
```

## Database Sharding Strategy

### Horizontal Partitioning
```python
class DatabaseShardManager:
    def __init__(self):
        self.shards = {
            'shard_0': create_async_engine(SHARD_0_URL),
            'shard_1': create_async_engine(SHARD_1_URL),
            'shard_2': create_async_engine(SHARD_2_URL),
            'shard_3': create_async_engine(SHARD_3_URL)
        }
        self.shard_count = len(self.shards)
    
    def get_shard_key(self, user_id: str) -> str:
        """Determine shard based on user ID"""
        
        # Use consistent hashing
        hash_value = hashlib.md5(user_id.encode()).hexdigest()
        shard_index = int(hash_value, 16) % self.shard_count
        return f'shard_{shard_index}'
    
    async def get_user_data(self, user_id: str) -> dict:
        """Get user data from appropriate shard"""
        
        shard_key = self.get_shard_key(user_id)
        engine = self.shards[shard_key]
        
        async with AsyncSession(engine) as session:
            result = await session.execute(
                text("SELECT * FROM users WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            return result.fetchone()._asdict() if result.fetchone() else None
    
    async def create_user(self, user_data: dict) -> str:
        """Create user in appropriate shard"""
        
        user_id = str(uuid.uuid4())
        shard_key = self.get_shard_key(user_id)
        engine = self.shards[shard_key]
        
        async with AsyncSession(engine) as session:
            await session.execute(
                text("""
                    INSERT INTO users (user_id, email, first_name, last_name, created_at)
                    VALUES (:user_id, :email, :first_name, :last_name, NOW())
                """),
                {
                    "user_id": user_id,
                    "email": user_data["email"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"]
                }
            )
            await session.commit()
        
        return user_id
    
    async def cross_shard_query(self, query: str, params: dict = None) -> list:
        """Execute query across all shards (use sparingly)"""
        
        results = []
        
        # Execute query on all shards in parallel
        tasks = []
        for shard_key, engine in self.shards.items():
            task = self._execute_on_shard(engine, query, params)
            tasks.append(task)
        
        shard_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in shard_results:
            if isinstance(result, Exception):
                logger.error(f"Shard query failed: {result}")
            else:
                results.extend(result)
        
        return results
    
    async def _execute_on_shard(self, engine, query: str, params: dict):
        """Execute query on specific shard"""
        
        async with AsyncSession(engine) as session:
            result = await session.execute(text(query), params or {})
            return [row._asdict() for row in result.fetchall()]

shard_manager = DatabaseShardManager()
```

## Performance Monitoring

### Scalability Metrics
```python
class ScalabilityMonitor:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        self.metrics_buffer = []
        self.buffer_size = 100
    
    async def track_throughput(self, service_name: str, operation: str, count: int = 1):
        """Track service throughput"""
        
        metric = {
            'MetricName': 'Throughput',
            'Value': count,
            'Unit': 'Count/Second',
            'Dimensions': [
                {'Name': 'Service', 'Value': service_name},
                {'Name': 'Operation', 'Value': operation}
            ],
            'Timestamp': datetime.utcnow()
        }
        
        self.metrics_buffer.append(metric)
        
        if len(self.metrics_buffer) >= self.buffer_size:
            await self._flush_metrics()
    
    async def track_resource_utilization(self, resource_type: str, utilization: float):
        """Track resource utilization for scaling decisions"""
        
        await self.cloudwatch.put_metric_data(
            Namespace='PayPalClone/Scalability',
            MetricData=[
                {
                    'MetricName': 'ResourceUtilization',
                    'Value': utilization,
                    'Unit': 'Percent',
                    'Dimensions': [
                        {'Name': 'ResourceType', 'Value': resource_type}
                    ]
                }
            ]
        )
    
    async def _flush_metrics(self):
        """Flush metrics buffer to CloudWatch"""
        
        if not self.metrics_buffer:
            return
        
        try:
            await self.cloudwatch.put_metric_data(
                Namespace='PayPalClone/Scalability',
                MetricData=self.metrics_buffer
            )
            self.metrics_buffer.clear()
        except Exception as e:
            logger.error(f"Failed to flush metrics: {e}")

scalability_monitor = ScalabilityMonitor()
```

## Cost Optimization

### Resource Right-sizing
```python
class CostOptimizer:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        self.ec2 = boto3.client('ec2', region_name='us-east-1')
    
    async def analyze_resource_usage(self) -> dict:
        """Analyze resource usage for cost optimization"""
        
        # Get CPU utilization for last 7 days
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=7)
        
        cpu_metrics = await self.cloudwatch.get_metric_statistics(
            Namespace='AWS/EKS',
            MetricName='CPUUtilization',
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,  # 1 hour periods
            Statistics=['Average', 'Maximum']
        )
        
        # Analyze utilization patterns
        avg_cpu = sum(point['Average'] for point in cpu_metrics['Datapoints']) / len(cpu_metrics['Datapoints'])
        max_cpu = max(point['Maximum'] for point in cpu_metrics['Datapoints'])
        
        recommendations = []
        
        if avg_cpu < 30:
            recommendations.append({
                'type': 'downsize',
                'reason': f'Average CPU utilization is only {avg_cpu:.1f}%',
                'potential_savings': '30-50%'
            })
        elif avg_cpu > 80:
            recommendations.append({
                'type': 'upsize',
                'reason': f'Average CPU utilization is {avg_cpu:.1f}%',
                'risk': 'Performance degradation'
            })
        
        return {
            'avg_cpu_utilization': avg_cpu,
            'max_cpu_utilization': max_cpu,
            'recommendations': recommendations
        }
    
    async def implement_spot_instances(self):
        """Implement spot instances for cost savings"""
        
        # Use spot instances for non-critical workloads
        spot_fleet_config = {
            'IamFleetRole': 'arn:aws:iam::123456789:role/aws-ec2-spot-fleet-role',
            'AllocationStrategy': 'diversified',
            'TargetCapacity': 10,
            'SpotPrice': '0.05',
            'LaunchSpecifications': [
                {
                    'ImageId': 'ami-12345678',
                    'InstanceType': 'm5.large',
                    'KeyName': 'paypal-clone-key',
                    'SecurityGroups': [{'GroupId': 'sg-12345678'}],
                    'SubnetId': 'subnet-12345678',
                    'UserData': base64.b64encode(b'#!/bin/bash\n# Setup script').decode()
                }
            ]
        }
        
        response = await self.ec2.request_spot_fleet(
            SpotFleetRequestConfig=spot_fleet_config
        )
        
        return response['SpotFleetRequestId']
```