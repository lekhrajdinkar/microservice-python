# Monitoring Strategy

## Overview
Comprehensive monitoring strategy using DataDog as the primary observability platform with AWS-native services for a complete view of system health, performance, and business metrics.

## Monitoring Architecture

```
┌─────────────────┐    Metrics/Logs    ┌─────────────────┐
│   Application   │──────────────────►│   DataDog       │
│   Services      │                   │   Platform      │
└─────────────────┘                   └─────────────────┘
         │                                       │
         │ Custom Metrics                        │ Alerts
         ▼                                       ▼
┌─────────────────┐                   ┌─────────────────┐
│   DataDog       │                   │   AWS SNS       │
│   StatsD        │                   │   Notifications │
└─────────────────┘                   └─────────────────┘
         │                                       │
         │ Infrastructure                        │ PagerDuty
         ▼                                       ▼
┌─────────────────┐                   ┌─────────────────┐
│   AWS           │                   │   Slack/Email   │
│   CloudWatch    │                   │   Integrations  │
└─────────────────┘                   └─────────────────┘
```

## Business Metrics Monitoring

### Key Performance Indicators (KPIs)
```python
import datadog
from datadog import statsd
from typing import Dict, Any
import asyncio

class BusinessMetricsCollector:
    def __init__(self):
        # Initialize DataDog
        datadog.initialize(
            api_key=os.getenv('DATADOG_API_KEY'),
            app_key=os.getenv('DATADOG_APP_KEY')
        )
        
        self.statsd = statsd
        self.statsd.constant_tags = [
            f'environment:{os.getenv("ENVIRONMENT", "production")}',
            f'service:paypal-clone',
            f'version:{os.getenv("APP_VERSION", "1.0.0")}'
        ]
    
    async def track_transaction_metrics(self, transaction_data: Dict[str, Any]):
        """Track transaction-related business metrics"""
        
        # Transaction volume
        self.statsd.increment(
            'business.transactions.count',
            tags=[
                f'currency:{transaction_data["currency"]}',
                f'type:{transaction_data["transaction_type"]}',
                f'status:{transaction_data["status"]}'
            ]
        )
        
        # Transaction value
        self.statsd.histogram(
            'business.transactions.amount',
            transaction_data['amount'],
            tags=[
                f'currency:{transaction_data["currency"]}',
                f'type:{transaction_data["transaction_type"]}'
            ]
        )
        
        # Processing time
        if 'processing_time_ms' in transaction_data:
            self.statsd.histogram(
                'business.transactions.processing_time',
                transaction_data['processing_time_ms'],
                tags=[f'type:{transaction_data["transaction_type"]}']
            )
        
        # Success rate
        success = transaction_data['status'] == 'completed'
        self.statsd.increment(
            'business.transactions.success_rate',
            tags=[
                f'success:{success}',
                f'type:{transaction_data["transaction_type"]}'
            ]
        )
    
    async def track_user_metrics(self, user_event: Dict[str, Any]):
        """Track user-related business metrics"""
        
        event_type = user_event['event_type']
        
        # User registrations
        if event_type == 'user_registered':
            self.statsd.increment('business.users.registrations')
            
        # User verifications
        elif event_type == 'user_verified':
            self.statsd.increment('business.users.verifications')
            
        # Active users
        elif event_type == 'user_login':
            self.statsd.increment('business.users.active')
            
        # User retention (daily/monthly active users)
        self.statsd.set(
            'business.users.unique_daily',
            user_event['user_id'],
            tags=['period:daily']
        )
    
    async def track_revenue_metrics(self, revenue_data: Dict[str, Any]):
        """Track revenue and financial metrics"""
        
        # Total revenue
        self.statsd.histogram(
            'business.revenue.total',
            revenue_data['amount'],
            tags=[
                f'currency:{revenue_data["currency"]}',
                f'source:{revenue_data["revenue_source"]}'
            ]
        )
        
        # Fee revenue
        if 'fee_amount' in revenue_data:
            self.statsd.histogram(
                'business.revenue.fees',
                revenue_data['fee_amount'],
                tags=[f'currency:{revenue_data["currency"]}']
            )
        
        # Average transaction value
        self.statsd.histogram(
            'business.revenue.avg_transaction_value',
            revenue_data['amount'],
            tags=[f'currency:{revenue_data["currency"]}']
        )
    
    async def track_fraud_metrics(self, fraud_data: Dict[str, Any]):
        """Track fraud detection metrics"""
        
        # Fraud detection rate
        self.statsd.histogram(
            'business.fraud.risk_score',
            fraud_data['risk_score'],
            tags=[f'action:{fraud_data["action"]}']
        )
        
        # Blocked transactions
        if fraud_data['action'] == 'block':
            self.statsd.increment(
                'business.fraud.blocked_transactions',
                tags=[f'reason:{fraud_data.get("reason", "high_risk")}']
            )
        
        # False positives (if available)
        if 'is_false_positive' in fraud_data:
            self.statsd.increment(
                'business.fraud.false_positives',
                tags=[f'false_positive:{fraud_data["is_false_positive"]}']
            )

business_metrics = BusinessMetricsCollector()
```

### Real-time Dashboard Metrics
```python
class RealTimeDashboard:
    def __init__(self):
        self.redis = redis.Redis(
            host=REDIS_ENDPOINT,
            port=6379,
            password=REDIS_AUTH_TOKEN,
            ssl=True
        )
        self.statsd = statsd
    
    async def update_real_time_counters(self):
        """Update real-time counters for dashboard"""
        
        # Get current metrics from Redis
        current_hour = datetime.utcnow().strftime('%Y%m%d%H')
        
        # Transaction counts
        hourly_transactions = await self.redis.get(f'hourly_transactions:{current_hour}') or 0
        daily_transactions = await self.redis.get(f'daily_transactions:{datetime.utcnow().strftime("%Y%m%d")}') or 0
        
        # Revenue totals
        hourly_revenue = await self.redis.get(f'hourly_revenue:{current_hour}') or 0
        daily_revenue = await self.redis.get(f'daily_revenue:{datetime.utcnow().strftime("%Y%m%d")}') or 0
        
        # Active users
        active_users_5min = await self.redis.scard('active_users:5min')
        active_users_1hour = await self.redis.scard('active_users:1hour')
        
        # Send to DataDog
        self.statsd.gauge('dashboard.transactions.hourly', int(hourly_transactions))
        self.statsd.gauge('dashboard.transactions.daily', int(daily_transactions))
        self.statsd.gauge('dashboard.revenue.hourly', float(hourly_revenue))
        self.statsd.gauge('dashboard.revenue.daily', float(daily_revenue))
        self.statsd.gauge('dashboard.users.active_5min', active_users_5min)
        self.statsd.gauge('dashboard.users.active_1hour', active_users_1hour)
    
    async def increment_transaction_counter(self, amount: float, currency: str):
        """Increment real-time transaction counters"""
        
        current_hour = datetime.utcnow().strftime('%Y%m%d%H')
        current_day = datetime.utcnow().strftime('%Y%m%d')
        
        # Increment counters
        await self.redis.incr(f'hourly_transactions:{current_hour}')
        await self.redis.incr(f'daily_transactions:{current_day}')
        
        # Add to revenue
        await self.redis.incrbyfloat(f'hourly_revenue:{current_hour}', amount)
        await self.redis.incrbyfloat(f'daily_revenue:{current_day}', amount)
        
        # Set expiry for cleanup
        await self.redis.expire(f'hourly_transactions:{current_hour}', 86400)  # 24 hours
        await self.redis.expire(f'daily_transactions:{current_day}', 604800)   # 7 days

dashboard = RealTimeDashboard()
```

## Technical Metrics Monitoring

### Application Performance Monitoring
```python
class TechnicalMetricsCollector:
    def __init__(self):
        self.statsd = statsd
    
    async def track_api_performance(self, endpoint: str, method: str, 
                                  response_time: float, status_code: int):
        """Track API endpoint performance"""
        
        # Response time
        self.statsd.histogram(
            'api.response_time',
            response_time,
            tags=[
                f'endpoint:{endpoint}',
                f'method:{method}',
                f'status_code:{status_code}'
            ]
        )
        
        # Request count
        self.statsd.increment(
            'api.requests',
            tags=[
                f'endpoint:{endpoint}',
                f'method:{method}',
                f'status_code:{status_code}'
            ]
        )
        
        # Error rate
        is_error = status_code >= 400
        self.statsd.increment(
            'api.errors',
            tags=[
                f'endpoint:{endpoint}',
                f'method:{method}',
                f'error:{is_error}'
            ]
        )
    
    async def track_database_performance(self, operation: str, 
                                       execution_time: float, success: bool):
        """Track database operation performance"""
        
        # Query execution time
        self.statsd.histogram(
            'database.query_time',
            execution_time,
            tags=[
                f'operation:{operation}',
                f'success:{success}'
            ]
        )
        
        # Connection pool metrics
        pool_info = await self.get_connection_pool_info()
        self.statsd.gauge('database.pool.active_connections', pool_info['active'])
        self.statsd.gauge('database.pool.idle_connections', pool_info['idle'])
        self.statsd.gauge('database.pool.total_connections', pool_info['total'])
    
    async def track_cache_performance(self, operation: str, hit: bool, 
                                    response_time: float):
        """Track cache performance metrics"""
        
        # Cache hit/miss rate
        self.statsd.increment(
            'cache.operations',
            tags=[
                f'operation:{operation}',
                f'hit:{hit}'
            ]
        )
        
        # Cache response time
        self.statsd.histogram(
            'cache.response_time',
            response_time,
            tags=[f'operation:{operation}']
        )
        
        # Cache hit ratio (calculated metric)
        if operation == 'get':
            self.statsd.increment(
                'cache.hit_ratio',
                tags=[f'result:{"hit" if hit else "miss"}']
            )
    
    async def track_message_queue_metrics(self, queue_name: str, 
                                        message_count: int, processing_time: float):
        """Track message queue performance"""
        
        # Queue depth
        self.statsd.gauge(
            'queue.depth',
            message_count,
            tags=[f'queue:{queue_name}']
        )
        
        # Message processing time
        self.statsd.histogram(
            'queue.processing_time',
            processing_time,
            tags=[f'queue:{queue_name}']
        )
        
        # Throughput
        self.statsd.increment(
            'queue.messages_processed',
            tags=[f'queue:{queue_name}']
        )

technical_metrics = TechnicalMetricsCollector()
```

### Infrastructure Monitoring
```python
class InfrastructureMonitor:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        self.statsd = statsd
    
    async def collect_kubernetes_metrics(self):
        """Collect Kubernetes cluster metrics"""
        
        # Get cluster metrics from Kubernetes API
        k8s_metrics = await self.get_k8s_metrics()
        
        # Pod metrics
        self.statsd.gauge('k8s.pods.running', k8s_metrics['pods']['running'])
        self.statsd.gauge('k8s.pods.pending', k8s_metrics['pods']['pending'])
        self.statsd.gauge('k8s.pods.failed', k8s_metrics['pods']['failed'])
        
        # Node metrics
        self.statsd.gauge('k8s.nodes.ready', k8s_metrics['nodes']['ready'])
        self.statsd.gauge('k8s.nodes.not_ready', k8s_metrics['nodes']['not_ready'])
        
        # Resource utilization
        self.statsd.gauge('k8s.cpu.utilization', k8s_metrics['cpu']['utilization'])
        self.statsd.gauge('k8s.memory.utilization', k8s_metrics['memory']['utilization'])
        
        # HPA metrics
        for hpa in k8s_metrics['hpa']:
            self.statsd.gauge(
                'k8s.hpa.current_replicas',
                hpa['current_replicas'],
                tags=[f'deployment:{hpa["name"]}']
            )
            self.statsd.gauge(
                'k8s.hpa.desired_replicas',
                hpa['desired_replicas'],
                tags=[f'deployment:{hpa["name"]}']
            )
    
    async def collect_aws_metrics(self):
        """Collect AWS service metrics"""
        
        # RDS metrics
        rds_metrics = await self.get_rds_metrics()
        self.statsd.gauge('aws.rds.cpu_utilization', rds_metrics['cpu_utilization'])
        self.statsd.gauge('aws.rds.database_connections', rds_metrics['connections'])
        self.statsd.gauge('aws.rds.read_iops', rds_metrics['read_iops'])
        self.statsd.gauge('aws.rds.write_iops', rds_metrics['write_iops'])
        
        # ElastiCache metrics
        redis_metrics = await self.get_redis_metrics()
        self.statsd.gauge('aws.redis.cpu_utilization', redis_metrics['cpu_utilization'])
        self.statsd.gauge('aws.redis.memory_utilization', redis_metrics['memory_utilization'])
        self.statsd.gauge('aws.redis.cache_hits', redis_metrics['cache_hits'])
        self.statsd.gauge('aws.redis.cache_misses', redis_metrics['cache_misses'])
        
        # SQS metrics
        sqs_metrics = await self.get_sqs_metrics()
        for queue_name, metrics in sqs_metrics.items():
            self.statsd.gauge(
                'aws.sqs.messages_visible',
                metrics['messages_visible'],
                tags=[f'queue:{queue_name}']
            )
            self.statsd.gauge(
                'aws.sqs.messages_in_flight',
                metrics['messages_in_flight'],
                tags=[f'queue:{queue_name}']
            )
    
    async def get_rds_metrics(self) -> Dict[str, float]:
        """Get RDS performance metrics from CloudWatch"""
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)
        
        metrics = {}
        
        # CPU Utilization
        cpu_response = await self.cloudwatch.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='CPUUtilization',
            Dimensions=[
                {'Name': 'DBInstanceIdentifier', 'Value': 'paypal-clone-primary'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average']
        )
        
        if cpu_response['Datapoints']:
            metrics['cpu_utilization'] = cpu_response['Datapoints'][-1]['Average']
        
        # Database Connections
        conn_response = await self.cloudwatch.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='DatabaseConnections',
            Dimensions=[
                {'Name': 'DBInstanceIdentifier', 'Value': 'paypal-clone-primary'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average']
        )
        
        if conn_response['Datapoints']:
            metrics['connections'] = conn_response['Datapoints'][-1]['Average']
        
        return metrics

infrastructure_monitor = InfrastructureMonitor()
```

## Health Checks & Synthetic Monitoring

### Application Health Checks
```python
class HealthCheckMonitor:
    def __init__(self):
        self.statsd = statsd
        self.health_checks = [
            self.check_database_health,
            self.check_redis_health,
            self.check_external_services_health,
            self.check_message_queue_health
        ]
    
    async def run_health_checks(self):
        """Run all health checks and report status"""
        
        overall_health = True
        health_results = {}
        
        for health_check in self.health_checks:
            try:
                start_time = time.time()
                result = await health_check()
                response_time = (time.time() - start_time) * 1000
                
                health_results[health_check.__name__] = {
                    'healthy': result['healthy'],
                    'response_time': response_time,
                    'details': result.get('details', {})
                }
                
                # Report to DataDog
                self.statsd.gauge(
                    'health_check.status',
                    1 if result['healthy'] else 0,
                    tags=[f'check:{health_check.__name__}']
                )
                
                self.statsd.histogram(
                    'health_check.response_time',
                    response_time,
                    tags=[f'check:{health_check.__name__}']
                )
                
                if not result['healthy']:
                    overall_health = False
                    
            except Exception as e:
                logger.error(f"Health check {health_check.__name__} failed: {e}")
                health_results[health_check.__name__] = {
                    'healthy': False,
                    'error': str(e)
                }
                overall_health = False
        
        # Report overall health
        self.statsd.gauge('health_check.overall', 1 if overall_health else 0)
        
        return {
            'overall_healthy': overall_health,
            'checks': health_results,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and performance"""
        
        try:
            start_time = time.time()
            
            # Test primary database
            async with db_manager.get_write_session() as session:
                result = await session.execute(text("SELECT 1 as health_check"))
                primary_healthy = result.fetchone() is not None
            
            primary_time = time.time() - start_time
            
            # Test read replica
            start_time = time.time()
            async with db_manager.get_read_session() as session:
                result = await session.execute(text("SELECT 1 as health_check"))
                replica_healthy = result.fetchone() is not None
            
            replica_time = time.time() - start_time
            
            return {
                'healthy': primary_healthy and replica_healthy,
                'details': {
                    'primary_response_time': primary_time,
                    'replica_response_time': replica_time,
                    'primary_healthy': primary_healthy,
                    'replica_healthy': replica_healthy
                }
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    async def check_redis_health(self) -> Dict[str, Any]:
        """Check Redis cache connectivity"""
        
        try:
            start_time = time.time()
            
            # Test basic operations
            test_key = f"health_check:{int(time.time())}"
            await redis.setex(test_key, 60, "health_check_value")
            result = await redis.get(test_key)
            await redis.delete(test_key)
            
            response_time = time.time() - start_time
            healthy = result == b"health_check_value"
            
            # Get Redis info
            redis_info = await redis.info()
            
            return {
                'healthy': healthy,
                'details': {
                    'response_time': response_time,
                    'connected_clients': redis_info.get('connected_clients', 0),
                    'used_memory': redis_info.get('used_memory_human', 'unknown'),
                    'keyspace_hits': redis_info.get('keyspace_hits', 0),
                    'keyspace_misses': redis_info.get('keyspace_misses', 0)
                }
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }

health_monitor = HealthCheckMonitor()
```

### Synthetic Transaction Monitoring
```python
class SyntheticMonitoring:
    def __init__(self):
        self.statsd = statsd
        self.test_user_credentials = {
            'email': 'synthetic.test@paypal-clone.com',
            'password': 'SyntheticTest123!'
        }
    
    async def run_synthetic_transaction(self):
        """Run end-to-end synthetic transaction test"""
        
        transaction_start = time.time()
        success = False
        error_message = None
        
        try:
            # Step 1: User login
            login_start = time.time()
            auth_token = await self.synthetic_login()
            login_time = (time.time() - login_start) * 1000
            
            self.statsd.histogram('synthetic.login.response_time', login_time)
            
            # Step 2: Get user balance
            balance_start = time.time()
            balance = await self.synthetic_get_balance(auth_token)
            balance_time = (time.time() - balance_start) * 1000
            
            self.statsd.histogram('synthetic.balance.response_time', balance_time)
            
            # Step 3: Send small test payment
            payment_start = time.time()
            payment_result = await self.synthetic_send_payment(auth_token, 1.00)
            payment_time = (time.time() - payment_start) * 1000
            
            self.statsd.histogram('synthetic.payment.response_time', payment_time)
            
            # Step 4: Verify transaction
            verify_start = time.time()
            transaction_status = await self.synthetic_verify_transaction(
                auth_token, payment_result['transaction_id']
            )
            verify_time = (time.time() - verify_start) * 1000
            
            self.statsd.histogram('synthetic.verify.response_time', verify_time)
            
            success = transaction_status == 'completed'
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"Synthetic transaction failed: {e}")
        
        total_time = (time.time() - transaction_start) * 1000
        
        # Report results
        self.statsd.histogram('synthetic.transaction.total_time', total_time)
        self.statsd.increment(
            'synthetic.transaction.result',
            tags=[f'success:{success}']
        )
        
        if not success:
            self.statsd.increment('synthetic.transaction.failures')
        
        return {
            'success': success,
            'total_time': total_time,
            'error': error_message,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def synthetic_login(self) -> str:
        """Synthetic login test"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/v1/auth/login",
                json=self.test_user_credentials,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Login failed: {response.status_code}")
            
            return response.json()['access_token']
    
    async def synthetic_send_payment(self, auth_token: str, amount: float) -> dict:
        """Synthetic payment test"""
        
        headers = {'Authorization': f'Bearer {auth_token}'}
        payment_data = {
            'receiver_email': 'synthetic.receiver@paypal-clone.com',
            'amount': amount,
            'currency': 'USD',
            'description': 'Synthetic test payment',
            'payment_method_id': 'synthetic-payment-method-id'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/v1/payments/send",
                json=payment_data,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Payment failed: {response.status_code}")
            
            return response.json()

synthetic_monitor = SyntheticMonitoring()
```

## Monitoring Automation

### Automated Monitoring Tasks
```python
class MonitoringAutomation:
    def __init__(self):
        self.business_metrics = business_metrics
        self.technical_metrics = technical_metrics
        self.health_monitor = health_monitor
        self.synthetic_monitor = synthetic_monitor
        self.infrastructure_monitor = infrastructure_monitor
    
    async def run_monitoring_cycle(self):
        """Run complete monitoring cycle"""
        
        tasks = [
            self.collect_business_metrics(),
            self.collect_technical_metrics(),
            self.run_health_checks(),
            self.run_synthetic_tests(),
            self.collect_infrastructure_metrics()
        ]
        
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Monitoring cycle error: {e}")
    
    async def collect_business_metrics(self):
        """Collect business metrics from various sources"""
        
        # Update real-time dashboard
        await dashboard.update_real_time_counters()
        
        # Collect hourly business summaries
        await self.generate_business_summary()
    
    async def generate_business_summary(self):
        """Generate hourly business metrics summary"""
        
        current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        
        # Query database for hourly metrics
        async with db_manager.get_read_session() as session:
            # Transaction metrics
            transaction_summary = await session.execute(
                text("""
                    SELECT 
                        COUNT(*) as total_transactions,
                        SUM(amount) as total_volume,
                        AVG(amount) as avg_transaction_value,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful_transactions
                    FROM transactions 
                    WHERE created_at >= :start_time AND created_at < :end_time
                """),
                {
                    'start_time': current_hour,
                    'end_time': current_hour + timedelta(hours=1)
                }
            )
            
            summary = transaction_summary.fetchone()
            
            if summary:
                self.business_metrics.statsd.gauge(
                    'business.hourly.transaction_count', 
                    summary.total_transactions or 0
                )
                self.business_metrics.statsd.gauge(
                    'business.hourly.transaction_volume', 
                    float(summary.total_volume or 0)
                )
                self.business_metrics.statsd.gauge(
                    'business.hourly.avg_transaction_value', 
                    float(summary.avg_transaction_value or 0)
                )
                
                # Success rate
                success_rate = 0
                if summary.total_transactions > 0:
                    success_rate = (summary.successful_transactions / summary.total_transactions) * 100
                
                self.business_metrics.statsd.gauge(
                    'business.hourly.success_rate', 
                    success_rate
                )

monitoring_automation = MonitoringAutomation()

# Schedule monitoring tasks
async def start_monitoring():
    """Start automated monitoring tasks"""
    
    # Run monitoring cycle every minute
    while True:
        try:
            await monitoring_automation.run_monitoring_cycle()
            await asyncio.sleep(60)  # 1 minute interval
        except Exception as e:
            logger.error(f"Monitoring automation error: {e}")
            await asyncio.sleep(60)
```