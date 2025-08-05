# Reliable System Design

## Overview
Building a highly reliable payment system using AWS-native services with fault tolerance, disaster recovery, and high availability patterns.

## Reliability Principles

### 1. Fault Tolerance
**System continues operating despite component failures**

```python
# Circuit breaker implementation for service calls
import asyncio
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open" 
    HALF_OPEN = "half_open"

class ReliableServiceClient:
    def __init__(self, service_url: str, failure_threshold: int = 5, timeout: int = 60):
        self.service_url = service_url
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def call_with_retry(self, endpoint: str, data: dict, max_retries: int = 3):
        """Make service call with circuit breaker and retry logic"""
        
        if self.state == CircuitState.OPEN:
            if not self._should_attempt_reset():
                raise ServiceUnavailableError("Circuit breaker is OPEN")
            self.state = CircuitState.HALF_OPEN
        
        for attempt in range(max_retries + 1):
            try:
                response = await self._make_request(endpoint, data)
                self._on_success()
                return response
                
            except Exception as e:
                if attempt == max_retries:
                    self._on_failure()
                    raise e
                
                # Exponential backoff
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                await asyncio.sleep(wait_time)
    
    async def _make_request(self, endpoint: str, data: dict):
        """Make HTTP request with timeout"""
        
        response = await self.client.post(
            f"{self.service_url}{endpoint}",
            json=data,
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
    
    def _on_success(self):
        """Reset circuit breaker on successful call"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failure and potentially open circuit"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit should attempt reset"""
        return (
            self.last_failure_time and
            datetime.utcnow() - self.last_failure_time > timedelta(seconds=self.timeout)
        )
```

### 2. Graceful Degradation
**Reduce functionality rather than complete failure**

```python
class PaymentService:
    def __init__(self):
        self.fraud_service = ReliableServiceClient("http://fraud-service:8000")
        self.notification_service = ReliableServiceClient("http://notification-service:8000")
        self.wallet_service = ReliableServiceClient("http://wallet-service:8000")
    
    async def process_payment(self, payment_data: dict) -> dict:
        """Process payment with graceful degradation"""
        
        transaction_id = str(uuid.uuid4())
        
        try:
            # Core payment processing (critical path)
            transaction = await self._create_transaction(payment_data, transaction_id)
            
            # Non-critical services with graceful degradation
            await self._handle_non_critical_services(transaction)
            
            return {
                "transaction_id": transaction_id,
                "status": "completed",
                "amount": payment_data["amount"]
            }
            
        except Exception as e:
            logger.error(f"Payment processing failed: {e}")
            await self._handle_payment_failure(transaction_id, e)
            raise
    
    async def _handle_non_critical_services(self, transaction: dict):
        """Handle non-critical services with fallbacks"""
        
        # Fraud check with fallback
        try:
            fraud_result = await self.fraud_service.call_with_retry(
                "/check-fraud", 
                transaction,
                max_retries=2
            )
            
            if fraud_result.get("risk_score", 0) > 80:
                await self._flag_for_manual_review(transaction)
                
        except Exception as e:
            logger.warning(f"Fraud service unavailable, using fallback: {e}")
            # Fallback: Use simple rule-based fraud check
            await self._simple_fraud_check(transaction)
        
        # Notification with fallback
        try:
            await self.notification_service.call_with_retry(
                "/send-notification",
                {
                    "user_id": transaction["sender_id"],
                    "type": "payment_completed",
                    "transaction_id": transaction["transaction_id"]
                },
                max_retries=1
            )
        except Exception as e:
            logger.warning(f"Notification service unavailable: {e}")
            # Fallback: Queue notification for later delivery
            await self._queue_notification(transaction)
    
    async def _simple_fraud_check(self, transaction: dict):
        """Simple rule-based fraud check as fallback"""
        
        # Basic checks when fraud service is down
        amount = transaction.get("amount", 0)
        
        if amount > 10000:  # High amount threshold
            await self._flag_for_manual_review(transaction)
        
        # Check velocity from cache
        user_id = transaction["sender_id"]
        daily_total = await redis.get(f"daily_total:{user_id}") or 0
        
        if float(daily_total) + amount > 50000:  # Daily limit
            await self._flag_for_manual_review(transaction)
```

## High Availability Architecture

### Multi-AZ Deployment
```yaml
# EKS cluster with multi-AZ node groups
EKSCluster:
  Type: AWS::EKS::Cluster
  Properties:
    Name: paypal-clone-cluster
    Version: "1.28"
    RoleArn: !GetAtt EKSClusterRole.Arn
    ResourcesVpcConfig:
      SubnetIds:
        - !Ref PrivateSubnetAZ1
        - !Ref PrivateSubnetAZ2
        - !Ref PrivateSubnetAZ3
      EndpointConfigPrivate: true
      EndpointConfigPublic: true

# Node groups across multiple AZs
NodeGroupAZ1:
  Type: AWS::EKS::Nodegroup
  Properties:
    ClusterName: !Ref EKSCluster
    NodegroupName: paypal-clone-nodes-az1
    Subnets:
      - !Ref PrivateSubnetAZ1
    InstanceTypes:
      - m5.xlarge
    ScalingConfig:
      MinSize: 2
      MaxSize: 10
      DesiredSize: 3

NodeGroupAZ2:
  Type: AWS::EKS::Nodegroup
  Properties:
    ClusterName: !Ref EKSCluster
    NodegroupName: paypal-clone-nodes-az2
    Subnets:
      - !Ref PrivateSubnetAZ2
    InstanceTypes:
      - m5.xlarge
    ScalingConfig:
      MinSize: 2
      MaxSize: 10
      DesiredSize: 3
```

### Database High Availability
```yaml
# RDS Multi-AZ with read replicas
PrimaryDatabase:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceIdentifier: paypal-clone-primary
    DBInstanceClass: db.r6g.xlarge
    Engine: postgres
    EngineVersion: "15.4"
    MultiAZ: true
    AllocatedStorage: 100
    StorageType: gp3
    StorageEncrypted: true
    BackupRetentionPeriod: 7
    PreferredBackupWindow: "03:00-04:00"
    PreferredMaintenanceWindow: "sun:04:00-sun:05:00"
    DeletionProtection: true
    
    # Performance Insights
    EnablePerformanceInsights: true
    PerformanceInsightsRetentionPeriod: 7

# Read replicas for read scaling
ReadReplicaAZ2:
  Type: AWS::RDS::DBInstance
  Properties:
    SourceDBInstanceIdentifier: !Ref PrimaryDatabase
    DBInstanceClass: db.r6g.large
    PubliclyAccessible: false
    MultiAZ: false

ReadReplicaAZ3:
  Type: AWS::RDS::DBInstance
  Properties:
    SourceDBInstanceIdentifier: !Ref PrimaryDatabase
    DBInstanceClass: db.r6g.large
    PubliclyAccessible: false
    MultiAZ: false
```

### Load Balancing Strategy
```python
# Database connection routing
class DatabaseRouter:
    def __init__(self):
        self.primary_db = create_async_engine(PRIMARY_DB_URL)
        self.read_replicas = [
            create_async_engine(READ_REPLICA_1_URL),
            create_async_engine(READ_REPLICA_2_URL)
        ]
        self.replica_index = 0
    
    def get_read_connection(self):
        """Round-robin read replica selection"""
        replica = self.read_replicas[self.replica_index]
        self.replica_index = (self.replica_index + 1) % len(self.read_replicas)
        return replica
    
    def get_write_connection(self):
        """Always use primary for writes"""
        return self.primary_db
    
    async def execute_read_query(self, query: str, params: dict = None):
        """Execute read query on replica"""
        try:
            replica = self.get_read_connection()
            async with replica.begin() as conn:
                result = await conn.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            logger.warning(f"Read replica failed, falling back to primary: {e}")
            # Fallback to primary database
            async with self.primary_db.begin() as conn:
                result = await conn.execute(text(query), params or {})
                return result.fetchall()
    
    async def execute_write_query(self, query: str, params: dict = None):
        """Execute write query on primary"""
        async with self.primary_db.begin() as conn:
            result = await conn.execute(text(query), params or {})
            await conn.commit()
            return result
```

## Disaster Recovery

### Cross-Region Backup Strategy
```python
class DisasterRecoveryService:
    def __init__(self):
        self.primary_region = 'us-east-1'
        self.dr_region = 'us-west-2'
        self.s3_primary = boto3.client('s3', region_name=self.primary_region)
        self.s3_dr = boto3.client('s3', region_name=self.dr_region)
        self.rds_primary = boto3.client('rds', region_name=self.primary_region)
        self.rds_dr = boto3.client('rds', region_name=self.dr_region)
    
    async def create_cross_region_backup(self):
        """Create cross-region backups"""
        
        # Database snapshot
        snapshot_id = f"paypal-clone-snapshot-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Create RDS snapshot
        self.rds_primary.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_id,
            DBInstanceIdentifier='paypal-clone-primary'
        )
        
        # Wait for snapshot completion
        waiter = self.rds_primary.get_waiter('db_snapshot_completed')
        await waiter.wait(DBSnapshotIdentifier=snapshot_id)
        
        # Copy snapshot to DR region
        self.rds_dr.copy_db_snapshot(
            SourceDBSnapshotIdentifier=f'arn:aws:rds:{self.primary_region}:123456789:snapshot:{snapshot_id}',
            TargetDBSnapshotIdentifier=snapshot_id,
            SourceRegion=self.primary_region
        )
        
        # Backup application data to S3
        await self._backup_application_data()
    
    async def _backup_application_data(self):
        """Backup application data and configurations"""
        
        backup_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'kubernetes_configs': await self._export_k8s_configs(),
            'application_configs': await self._export_app_configs(),
            'secrets': await self._export_secrets()
        }
        
        # Upload to primary region S3
        backup_key = f"backups/{datetime.utcnow().strftime('%Y/%m/%d')}/app-backup.json"
        
        self.s3_primary.put_object(
            Bucket='paypal-clone-backups',
            Key=backup_key,
            Body=json.dumps(backup_data),
            ServerSideEncryption='aws:kms'
        )
        
        # Replicate to DR region
        self.s3_dr.copy_object(
            Bucket='paypal-clone-backups-dr',
            Key=backup_key,
            CopySource={
                'Bucket': 'paypal-clone-backups',
                'Key': backup_key,
                'Region': self.primary_region
            }
        )
    
    async def initiate_failover(self):
        """Initiate disaster recovery failover"""
        
        logger.critical("Initiating disaster recovery failover")
        
        # 1. Update DNS to point to DR region
        await self._update_dns_to_dr()
        
        # 2. Restore database from latest snapshot
        await self._restore_database_in_dr()
        
        # 3. Deploy application in DR region
        await self._deploy_application_in_dr()
        
        # 4. Verify system health
        health_check = await self._verify_dr_system_health()
        
        if health_check['healthy']:
            logger.info("Disaster recovery failover completed successfully")
            await self._notify_stakeholders("DR_FAILOVER_SUCCESS")
        else:
            logger.error("Disaster recovery failover failed")
            await self._notify_stakeholders("DR_FAILOVER_FAILED")
            raise Exception("DR failover verification failed")
```

### Automated Failover
```python
class HealthMonitor:
    def __init__(self):
        self.dr_service = DisasterRecoveryService()
        self.health_checks = [
            self._check_api_health,
            self._check_database_health,
            self._check_payment_processing,
            self._check_external_dependencies
        ]
    
    async def continuous_health_monitoring(self):
        """Continuously monitor system health"""
        
        consecutive_failures = 0
        failure_threshold = 3
        
        while True:
            try:
                health_results = []
                
                for health_check in self.health_checks:
                    result = await health_check()
                    health_results.append(result)
                
                overall_health = all(result['healthy'] for result in health_results)
                
                if overall_health:
                    consecutive_failures = 0
                    await self._report_health_status('HEALTHY', health_results)
                else:
                    consecutive_failures += 1
                    await self._report_health_status('UNHEALTHY', health_results)
                    
                    if consecutive_failures >= failure_threshold:
                        logger.critical(f"System unhealthy for {consecutive_failures} consecutive checks")
                        await self._trigger_automated_failover()
                        break
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                consecutive_failures += 1
    
    async def _check_api_health(self) -> dict:
        """Check API endpoint health"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.paypal-clone.com/health",
                    timeout=10.0
                )
                return {
                    'service': 'api',
                    'healthy': response.status_code == 200,
                    'response_time': response.elapsed.total_seconds()
                }
        except Exception as e:
            return {
                'service': 'api',
                'healthy': False,
                'error': str(e)
            }
    
    async def _check_database_health(self) -> dict:
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            
            # Simple query to check database
            async with database.transaction():
                result = await database.fetch_one("SELECT 1 as health_check")
            
            response_time = time.time() - start_time
            
            return {
                'service': 'database',
                'healthy': result is not None,
                'response_time': response_time
            }
        except Exception as e:
            return {
                'service': 'database',
                'healthy': False,
                'error': str(e)
            }
    
    async def _trigger_automated_failover(self):
        """Trigger automated disaster recovery failover"""
        
        logger.critical("Triggering automated failover due to system health failure")
        
        try:
            # Send immediate alert
            await self._send_critical_alert("AUTOMATED_FAILOVER_INITIATED")
            
            # Initiate failover
            await self.dr_service.initiate_failover()
            
        except Exception as e:
            logger.error(f"Automated failover failed: {e}")
            await self._send_critical_alert("AUTOMATED_FAILOVER_FAILED")
```

## Data Consistency & Integrity

### ACID Transaction Management
```python
class TransactionManager:
    def __init__(self):
        self.db = DatabaseRouter()
    
    async def transfer_money(self, sender_id: str, receiver_id: str, amount: Decimal) -> dict:
        """Execute money transfer with ACID guarantees"""
        
        transaction_id = str(uuid.uuid4())
        
        try:
            async with self.db.primary_db.begin() as conn:
                # 1. Lock sender wallet (prevent concurrent modifications)
                sender_wallet = await conn.execute(
                    text("""
                        SELECT wallet_id, balance, available_balance 
                        FROM wallets 
                        WHERE user_id = :user_id AND currency = 'USD'
                        FOR UPDATE
                    """),
                    {"user_id": sender_id}
                )
                sender_wallet = sender_wallet.fetchone()
                
                if not sender_wallet or sender_wallet.available_balance < amount:
                    raise InsufficientFundsError("Insufficient funds")
                
                # 2. Lock receiver wallet
                receiver_wallet = await conn.execute(
                    text("""
                        SELECT wallet_id, balance 
                        FROM wallets 
                        WHERE user_id = :user_id AND currency = 'USD'
                        FOR UPDATE
                    """),
                    {"user_id": receiver_id}
                )
                receiver_wallet = receiver_wallet.fetchone()
                
                if not receiver_wallet:
                    raise ReceiverNotFoundError("Receiver wallet not found")
                
                # 3. Create transaction record
                await conn.execute(
                    text("""
                        INSERT INTO transactions 
                        (transaction_id, sender_id, receiver_id, amount, currency, status, created_at)
                        VALUES (:txn_id, :sender_id, :receiver_id, :amount, 'USD', 'processing', NOW())
                    """),
                    {
                        "txn_id": transaction_id,
                        "sender_id": sender_id,
                        "receiver_id": receiver_id,
                        "amount": amount
                    }
                )
                
                # 4. Update sender balance
                await conn.execute(
                    text("""
                        UPDATE wallets 
                        SET balance = balance - :amount,
                            available_balance = available_balance - :amount,
                            updated_at = NOW()
                        WHERE wallet_id = :wallet_id
                    """),
                    {"amount": amount, "wallet_id": sender_wallet.wallet_id}
                )
                
                # 5. Update receiver balance
                await conn.execute(
                    text("""
                        UPDATE wallets 
                        SET balance = balance + :amount,
                            available_balance = available_balance + :amount,
                            updated_at = NOW()
                        WHERE wallet_id = :wallet_id
                    """),
                    {"amount": amount, "wallet_id": receiver_wallet.wallet_id}
                )
                
                # 6. Create balance history records
                await conn.execute(
                    text("""
                        INSERT INTO balance_history 
                        (wallet_id, transaction_id, amount, balance_before, balance_after, operation_type, created_at)
                        VALUES 
                        (:sender_wallet_id, :txn_id, :negative_amount, :sender_balance_before, :sender_balance_after, 'debit', NOW()),
                        (:receiver_wallet_id, :txn_id, :amount, :receiver_balance_before, :receiver_balance_after, 'credit', NOW())
                    """),
                    {
                        "sender_wallet_id": sender_wallet.wallet_id,
                        "receiver_wallet_id": receiver_wallet.wallet_id,
                        "txn_id": transaction_id,
                        "negative_amount": -amount,
                        "amount": amount,
                        "sender_balance_before": sender_wallet.balance,
                        "sender_balance_after": sender_wallet.balance - amount,
                        "receiver_balance_before": receiver_wallet.balance,
                        "receiver_balance_after": receiver_wallet.balance + amount
                    }
                )
                
                # 7. Update transaction status
                await conn.execute(
                    text("""
                        UPDATE transactions 
                        SET status = 'completed', completed_at = NOW()
                        WHERE transaction_id = :txn_id
                    """),
                    {"txn_id": transaction_id}
                )
                
                # Transaction automatically commits here
                
                return {
                    "transaction_id": transaction_id,
                    "status": "completed",
                    "amount": amount,
                    "sender_id": sender_id,
                    "receiver_id": receiver_id
                }
                
        except Exception as e:
            # Transaction automatically rolls back on exception
            logger.error(f"Transaction failed: {e}")
            
            # Update transaction status to failed
            try:
                async with self.db.primary_db.begin() as conn:
                    await conn.execute(
                        text("""
                            UPDATE transactions 
                            SET status = 'failed', completed_at = NOW()
                            WHERE transaction_id = :txn_id
                        """),
                        {"txn_id": transaction_id}
                    )
            except Exception as update_error:
                logger.error(f"Failed to update transaction status: {update_error}")
            
            raise e
```

## Monitoring & Alerting

### Reliability Metrics
```python
class ReliabilityMetrics:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    
    async def track_sla_metrics(self, service_name: str, response_time: float, success: bool):
        """Track SLA metrics for reliability monitoring"""
        
        # Response time metric
        await self.cloudwatch.put_metric_data(
            Namespace='PayPalClone/Reliability',
            MetricData=[
                {
                    'MetricName': 'ResponseTime',
                    'Value': response_time,
                    'Unit': 'Milliseconds',
                    'Dimensions': [
                        {'Name': 'Service', 'Value': service_name}
                    ]
                },
                {
                    'MetricName': 'RequestCount',
                    'Value': 1,
                    'Unit': 'Count',
                    'Dimensions': [
                        {'Name': 'Service', 'Value': service_name},
                        {'Name': 'Status', 'Value': 'success' if success else 'failure'}
                    ]
                }
            ]
        )
    
    async def calculate_availability(self, service_name: str, time_period: int = 3600) -> float:
        """Calculate service availability percentage"""
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(seconds=time_period)
        
        # Get success and failure counts
        response = await self.cloudwatch.get_metric_statistics(
            Namespace='PayPalClone/Reliability',
            MetricName='RequestCount',
            Dimensions=[
                {'Name': 'Service', 'Value': service_name}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=time_period,
            Statistics=['Sum']
        )
        
        total_requests = sum(point['Sum'] for point in response['Datapoints'])
        
        if total_requests == 0:
            return 100.0  # No requests = 100% availability
        
        # Get failure count
        failure_response = await self.cloudwatch.get_metric_statistics(
            Namespace='PayPalClone/Reliability',
            MetricName='RequestCount',
            Dimensions=[
                {'Name': 'Service', 'Value': service_name},
                {'Name': 'Status', 'Value': 'failure'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=time_period,
            Statistics=['Sum']
        )
        
        total_failures = sum(point['Sum'] for point in failure_response['Datapoints'])
        
        availability = ((total_requests - total_failures) / total_requests) * 100
        return round(availability, 2)
```

## Chaos Engineering

### Fault Injection Testing
```python
class ChaosEngineering:
    def __init__(self):
        self.enabled = os.getenv('CHAOS_ENGINEERING_ENABLED', 'false').lower() == 'true'
        self.failure_rate = float(os.getenv('CHAOS_FAILURE_RATE', '0.01'))  # 1% failure rate
    
    async def inject_latency(self, min_delay: float = 0.1, max_delay: float = 2.0):
        """Inject random latency to test timeout handling"""
        
        if not self.enabled or random.random() > self.failure_rate:
            return
        
        delay = random.uniform(min_delay, max_delay)
        logger.warning(f"Chaos Engineering: Injecting {delay:.2f}s latency")
        await asyncio.sleep(delay)
    
    async def inject_failure(self, failure_type: str = "generic"):
        """Inject random failures to test error handling"""
        
        if not self.enabled or random.random() > self.failure_rate:
            return
        
        logger.warning(f"Chaos Engineering: Injecting {failure_type} failure")
        
        if failure_type == "database":
            raise DatabaseConnectionError("Chaos: Database connection failed")
        elif failure_type == "network":
            raise NetworkError("Chaos: Network timeout")
        elif failure_type == "service":
            raise ServiceUnavailableError("Chaos: Service temporarily unavailable")
        else:
            raise Exception(f"Chaos: Random {failure_type} failure")
    
    def chaos_decorator(self, failure_type: str = "generic"):
        """Decorator to add chaos engineering to functions"""
        
        def decorator(func):
            async def wrapper(*args, **kwargs):
                await self.inject_latency()
                await self.inject_failure(failure_type)
                return await func(*args, **kwargs)
            return wrapper
        return decorator

# Usage in services
chaos = ChaosEngineering()

@chaos.chaos_decorator("database")
async def get_user_balance(user_id: str) -> float:
    """Get user balance with chaos engineering"""
    # Normal function logic
    pass
```