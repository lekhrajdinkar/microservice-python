# Metrics Strategy

## Overview
Comprehensive metrics strategy using DataDog for collecting, analyzing, and alerting on business, technical, and infrastructure metrics in the PayPal clone system.

## Metrics Architecture

```
┌─────────────────┐    StatsD/HTTP   ┌─────────────────┐
│   Application   │─────────────────►│   DataDog       │
│   Services      │                  │   Agent         │
└─────────────────┘                  └─────────────────┘
         │                                     │
         │ Custom                              │ Processed
         │ Metrics                             │ Metrics
         ▼                                     ▼
┌─────────────────┐                  ┌─────────────────┐
│   StatsD        │                  │   DataDog       │
│   Client        │                  │   Platform      │
└─────────────────┘                  └─────────────────┘
         │                                     │
         │ Aggregated                          │ Dashboards
         │ Data                                │ & Alerts
         ▼                                     ▼
┌─────────────────┐                  ┌─────────────────┐
│   Local         │                  │   Analytics     │
│   Aggregation   │                  │   & Insights    │
└─────────────────┘                  └─────────────────┘
```

## Metrics Types and Implementation

### Business Metrics
```python
from datadog import statsd
import time
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime, timedelta
import asyncio

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"
    SET = "set"

class BusinessMetrics:
    def __init__(self):
        self.statsd = statsd
        self.default_tags = [
            f'env:{os.getenv("DD_ENV", "production")}',
            f'service:paypal-clone',
            f'version:{os.getenv("DD_VERSION", "1.0.0")}'
        ]
    
    # Payment Metrics
    async def track_payment_attempt(self, payment_data: Dict[str, Any]):
        """Track payment attempt metrics"""
        
        tags = [
            f'currency:{payment_data["currency"]}',
            f'payment_method:{payment_data["payment_method_type"]}',
            f'amount_range:{self._categorize_amount(payment_data["amount"])}',
            f'sender_country:{payment_data.get("sender_country", "unknown")}',
            f'receiver_country:{payment_data.get("receiver_country", "unknown")}'
        ]
        
        # Increment payment attempts counter
        self.statsd.increment('business.payment.attempts', tags=tags)
        
        # Track payment amount distribution
        self.statsd.histogram('business.payment.amount', payment_data['amount'], tags=tags)
        
        # Track unique users making payments
        self.statsd.set('business.payment.unique_senders', payment_data['sender_id'], tags=tags)
    
    async def track_payment_completion(self, payment_result: Dict[str, Any]):
        """Track payment completion metrics"""
        
        tags = [
            f'status:{payment_result["status"]}',
            f'currency:{payment_result["currency"]}',
            f'payment_method:{payment_result.get("payment_method_type", "unknown")}',
            f'processing_time_bucket:{self._categorize_processing_time(payment_result.get("processing_time_ms", 0))}'
        ]
        
        # Increment completion counter
        self.statsd.increment('business.payment.completions', tags=tags)
        
        # Track processing time
        if 'processing_time_ms' in payment_result:
            self.statsd.histogram('business.payment.processing_time', 
                                payment_result['processing_time_ms'], tags=tags)
        
        # Track success rate
        success = payment_result['status'] == 'completed'
        self.statsd.increment('business.payment.success_rate', 
                            tags=tags + [f'success:{success}'])
        
        # Track revenue (only for successful payments)
        if success:
            self.statsd.histogram('business.revenue.transaction_value', 
                                payment_result['amount'], tags=tags)
            
            # Track fees
            if 'fees' in payment_result:
                self.statsd.histogram('business.revenue.fees', 
                                    payment_result['fees'], tags=tags)
    
    # User Metrics
    async def track_user_registration(self, user_data: Dict[str, Any]):
        """Track user registration metrics"""
        
        tags = [
            f'registration_method:{user_data.get("method", "email")}',
            f'country:{user_data.get("country", "unknown")}',
            f'referrer:{user_data.get("referrer", "direct")}'
        ]
        
        # Increment registration counter
        self.statsd.increment('business.user.registrations', tags=tags)
        
        # Track registration funnel
        self.statsd.increment('business.user.funnel.registration_started', tags=tags)
    
    async def track_user_verification(self, verification_data: Dict[str, Any]):
        """Track user verification metrics"""
        
        tags = [
            f'verification_type:{verification_data["type"]}',
            f'status:{verification_data["status"]}',
            f'method:{verification_data.get("method", "unknown")}'
        ]
        
        # Increment verification attempts
        self.statsd.increment('business.user.verification_attempts', tags=tags)
        
        # Track verification success rate
        success = verification_data['status'] == 'verified'
        self.statsd.increment('business.user.verification_success_rate', 
                            tags=tags + [f'success:{success}'])
        
        # Track verification time
        if 'processing_time_ms' in verification_data:
            self.statsd.histogram('business.user.verification_time', 
                                verification_data['processing_time_ms'], tags=tags)
    
    async def track_user_activity(self, activity_data: Dict[str, Any]):
        """Track user activity metrics"""
        
        tags = [
            f'activity_type:{activity_data["type"]}',
            f'user_tier:{activity_data.get("user_tier", "standard")}',
            f'device_type:{activity_data.get("device_type", "unknown")}'
        ]
        
        # Track daily active users
        self.statsd.set('business.user.daily_active', activity_data['user_id'], 
                       tags=tags + ['period:daily'])
        
        # Track monthly active users
        self.statsd.set('business.user.monthly_active', activity_data['user_id'], 
                       tags=tags + ['period:monthly'])
        
        # Track session duration
        if 'session_duration_ms' in activity_data:
            self.statsd.histogram('business.user.session_duration', 
                                activity_data['session_duration_ms'], tags=tags)
    
    # Fraud Metrics
    async def track_fraud_detection(self, fraud_data: Dict[str, Any]):
        """Track fraud detection metrics"""
        
        tags = [
            f'action:{fraud_data["action"]}',
            f'risk_level:{self._categorize_risk_score(fraud_data["risk_score"])}',
            f'model_version:{fraud_data.get("model_version", "unknown")}'
        ]
        
        # Track fraud detection events
        self.statsd.increment('business.fraud.detections', tags=tags)
        
        # Track risk score distribution
        self.statsd.histogram('business.fraud.risk_score', fraud_data['risk_score'], tags=tags)
        
        # Track detection time
        if 'detection_time_ms' in fraud_data:
            self.statsd.histogram('business.fraud.detection_time', 
                                fraud_data['detection_time_ms'], tags=tags)
        
        # Track blocked transactions
        if fraud_data['action'] == 'block':
            self.statsd.increment('business.fraud.blocked_transactions', tags=tags)
            
            # Track potential loss prevented
            if 'transaction_amount' in fraud_data:
                self.statsd.histogram('business.fraud.loss_prevented', 
                                    fraud_data['transaction_amount'], tags=tags)
    
    # Helper methods
    def _categorize_amount(self, amount: float) -> str:
        """Categorize payment amount into ranges"""
        if amount < 10:
            return 'micro'
        elif amount < 100:
            return 'small'
        elif amount < 1000:
            return 'medium'
        elif amount < 10000:
            return 'large'
        else:
            return 'enterprise'
    
    def _categorize_processing_time(self, time_ms: float) -> str:
        """Categorize processing time into buckets"""
        if time_ms < 100:
            return 'fast'
        elif time_ms < 500:
            return 'normal'
        elif time_ms < 2000:
            return 'slow'
        else:
            return 'very_slow'
    
    def _categorize_risk_score(self, score: float) -> str:
        """Categorize risk score into levels"""
        if score < 30:
            return 'low'
        elif score < 70:
            return 'medium'
        else:
            return 'high'

business_metrics = BusinessMetrics()
```

### Technical Metrics
```python
class TechnicalMetrics:
    def __init__(self):
        self.statsd = statsd
        self.default_tags = [
            f'env:{os.getenv("DD_ENV", "production")}',
            f'service:paypal-clone',
            f'version:{os.getenv("DD_VERSION", "1.0.0")}'
        ]
    
    # API Metrics
    async def track_api_request(self, request_data: Dict[str, Any]):
        """Track API request metrics"""
        
        tags = [
            f'method:{request_data["method"]}',
            f'endpoint:{request_data["endpoint"]}',
            f'status_code:{request_data["status_code"]}',
            f'user_tier:{request_data.get("user_tier", "unknown")}'
        ]
        
        # Request count
        self.statsd.increment('api.requests.count', tags=tags)
        
        # Response time
        self.statsd.histogram('api.requests.response_time', 
                            request_data['response_time_ms'], tags=tags)
        
        # Request/Response size
        if 'request_size_bytes' in request_data:
            self.statsd.histogram('api.requests.size', 
                                request_data['request_size_bytes'], tags=tags)
        
        if 'response_size_bytes' in request_data:
            self.statsd.histogram('api.responses.size', 
                                request_data['response_size_bytes'], tags=tags)
        
        # Error rate
        is_error = request_data['status_code'] >= 400
        self.statsd.increment('api.requests.error_rate', 
                            tags=tags + [f'error:{is_error}'])
        
        # Rate limiting
        if 'rate_limit_remaining' in request_data:
            self.statsd.gauge('api.rate_limit.remaining', 
                            request_data['rate_limit_remaining'], tags=tags)
    
    # Database Metrics
    async def track_database_operation(self, db_data: Dict[str, Any]):
        """Track database operation metrics"""
        
        tags = [
            f'operation:{db_data["operation"]}',
            f'table:{db_data.get("table", "unknown")}',
            f'database:{db_data.get("database", "primary")}'
        ]
        
        # Query count
        self.statsd.increment('database.queries.count', tags=tags)
        
        # Query execution time
        self.statsd.histogram('database.queries.execution_time', 
                            db_data['execution_time_ms'], tags=tags)
        
        # Rows affected
        if 'rows_affected' in db_data:
            self.statsd.histogram('database.queries.rows_affected', 
                                db_data['rows_affected'], tags=tags)
        
        # Connection pool metrics
        if 'connection_pool' in db_data:
            pool_data = db_data['connection_pool']
            self.statsd.gauge('database.pool.active_connections', 
                            pool_data.get('active', 0), tags=tags)
            self.statsd.gauge('database.pool.idle_connections', 
                            pool_data.get('idle', 0), tags=tags)
            self.statsd.gauge('database.pool.total_connections', 
                            pool_data.get('total', 0), tags=tags)
        
        # Query errors
        if db_data.get('error'):
            self.statsd.increment('database.queries.errors', 
                                tags=tags + [f'error_type:{type(db_data["error"]).__name__}'])
    
    # Cache Metrics
    async def track_cache_operation(self, cache_data: Dict[str, Any]):
        """Track cache operation metrics"""
        
        tags = [
            f'operation:{cache_data["operation"]}',
            f'cache_type:{cache_data.get("cache_type", "redis")}',
            f'key_pattern:{cache_data.get("key_pattern", "unknown")}'
        ]
        
        # Cache operations count
        self.statsd.increment('cache.operations.count', tags=tags)
        
        # Cache hit/miss
        if cache_data['operation'] == 'get':
            hit = cache_data.get('hit', False)
            self.statsd.increment('cache.operations.hit_miss', 
                                tags=tags + [f'result:{"hit" if hit else "miss"}'])
        
        # Response time
        if 'response_time_ms' in cache_data:
            self.statsd.histogram('cache.operations.response_time', 
                                cache_data['response_time_ms'], tags=tags)
        
        # Cache size metrics
        if 'cache_size' in cache_data:
            self.statsd.gauge('cache.size.current', cache_data['cache_size'], tags=tags)
        
        # TTL metrics
        if 'ttl_seconds' in cache_data:
            self.statsd.histogram('cache.ttl.distribution', 
                                cache_data['ttl_seconds'], tags=tags)
    
    # Message Queue Metrics
    async def track_message_queue_operation(self, queue_data: Dict[str, Any]):
        """Track message queue operation metrics"""
        
        tags = [
            f'queue_name:{queue_data["queue_name"]}',
            f'operation:{queue_data["operation"]}',
            f'message_type:{queue_data.get("message_type", "unknown")}'
        ]
        
        # Message operations count
        self.statsd.increment('queue.operations.count', tags=tags)
        
        # Processing time
        if 'processing_time_ms' in queue_data:
            self.statsd.histogram('queue.operations.processing_time', 
                                queue_data['processing_time_ms'], tags=tags)
        
        # Queue depth
        if 'queue_depth' in queue_data:
            self.statsd.gauge('queue.depth.current', queue_data['queue_depth'], tags=tags)
        
        # Message size
        if 'message_size_bytes' in queue_data:
            self.statsd.histogram('queue.message.size', 
                                queue_data['message_size_bytes'], tags=tags)
        
        # Retry metrics
        if 'retry_count' in queue_data:
            self.statsd.histogram('queue.message.retry_count', 
                                queue_data['retry_count'], tags=tags)
        
        # Dead letter queue
        if queue_data.get('sent_to_dlq'):
            self.statsd.increment('queue.dlq.messages', tags=tags)
    
    # External Service Metrics
    async def track_external_service_call(self, service_data: Dict[str, Any]):
        """Track external service call metrics"""
        
        tags = [
            f'service_name:{service_data["service_name"]}',
            f'endpoint:{service_data.get("endpoint", "unknown")}',
            f'method:{service_data.get("method", "unknown")}'
        ]
        
        # Service call count
        self.statsd.increment('external_service.calls.count', tags=tags)
        
        # Response time
        if 'response_time_ms' in service_data:
            self.statsd.histogram('external_service.calls.response_time', 
                                service_data['response_time_ms'], tags=tags)
        
        # Success/Error rate
        success = not service_data.get('error')
        self.statsd.increment('external_service.calls.success_rate', 
                            tags=tags + [f'success:{success}'])
        
        # Circuit breaker state
        if 'circuit_breaker_state' in service_data:
            self.statsd.gauge('external_service.circuit_breaker.state', 
                            1 if service_data['circuit_breaker_state'] == 'open' else 0, 
                            tags=tags)
        
        # Retry metrics
        if 'retry_count' in service_data:
            self.statsd.histogram('external_service.calls.retry_count', 
                                service_data['retry_count'], tags=tags)

technical_metrics = TechnicalMetrics()
```

### Infrastructure Metrics
```python
class InfrastructureMetrics:
    def __init__(self):
        self.statsd = statsd
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        self.default_tags = [
            f'env:{os.getenv("DD_ENV", "production")}',
            f'cluster:{os.getenv("CLUSTER_NAME", "paypal-clone")}'
        ]
    
    async def collect_kubernetes_metrics(self):
        """Collect Kubernetes cluster metrics"""
        
        # Mock Kubernetes metrics collection
        k8s_metrics = await self._get_kubernetes_metrics()
        
        # Pod metrics
        self.statsd.gauge('k8s.pods.running', k8s_metrics['pods']['running'])
        self.statsd.gauge('k8s.pods.pending', k8s_metrics['pods']['pending'])
        self.statsd.gauge('k8s.pods.failed', k8s_metrics['pods']['failed'])
        
        # Node metrics
        self.statsd.gauge('k8s.nodes.ready', k8s_metrics['nodes']['ready'])
        self.statsd.gauge('k8s.nodes.not_ready', k8s_metrics['nodes']['not_ready'])
        
        # Resource utilization
        for node, metrics in k8s_metrics['node_metrics'].items():
            node_tags = self.default_tags + [f'node:{node}']
            self.statsd.gauge('k8s.node.cpu.utilization', 
                            metrics['cpu_utilization'], tags=node_tags)
            self.statsd.gauge('k8s.node.memory.utilization', 
                            metrics['memory_utilization'], tags=node_tags)
            self.statsd.gauge('k8s.node.disk.utilization', 
                            metrics['disk_utilization'], tags=node_tags)
        
        # HPA metrics
        for hpa in k8s_metrics['hpa']:
            hpa_tags = self.default_tags + [f'deployment:{hpa["name"]}']
            self.statsd.gauge('k8s.hpa.current_replicas', 
                            hpa['current_replicas'], tags=hpa_tags)
            self.statsd.gauge('k8s.hpa.desired_replicas', 
                            hpa['desired_replicas'], tags=hpa_tags)
            self.statsd.gauge('k8s.hpa.target_cpu_utilization', 
                            hpa['target_cpu'], tags=hpa_tags)
    
    async def collect_aws_metrics(self):
        """Collect AWS service metrics"""
        
        # RDS metrics
        await self._collect_rds_metrics()
        
        # ElastiCache metrics
        await self._collect_elasticache_metrics()
        
        # SQS metrics
        await self._collect_sqs_metrics()
        
        # EKS metrics
        await self._collect_eks_metrics()
    
    async def _collect_rds_metrics(self):
        """Collect RDS performance metrics"""
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)
        
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
            cpu_utilization = cpu_response['Datapoints'][-1]['Average']
            self.statsd.gauge('aws.rds.cpu.utilization', cpu_utilization, 
                            tags=self.default_tags + ['instance:primary'])
        
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
            connections = conn_response['Datapoints'][-1]['Average']
            self.statsd.gauge('aws.rds.connections.count', connections, 
                            tags=self.default_tags + ['instance:primary'])
    
    async def _collect_elasticache_metrics(self):
        """Collect ElastiCache Redis metrics"""
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)
        
        # CPU Utilization
        cpu_response = await self.cloudwatch.get_metric_statistics(
            Namespace='AWS/ElastiCache',
            MetricName='CPUUtilization',
            Dimensions=[
                {'Name': 'CacheClusterId', 'Value': 'paypal-clone-redis'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average']
        )
        
        if cpu_response['Datapoints']:
            cpu_utilization = cpu_response['Datapoints'][-1]['Average']
            self.statsd.gauge('aws.elasticache.cpu.utilization', cpu_utilization, 
                            tags=self.default_tags + ['cluster:redis'])
        
        # Memory Utilization
        memory_response = await self.cloudwatch.get_metric_statistics(
            Namespace='AWS/ElastiCache',
            MetricName='DatabaseMemoryUsagePercentage',
            Dimensions=[
                {'Name': 'CacheClusterId', 'Value': 'paypal-clone-redis'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average']
        )
        
        if memory_response['Datapoints']:
            memory_utilization = memory_response['Datapoints'][-1]['Average']
            self.statsd.gauge('aws.elasticache.memory.utilization', memory_utilization, 
                            tags=self.default_tags + ['cluster:redis'])
    
    async def _get_kubernetes_metrics(self) -> Dict[str, Any]:
        """Mock Kubernetes metrics collection"""
        
        # In real implementation, this would use Kubernetes API
        return {
            'pods': {'running': 25, 'pending': 2, 'failed': 1},
            'nodes': {'ready': 3, 'not_ready': 0},
            'node_metrics': {
                'node-1': {'cpu_utilization': 65, 'memory_utilization': 70, 'disk_utilization': 45},
                'node-2': {'cpu_utilization': 72, 'memory_utilization': 68, 'disk_utilization': 50},
                'node-3': {'cpu_utilization': 58, 'memory_utilization': 75, 'disk_utilization': 42}
            },
            'hpa': [
                {'name': 'payment-service', 'current_replicas': 5, 'desired_replicas': 5, 'target_cpu': 70},
                {'name': 'user-service', 'current_replicas': 3, 'desired_replicas': 4, 'target_cpu': 70}
            ]
        }

infrastructure_metrics = InfrastructureMetrics()
```

## Custom Metrics and Aggregations

### Business KPI Calculations
```python
class BusinessKPICalculator:
    def __init__(self):
        self.statsd = statsd
        self.redis = redis.Redis(
            host=REDIS_ENDPOINT,
            port=6379,
            password=REDIS_AUTH_TOKEN,
            ssl=True
        )
    
    async def calculate_real_time_kpis(self):
        """Calculate and publish real-time business KPIs"""
        
        current_time = datetime.utcnow()
        
        # Calculate transaction success rate (last hour)
        success_rate = await self._calculate_transaction_success_rate(current_time)
        self.statsd.gauge('kpi.transaction.success_rate', success_rate)
        
        # Calculate average transaction value (last hour)
        avg_transaction_value = await self._calculate_avg_transaction_value(current_time)
        self.statsd.gauge('kpi.transaction.avg_value', avg_transaction_value)
        
        # Calculate customer acquisition rate (last 24 hours)
        acquisition_rate = await self._calculate_customer_acquisition_rate(current_time)
        self.statsd.gauge('kpi.customer.acquisition_rate', acquisition_rate)
        
        # Calculate fraud detection effectiveness
        fraud_effectiveness = await self._calculate_fraud_effectiveness(current_time)
        self.statsd.gauge('kpi.fraud.effectiveness', fraud_effectiveness)
        
        # Calculate system availability (last hour)
        availability = await self._calculate_system_availability(current_time)
        self.statsd.gauge('kpi.system.availability', availability)
    
    async def _calculate_transaction_success_rate(self, current_time: datetime) -> float:
        """Calculate transaction success rate for the last hour"""
        
        hour_key = current_time.strftime('%Y%m%d%H')
        
        # Get counts from Redis
        total_transactions = await self.redis.get(f'txn_total:{hour_key}') or 0
        successful_transactions = await self.redis.get(f'txn_success:{hour_key}') or 0
        
        if int(total_transactions) == 0:
            return 100.0  # No transactions = 100% success rate
        
        success_rate = (int(successful_transactions) / int(total_transactions)) * 100
        return round(success_rate, 2)
    
    async def _calculate_avg_transaction_value(self, current_time: datetime) -> float:
        """Calculate average transaction value for the last hour"""
        
        hour_key = current_time.strftime('%Y%m%d%H')
        
        # Get values from Redis
        total_value = await self.redis.get(f'txn_value:{hour_key}') or 0
        total_count = await self.redis.get(f'txn_count:{hour_key}') or 0
        
        if int(total_count) == 0:
            return 0.0
        
        avg_value = float(total_value) / int(total_count)
        return round(avg_value, 2)
    
    async def _calculate_customer_acquisition_rate(self, current_time: datetime) -> float:
        """Calculate customer acquisition rate for the last 24 hours"""
        
        day_key = current_time.strftime('%Y%m%d')
        
        # Get new registrations from Redis
        new_registrations = await self.redis.get(f'new_users:{day_key}') or 0
        
        return float(new_registrations)
    
    async def _calculate_fraud_effectiveness(self, current_time: datetime) -> float:
        """Calculate fraud detection effectiveness"""
        
        hour_key = current_time.strftime('%Y%m%d%H')
        
        # Get fraud metrics from Redis
        blocked_fraudulent = await self.redis.get(f'fraud_blocked:{hour_key}') or 0
        total_fraudulent = await self.redis.get(f'fraud_total:{hour_key}') or 0
        
        if int(total_fraudulent) == 0:
            return 100.0  # No fraud = 100% effectiveness
        
        effectiveness = (int(blocked_fraudulent) / int(total_fraudulent)) * 100
        return round(effectiveness, 2)
    
    async def _calculate_system_availability(self, current_time: datetime) -> float:
        """Calculate system availability for the last hour"""
        
        hour_key = current_time.strftime('%Y%m%d%H')
        
        # Get uptime metrics from Redis
        total_checks = await self.redis.get(f'health_checks:{hour_key}') or 0
        successful_checks = await self.redis.get(f'health_success:{hour_key}') or 0
        
        if int(total_checks) == 0:
            return 100.0  # No checks = assume 100% availability
        
        availability = (int(successful_checks) / int(total_checks)) * 100
        return round(availability, 2)

kpi_calculator = BusinessKPICalculator()
```

### Metric Aggregation and Rollups
```python
class MetricAggregator:
    def __init__(self):
        self.statsd = statsd
        self.redis = redis.Redis(
            host=REDIS_ENDPOINT,
            port=6379,
            password=REDIS_AUTH_TOKEN,
            ssl=True
        )
    
    async def aggregate_hourly_metrics(self):
        """Aggregate metrics into hourly rollups"""
        
        current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        previous_hour = current_hour - timedelta(hours=1)
        
        # Aggregate payment metrics
        await self._aggregate_payment_metrics(previous_hour)
        
        # Aggregate user metrics
        await self._aggregate_user_metrics(previous_hour)
        
        # Aggregate system metrics
        await self._aggregate_system_metrics(previous_hour)
    
    async def _aggregate_payment_metrics(self, hour: datetime):
        """Aggregate payment metrics for the specified hour"""
        
        hour_key = hour.strftime('%Y%m%d%H')
        
        # Get raw metrics from Redis
        payment_data = {
            'total_payments': await self.redis.get(f'payments_total:{hour_key}') or 0,
            'successful_payments': await self.redis.get(f'payments_success:{hour_key}') or 0,
            'failed_payments': await self.redis.get(f'payments_failed:{hour_key}') or 0,
            'total_volume': await self.redis.get(f'payments_volume:{hour_key}') or 0,
            'total_fees': await self.redis.get(f'payments_fees:{hour_key}') or 0
        }
        
        # Calculate aggregated metrics
        success_rate = 0
        if int(payment_data['total_payments']) > 0:
            success_rate = (int(payment_data['successful_payments']) / 
                          int(payment_data['total_payments'])) * 100
        
        avg_transaction_value = 0
        if int(payment_data['successful_payments']) > 0:
            avg_transaction_value = (float(payment_data['total_volume']) / 
                                   int(payment_data['successful_payments']))
        
        # Send aggregated metrics to DataDog
        tags = [f'hour:{hour.isoformat()}', 'aggregation:hourly']
        
        self.statsd.gauge('aggregated.payments.total', 
                         int(payment_data['total_payments']), tags=tags)
        self.statsd.gauge('aggregated.payments.success_rate', success_rate, tags=tags)
        self.statsd.gauge('aggregated.payments.avg_value', avg_transaction_value, tags=tags)
        self.statsd.gauge('aggregated.payments.total_volume', 
                         float(payment_data['total_volume']), tags=tags)
        self.statsd.gauge('aggregated.payments.total_fees', 
                         float(payment_data['total_fees']), tags=tags)
    
    async def aggregate_daily_metrics(self):
        """Aggregate metrics into daily rollups"""
        
        current_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        previous_day = current_day - timedelta(days=1)
        
        # Aggregate 24 hours of hourly data
        daily_aggregates = {
            'total_payments': 0,
            'total_volume': 0,
            'total_users': 0,
            'total_revenue': 0
        }
        
        # Sum up hourly data for the day
        for hour in range(24):
            hour_time = previous_day + timedelta(hours=hour)
            hour_key = hour_time.strftime('%Y%m%d%H')
            
            daily_aggregates['total_payments'] += int(
                await self.redis.get(f'payments_total:{hour_key}') or 0
            )
            daily_aggregates['total_volume'] += float(
                await self.redis.get(f'payments_volume:{hour_key}') or 0
            )
            daily_aggregates['total_revenue'] += float(
                await self.redis.get(f'payments_fees:{hour_key}') or 0
            )
        
        # Get unique users for the day
        daily_aggregates['total_users'] = await self.redis.scard(
            f'daily_active_users:{previous_day.strftime("%Y%m%d")}'
        )
        
        # Send daily aggregates to DataDog
        tags = [f'date:{previous_day.strftime("%Y-%m-%d")}', 'aggregation:daily']
        
        for metric, value in daily_aggregates.items():
            self.statsd.gauge(f'aggregated.daily.{metric}', value, tags=tags)

metric_aggregator = MetricAggregator()
```

## Alerting on Metrics

### Metric-based Alert Rules
```python
class MetricAlertRules:
    def __init__(self):
        self.alert_rules = {
            # Business Alerts
            'payment_success_rate_low': {
                'metric': 'business.payment.success_rate',
                'aggregation': 'avg',
                'threshold': 95,  # Below 95%
                'comparison': '<',
                'window': '10m',
                'severity': 'critical'
            },
            'transaction_volume_spike': {
                'metric': 'business.payment.amount',
                'aggregation': 'sum',
                'threshold': 1000000,  # Above $1M per hour
                'comparison': '>',
                'window': '1h',
                'severity': 'warning'
            },
            'fraud_detection_rate_high': {
                'metric': 'business.fraud.detections',
                'aggregation': 'sum',
                'threshold': 100,  # More than 100 detections per hour
                'comparison': '>',
                'window': '1h',
                'severity': 'warning'
            },
            
            # Technical Alerts
            'api_response_time_high': {
                'metric': 'api.requests.response_time',
                'aggregation': 'p95',
                'threshold': 2000,  # Above 2 seconds
                'comparison': '>',
                'window': '5m',
                'severity': 'warning'
            },
            'database_query_time_high': {
                'metric': 'database.queries.execution_time',
                'aggregation': 'p95',
                'threshold': 1000,  # Above 1 second
                'comparison': '>',
                'window': '5m',
                'severity': 'critical'
            },
            'cache_hit_rate_low': {
                'metric': 'cache.operations.hit_miss',
                'aggregation': 'avg',
                'threshold': 80,  # Below 80%
                'comparison': '<',
                'window': '10m',
                'severity': 'warning'
            },
            
            # Infrastructure Alerts
            'kubernetes_pods_failing': {
                'metric': 'k8s.pods.failed',
                'aggregation': 'max',
                'threshold': 5,  # More than 5 failed pods
                'comparison': '>',
                'window': '5m',
                'severity': 'critical'
            },
            'aws_rds_cpu_high': {
                'metric': 'aws.rds.cpu.utilization',
                'aggregation': 'avg',
                'threshold': 80,  # Above 80%
                'comparison': '>',
                'window': '10m',
                'severity': 'warning'
            }
        }
    
    def generate_datadog_monitor_configs(self) -> List[Dict[str, Any]]:
        """Generate DataDog monitor configurations for all alert rules"""
        
        monitors = []
        
        for alert_name, rule in self.alert_rules.items():
            monitor_config = {
                'name': f'Metric Alert: {alert_name.replace("_", " ").title()}',
                'query': self._build_query(rule),
                'message': self._build_alert_message(alert_name, rule),
                'type': 'metric alert',
                'options': {
                    'thresholds': {
                        'critical': rule['threshold']
                    },
                    'notify_audit': rule['severity'] == 'critical',
                    'require_full_window': True,
                    'notify_no_data': False,
                    'evaluation_delay': 60
                },
                'tags': [
                    f'severity:{rule["severity"]}',
                    f'category:{"business" if "business." in rule["metric"] else "technical"}',
                    'source:metrics'
                ]
            }
            
            monitors.append(monitor_config)
        
        return monitors
    
    def _build_query(self, rule: Dict[str, Any]) -> str:
        """Build DataDog query string for alert rule"""
        
        metric = rule['metric']
        aggregation = rule['aggregation']
        window = rule['window']
        threshold = rule['threshold']
        comparison = rule['comparison']
        
        query = f'{aggregation}(last_{window}):{metric}{{*}} {comparison} {threshold}'
        
        return query
    
    def _build_alert_message(self, alert_name: str, rule: Dict[str, Any]) -> str:
        """Build alert message for DataDog monitor"""
        
        severity_channel = '@pagerduty-critical' if rule['severity'] == 'critical' else '@slack-alerts'
        
        message = f'''
        {severity_channel}
        
        Alert: {alert_name.replace("_", " ").title()}
        
        Metric: {rule["metric"]}
        Threshold: {rule["comparison"]} {rule["threshold"]}
        Window: {rule["window"]}
        Current Value: {{{{value}}}}
        
        Please investigate immediately.
        
        Runbook: https://wiki.paypal-clone.com/runbooks/{alert_name}
        '''
        
        return message.strip()

metric_alert_rules = MetricAlertRules()
```

## Performance Optimization

### Metric Batching and Sampling
```python
class MetricOptimizer:
    def __init__(self):
        self.statsd = statsd
        self.metric_buffer = []
        self.buffer_size = 100
        self.flush_interval = 10  # seconds
        self.last_flush = time.time()
    
    async def optimized_metric_send(self, metric_type: str, metric_name: str, 
                                  value: float, tags: List[str] = None, 
                                  sample_rate: float = 1.0):
        """Send metrics with batching and sampling optimization"""
        
        # Apply sampling
        if sample_rate < 1.0 and random.random() > sample_rate:
            return
        
        # Add to buffer
        metric_data = {
            'type': metric_type,
            'name': metric_name,
            'value': value,
            'tags': tags or [],
            'timestamp': time.time()
        }
        
        self.metric_buffer.append(metric_data)
        
        # Flush if buffer is full or time interval exceeded
        if (len(self.metric_buffer) >= self.buffer_size or 
            time.time() - self.last_flush >= self.flush_interval):
            await self._flush_metrics()
    
    async def _flush_metrics(self):
        """Flush buffered metrics to DataDog"""
        
        if not self.metric_buffer:
            return
        
        try:
            # Group metrics by type for efficient sending
            grouped_metrics = {
                'counter': [],
                'gauge': [],
                'histogram': [],
                'timer': []
            }
            
            for metric in self.metric_buffer:
                metric_type = metric['type']
                if metric_type in grouped_metrics:
                    grouped_metrics[metric_type].append(metric)
            
            # Send grouped metrics
            for metric_type, metrics in grouped_metrics.items():
                if metrics:
                    await self._send_grouped_metrics(metric_type, metrics)
            
            # Clear buffer
            self.metric_buffer.clear()
            self.last_flush = time.time()
            
        except Exception as e:
            logger.error(f"Failed to flush metrics: {e}")
    
    async def _send_grouped_metrics(self, metric_type: str, metrics: List[Dict[str, Any]]):
        """Send grouped metrics of the same type"""
        
        for metric in metrics:
            try:
                if metric_type == 'counter':
                    self.statsd.increment(metric['name'], metric['value'], tags=metric['tags'])
                elif metric_type == 'gauge':
                    self.statsd.gauge(metric['name'], metric['value'], tags=metric['tags'])
                elif metric_type == 'histogram':
                    self.statsd.histogram(metric['name'], metric['value'], tags=metric['tags'])
                elif metric_type == 'timer':
                    self.statsd.timing(metric['name'], metric['value'], tags=metric['tags'])
                    
            except Exception as e:
                logger.error(f"Failed to send {metric_type} metric {metric['name']}: {e}")

metric_optimizer = MetricOptimizer()
```

## Metrics Automation

### Automated Metric Collection
```python
class MetricsAutomation:
    def __init__(self):
        self.business_metrics = business_metrics
        self.technical_metrics = technical_metrics
        self.infrastructure_metrics = infrastructure_metrics
        self.kpi_calculator = kpi_calculator
        self.metric_aggregator = metric_aggregator
    
    async def start_automated_collection(self):
        """Start automated metric collection tasks"""
        
        # Create background tasks for different metric types
        tasks = [
            asyncio.create_task(self._collect_business_metrics_loop()),
            asyncio.create_task(self._collect_technical_metrics_loop()),
            asyncio.create_task(self._collect_infrastructure_metrics_loop()),
            asyncio.create_task(self._calculate_kpis_loop()),
            asyncio.create_task(self._aggregate_metrics_loop())
        ]
        
        # Run all tasks concurrently
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _collect_business_metrics_loop(self):
        """Collect business metrics every minute"""
        
        while True:
            try:
                # This would typically be triggered by actual business events
                # For demonstration, we'll simulate some metrics
                await self._simulate_business_events()
                await asyncio.sleep(60)  # Every minute
                
            except Exception as e:
                logger.error(f"Business metrics collection error: {e}")
                await asyncio.sleep(60)
    
    async def _collect_infrastructure_metrics_loop(self):
        """Collect infrastructure metrics every 30 seconds"""
        
        while True:
            try:
                await self.infrastructure_metrics.collect_kubernetes_metrics()
                await self.infrastructure_metrics.collect_aws_metrics()
                await asyncio.sleep(30)  # Every 30 seconds
                
            except Exception as e:
                logger.error(f"Infrastructure metrics collection error: {e}")
                await asyncio.sleep(30)
    
    async def _calculate_kpis_loop(self):
        """Calculate KPIs every 5 minutes"""
        
        while True:
            try:
                await self.kpi_calculator.calculate_real_time_kpis()
                await asyncio.sleep(300)  # Every 5 minutes
                
            except Exception as e:
                logger.error(f"KPI calculation error: {e}")
                await asyncio.sleep(300)
    
    async def _aggregate_metrics_loop(self):
        """Aggregate metrics hourly"""
        
        while True:
            try:
                current_time = datetime.utcnow()
                
                # Run hourly aggregation at the top of each hour
                if current_time.minute == 0:
                    await self.metric_aggregator.aggregate_hourly_metrics()
                
                # Run daily aggregation at midnight
                if current_time.hour == 0 and current_time.minute == 0:
                    await self.metric_aggregator.aggregate_daily_metrics()
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Metric aggregation error: {e}")
                await asyncio.sleep(60)
    
    async def _simulate_business_events(self):
        """Simulate business events for demonstration"""
        
        # Simulate payment events
        for _ in range(random.randint(10, 50)):
            payment_data = {
                'transaction_id': str(uuid.uuid4()),
                'amount': random.uniform(10, 1000),
                'currency': random.choice(['USD', 'EUR', 'GBP']),
                'sender_id': str(uuid.uuid4()),
                'receiver_id': str(uuid.uuid4()),
                'payment_method_type': random.choice(['card', 'bank', 'wallet'])
            }
            
            await self.business_metrics.track_payment_attempt(payment_data)
            
            # Simulate completion
            if random.random() > 0.05:  # 95% success rate
                payment_result = {
                    **payment_data,
                    'status': 'completed',
                    'processing_time_ms': random.uniform(100, 2000),
                    'fees': payment_data['amount'] * 0.029  # 2.9% fee
                }
                await self.business_metrics.track_payment_completion(payment_result)

metrics_automation = MetricsAutomation()

# Start automated metrics collection
async def start_metrics_collection():
    """Start the automated metrics collection system"""
    
    logger.info("Starting automated metrics collection")
    await metrics_automation.start_automated_collection()
```