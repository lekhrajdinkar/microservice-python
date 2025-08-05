# DataDog Integration

## Overview
Comprehensive DataDog integration for the PayPal clone system, providing unified observability across logs, metrics, traces, and infrastructure monitoring.

## DataDog Agent Configuration

### Kubernetes Deployment
```yaml
# DataDog Agent DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: datadog-agent
  namespace: datadog
spec:
  selector:
    matchLabels:
      app: datadog-agent
  template:
    metadata:
      labels:
        app: datadog-agent
      name: datadog-agent
    spec:
      serviceAccountName: datadog-agent
      containers:
      - image: gcr.io/datadoghq/agent:7.48.0
        imagePullPolicy: Always
        name: datadog-agent
        ports:
        - containerPort: 8125
          name: dogstatsdport
          protocol: UDP
        - containerPort: 8126
          name: traceport
          protocol: TCP
        env:
        - name: DD_API_KEY
          valueFrom:
            secretKeyRef:
              name: datadog-secret
              key: api-key
        - name: DD_SITE
          value: "datadoghq.com"
        - name: DD_KUBERNETES_KUBELET_HOST
          valueFrom:
            fieldRef:
              fieldPath: status.hostIP
        - name: DD_CLUSTER_NAME
          value: "paypal-clone-cluster"
        - name: DD_COLLECT_KUBERNETES_EVENTS
          value: "true"
        - name: DD_LEADER_ELECTION
          value: "true"
        - name: DD_APM_ENABLED
          value: "true"
        - name: DD_APM_NON_LOCAL_TRAFFIC
          value: "true"
        - name: DD_LOGS_ENABLED
          value: "true"
        - name: DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL
          value: "true"
        - name: DD_PROCESS_AGENT_ENABLED
          value: "true"
        - name: DD_SYSTEM_PROBE_ENABLED
          value: "true"
        - name: DD_DOGSTATSD_NON_LOCAL_TRAFFIC
          value: "true"
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "256m"
        volumeMounts:
        - name: dockersocket
          mountPath: /var/run/docker.sock
        - name: procdir
          mountPath: /host/proc
          readOnly: true
        - name: cgroups
          mountPath: /host/sys/fs/cgroup
          readOnly: true
        - name: debugfs
          mountPath: /sys/kernel/debug
        - name: s6-run
          mountPath: /var/run/s6
        livenessProbe:
          exec:
            command:
            - ./probe.sh
          initialDelaySeconds: 15
          periodSeconds: 15
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3
        readinessProbe:
          exec:
            command:
            - ./probe.sh
          initialDelaySeconds: 15
          periodSeconds: 15
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3
      volumes:
      - hostPath:
          path: /var/run/docker.sock
        name: dockersocket
      - hostPath:
          path: /proc
        name: procdir
      - hostPath:
          path: /sys/fs/cgroup
        name: cgroups
      - hostPath:
          path: /sys/kernel/debug
        name: debugfs
      - emptyDir: {}
        name: s6-run
      tolerations:
      - operator: Exists
```

### Application Configuration
```python
# DataDog configuration for FastAPI applications
import os
from ddtrace import config, patch_all, tracer
from ddtrace.contrib.fastapi import get_version
import logging

# Configure DataDog tracing
config.fastapi['service_name'] = os.getenv('DD_SERVICE', 'paypal-clone-api')
config.fastapi['request_span_name'] = 'fastapi.request'
config.fastapi['distributed_tracing'] = True

# Configure database tracing
config.sqlalchemy['service_name'] = 'paypal-clone-db'
config.redis['service_name'] = 'paypal-clone-cache'
config.httpx['service_name'] = 'paypal-clone-http'

# Patch all supported libraries
patch_all()

# Configure tracer
tracer.configure(
    hostname=os.getenv('DD_AGENT_HOST', 'datadog-agent.datadog.svc.cluster.local'),
    port=int(os.getenv('DD_TRACE_AGENT_PORT', '8126')),
    https=False,
    priority_sampling=True,
    analytics_enabled=True
)

# Set global tags
tracer.set_tags({
    'env': os.getenv('DD_ENV', 'production'),
    'service': os.getenv('DD_SERVICE', 'paypal-clone-api'),
    'version': os.getenv('DD_VERSION', '1.0.0'),
    'cluster': os.getenv('DD_CLUSTER_NAME', 'paypal-clone-cluster')
})

class DataDogIntegration:
    def __init__(self):
        self.tracer = tracer
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        """Setup structured logging for DataDog"""
        
        import json_logging
        import sys
        
        # Enable JSON logging
        json_logging.init_fastapi(enable_json=True)
        json_logging.init_request_instrument(app)
        
        # Configure logger
        logger = logging.getLogger("paypal-clone")
        logger.setLevel(logging.INFO)
        
        # Add DataDog correlation
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s [%(name)s] [dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def trace_function(self, service_name: str = None, resource_name: str = None):
        """Decorator for tracing functions"""
        
        def decorator(func):
            @tracer.wrap(
                service=service_name or config.fastapi['service_name'],
                resource=resource_name or f"{func.__module__}.{func.__name__}"
            )
            async def wrapper(*args, **kwargs):
                span = tracer.current_span()
                if span:
                    span.set_tag('function.name', func.__name__)
                    span.set_tag('function.module', func.__module__)
                
                try:
                    result = await func(*args, **kwargs)
                    if span:
                        span.set_tag('function.result', 'success')
                    return result
                except Exception as e:
                    if span:
                        span.set_tag('function.result', 'error')
                        span.set_tag('error.message', str(e))
                        span.set_tag('error.type', type(e).__name__)
                    raise
            
            return wrapper
        return decorator

dd_integration = DataDogIntegration()
```

## Custom Metrics Integration

### Business Metrics
```python
from datadog import statsd
import time
from typing import Dict, Any, Optional

class DataDogMetrics:
    def __init__(self):
        self.statsd = statsd
        self.default_tags = [
            f'env:{os.getenv("DD_ENV", "production")}',
            f'service:{os.getenv("DD_SERVICE", "paypal-clone")}',
            f'version:{os.getenv("DD_VERSION", "1.0.0")}'
        ]
    
    def increment(self, metric_name: str, value: int = 1, tags: list = None):
        """Increment a counter metric"""
        
        all_tags = self.default_tags + (tags or [])
        self.statsd.increment(metric_name, value, tags=all_tags)
    
    def gauge(self, metric_name: str, value: float, tags: list = None):
        """Set a gauge metric"""
        
        all_tags = self.default_tags + (tags or [])
        self.statsd.gauge(metric_name, value, tags=all_tags)
    
    def histogram(self, metric_name: str, value: float, tags: list = None):
        """Record a histogram metric"""
        
        all_tags = self.default_tags + (tags or [])
        self.statsd.histogram(metric_name, value, tags=all_tags)
    
    def timing(self, metric_name: str, value: float, tags: list = None):
        """Record a timing metric"""
        
        all_tags = self.default_tags + (tags or [])
        self.statsd.timing(metric_name, value, tags=all_tags)
    
    def set_metric(self, metric_name: str, value: str, tags: list = None):
        """Record a set metric (unique values)"""
        
        all_tags = self.default_tags + (tags or [])
        self.statsd.set(metric_name, value, tags=all_tags)
    
    def timed(self, metric_name: str, tags: list = None):
        """Decorator for timing function execution"""
        
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    success = True
                    return result
                except Exception as e:
                    success = False
                    raise
                finally:
                    execution_time = (time.time() - start_time) * 1000
                    metric_tags = (tags or []) + [f'success:{success}']
                    self.timing(metric_name, execution_time, metric_tags)
            
            return wrapper
        return decorator

dd_metrics = DataDogMetrics()

# Usage examples
class PaymentMetrics:
    def __init__(self):
        self.metrics = dd_metrics
    
    async def track_payment_attempt(self, payment_data: Dict[str, Any]):
        """Track payment attempt metrics"""
        
        # Increment payment attempts
        self.metrics.increment(
            'payment.attempts',
            tags=[
                f'currency:{payment_data["currency"]}',
                f'amount_range:{self._get_amount_range(payment_data["amount"])}',
                f'payment_method:{payment_data["payment_method_type"]}'
            ]
        )
        
        # Track payment amount distribution
        self.metrics.histogram(
            'payment.amount',
            payment_data['amount'],
            tags=[f'currency:{payment_data["currency"]}']
        )
    
    async def track_payment_completion(self, payment_data: Dict[str, Any], 
                                     processing_time: float, success: bool):
        """Track payment completion metrics"""
        
        # Processing time
        self.metrics.timing(
            'payment.processing_time',
            processing_time,
            tags=[
                f'success:{success}',
                f'currency:{payment_data["currency"]}',
                f'payment_method:{payment_data["payment_method_type"]}'
            ]
        )
        
        # Success rate
        self.metrics.increment(
            'payment.completions',
            tags=[
                f'success:{success}',
                f'currency:{payment_data["currency"]}'
            ]
        )
        
        # Revenue tracking (only for successful payments)
        if success:
            self.metrics.histogram(
                'payment.revenue',
                payment_data['amount'],
                tags=[f'currency:{payment_data["currency"]}']
            )
    
    def _get_amount_range(self, amount: float) -> str:
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

payment_metrics = PaymentMetrics()
```

### Infrastructure Metrics
```python
class InfrastructureMetrics:
    def __init__(self):
        self.metrics = dd_metrics
    
    async def track_database_metrics(self, operation: str, execution_time: float, 
                                   success: bool, connection_pool_info: Dict[str, int]):
        """Track database performance metrics"""
        
        # Query execution time
        self.metrics.timing(
            'database.query.execution_time',
            execution_time,
            tags=[
                f'operation:{operation}',
                f'success:{success}'
            ]
        )
        
        # Connection pool metrics
        self.metrics.gauge('database.pool.active', connection_pool_info['active'])
        self.metrics.gauge('database.pool.idle', connection_pool_info['idle'])
        self.metrics.gauge('database.pool.total', connection_pool_info['total'])
        
        # Query success rate
        self.metrics.increment(
            'database.query.count',
            tags=[
                f'operation:{operation}',
                f'success:{success}'
            ]
        )
    
    async def track_cache_metrics(self, operation: str, hit: bool, response_time: float):
        """Track cache performance metrics"""
        
        # Cache hit/miss rate
        self.metrics.increment(
            'cache.operations',
            tags=[
                f'operation:{operation}',
                f'result:{"hit" if hit else "miss"}'
            ]
        )
        
        # Cache response time
        self.metrics.timing(
            'cache.response_time',
            response_time,
            tags=[f'operation:{operation}']
        )
        
        # Hit ratio calculation
        self.metrics.increment(
            'cache.hit_ratio',
            tags=[f'result:{"hit" if hit else "miss"}']
        )
    
    async def track_message_queue_metrics(self, queue_name: str, operation: str,
                                        processing_time: float, success: bool):
        """Track message queue metrics"""
        
        # Message processing time
        self.metrics.timing(
            'queue.message.processing_time',
            processing_time,
            tags=[
                f'queue:{queue_name}',
                f'operation:{operation}',
                f'success:{success}'
            ]
        )
        
        # Message throughput
        self.metrics.increment(
            'queue.message.processed',
            tags=[
                f'queue:{queue_name}',
                f'success:{success}'
            ]
        )

infrastructure_metrics = InfrastructureMetrics()
```

## APM (Application Performance Monitoring)

### Distributed Tracing
```python
from ddtrace import tracer
from ddtrace.ext import http, sql
import asyncio

class DistributedTracing:
    def __init__(self):
        self.tracer = tracer
    
    async def trace_payment_flow(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace complete payment flow with distributed tracing"""
        
        with self.tracer.trace('payment.flow', service='payment-service') as span:
            span.set_tag('payment.amount', payment_data['amount'])
            span.set_tag('payment.currency', payment_data['currency'])
            span.set_tag('payment.sender_id', payment_data['sender_id'])
            span.set_tag('payment.receiver_id', payment_data['receiver_id'])
            
            try:
                # Step 1: Validate payment
                validation_result = await self._trace_payment_validation(payment_data)
                span.set_tag('payment.validation.result', validation_result['valid'])
                
                if not validation_result['valid']:
                    span.set_tag('payment.result', 'validation_failed')
                    span.set_tag('error', True)
                    return {'success': False, 'error': 'Validation failed'}
                
                # Step 2: Fraud check
                fraud_result = await self._trace_fraud_check(payment_data)
                span.set_tag('payment.fraud.risk_score', fraud_result['risk_score'])
                span.set_tag('payment.fraud.action', fraud_result['action'])
                
                if fraud_result['action'] == 'block':
                    span.set_tag('payment.result', 'fraud_blocked')
                    span.set_tag('error', True)
                    return {'success': False, 'error': 'Payment blocked'}
                
                # Step 3: Process payment
                processing_result = await self._trace_payment_processing(payment_data)
                span.set_tag('payment.transaction_id', processing_result['transaction_id'])
                span.set_tag('payment.result', 'success')
                
                # Step 4: Send notifications
                await self._trace_notification_sending(processing_result)
                
                return processing_result
                
            except Exception as e:
                span.set_tag('error', True)
                span.set_tag('error.message', str(e))
                span.set_tag('error.type', type(e).__name__)
                span.set_tag('payment.result', 'error')
                raise
    
    async def _trace_payment_validation(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace payment validation step"""
        
        with self.tracer.trace('payment.validation', service='validation-service') as span:
            span.set_tag('validation.amount', payment_data['amount'])
            span.set_tag('validation.sender_id', payment_data['sender_id'])
            
            # Simulate validation logic
            await asyncio.sleep(0.1)  # Simulate processing time
            
            # Check balance
            balance_check = await self._trace_balance_check(payment_data['sender_id'])
            span.set_tag('validation.balance_sufficient', balance_check['sufficient'])
            
            # Check limits
            limits_check = await self._trace_limits_check(payment_data)
            span.set_tag('validation.within_limits', limits_check['within_limits'])
            
            valid = balance_check['sufficient'] and limits_check['within_limits']
            span.set_tag('validation.result', valid)
            
            return {'valid': valid}
    
    async def _trace_balance_check(self, user_id: str) -> Dict[str, Any]:
        """Trace balance check with database query"""
        
        with self.tracer.trace('database.balance_check', service='database') as span:
            span.set_tag(sql.QUERY, 'SELECT balance FROM wallets WHERE user_id = ?')
            span.set_tag('db.user_id', user_id)
            
            # Simulate database query
            await asyncio.sleep(0.05)
            
            # Mock balance check
            sufficient = True  # In real implementation, check actual balance
            span.set_tag('balance.sufficient', sufficient)
            
            return {'sufficient': sufficient}
    
    async def _trace_fraud_check(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace fraud detection check"""
        
        with self.tracer.trace('fraud.check', service='fraud-service') as span:
            span.set_tag('fraud.amount', payment_data['amount'])
            span.set_tag('fraud.sender_id', payment_data['sender_id'])
            
            # Simulate fraud check
            await asyncio.sleep(0.2)
            
            # Mock fraud score
            risk_score = 25  # Low risk
            action = 'allow' if risk_score < 80 else 'block'
            
            span.set_tag('fraud.risk_score', risk_score)
            span.set_tag('fraud.action', action)
            
            return {'risk_score': risk_score, 'action': action}
    
    async def _trace_payment_processing(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace actual payment processing"""
        
        with self.tracer.trace('payment.processing', service='payment-service') as span:
            transaction_id = f"txn_{int(time.time())}"
            span.set_tag('payment.transaction_id', transaction_id)
            
            # Simulate payment processing
            await asyncio.sleep(0.3)
            
            # Update balances
            await self._trace_balance_update(payment_data, transaction_id)
            
            span.set_tag('payment.status', 'completed')
            
            return {
                'success': True,
                'transaction_id': transaction_id,
                'status': 'completed'
            }
    
    async def _trace_balance_update(self, payment_data: Dict[str, Any], transaction_id: str):
        """Trace balance update operations"""
        
        with self.tracer.trace('database.balance_update', service='database') as span:
            span.set_tag(sql.QUERY, 'UPDATE wallets SET balance = balance - ? WHERE user_id = ?')
            span.set_tag('db.transaction_id', transaction_id)
            span.set_tag('db.amount', payment_data['amount'])
            
            # Simulate database update
            await asyncio.sleep(0.1)
            
            span.set_tag('db.rows_affected', 2)  # Sender and receiver
    
    async def _trace_notification_sending(self, processing_result: Dict[str, Any]):
        """Trace notification sending"""
        
        with self.tracer.trace('notification.send', service='notification-service') as span:
            span.set_tag('notification.transaction_id', processing_result['transaction_id'])
            span.set_tag('notification.type', 'payment_completed')
            
            # Simulate notification sending
            await asyncio.sleep(0.1)
            
            span.set_tag('notification.status', 'sent')

distributed_tracing = DistributedTracing()
```

## Log Management

### Structured Logging
```python
import structlog
import json
from ddtrace import tracer

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

class DataDogLogger:
    def __init__(self):
        self.logger = structlog.get_logger()
    
    def _add_trace_context(self, event_dict: dict) -> dict:
        """Add DataDog trace context to log events"""
        
        span = tracer.current_span()
        if span:
            event_dict.update({
                'dd.trace_id': str(span.trace_id),
                'dd.span_id': str(span.span_id),
                'dd.service': span.service,
                'dd.env': os.getenv('DD_ENV', 'production'),
                'dd.version': os.getenv('DD_VERSION', '1.0.0')
            })
        
        return event_dict
    
    def info(self, message: str, **kwargs):
        """Log info message with trace context"""
        
        log_data = self._add_trace_context(kwargs)
        self.logger.info(message, **log_data)
    
    def error(self, message: str, error: Exception = None, **kwargs):
        """Log error message with trace context"""
        
        log_data = self._add_trace_context(kwargs)
        if error:
            log_data.update({
                'error.message': str(error),
                'error.type': type(error).__name__,
                'error.stack': traceback.format_exc()
            })
        
        self.logger.error(message, **log_data)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with trace context"""
        
        log_data = self._add_trace_context(kwargs)
        self.logger.warning(message, **log_data)
    
    def debug(self, message: str, **kwargs):
        """Log debug message with trace context"""
        
        log_data = self._add_trace_context(kwargs)
        self.logger.debug(message, **log_data)

dd_logger = DataDogLogger()

# Usage in payment processing
async def process_payment_with_logging(payment_data: Dict[str, Any]):
    """Process payment with comprehensive logging"""
    
    transaction_id = str(uuid.uuid4())
    
    dd_logger.info(
        "Payment processing started",
        transaction_id=transaction_id,
        sender_id=payment_data['sender_id'],
        receiver_id=payment_data['receiver_id'],
        amount=payment_data['amount'],
        currency=payment_data['currency']
    )
    
    try:
        # Process payment
        result = await distributed_tracing.trace_payment_flow(payment_data)
        
        dd_logger.info(
            "Payment processing completed",
            transaction_id=transaction_id,
            success=result['success'],
            processing_time_ms=result.get('processing_time_ms', 0)
        )
        
        return result
        
    except Exception as e:
        dd_logger.error(
            "Payment processing failed",
            transaction_id=transaction_id,
            error=e,
            sender_id=payment_data['sender_id'],
            amount=payment_data['amount']
        )
        raise
```

## Dashboard Configuration

### DataDog Dashboard as Code
```python
from datadog import initialize, api
import json

class DataDogDashboards:
    def __init__(self):
        initialize(
            api_key=os.getenv('DATADOG_API_KEY'),
            app_key=os.getenv('DATADOG_APP_KEY')
        )
    
    def create_payment_system_dashboard(self):
        """Create main payment system dashboard"""
        
        dashboard_config = {
            "title": "PayPal Clone - Payment System Overview",
            "description": "Main dashboard for PayPal clone payment system monitoring",
            "widgets": [
                {
                    "definition": {
                        "type": "timeseries",
                        "requests": [
                            {
                                "q": "sum:payment.attempts{*} by {currency}.as_count()",
                                "display_type": "bars",
                                "style": {
                                    "palette": "dog_classic",
                                    "line_type": "solid",
                                    "line_width": "normal"
                                }
                            }
                        ],
                        "title": "Payment Attempts by Currency",
                        "title_size": "16",
                        "title_align": "left",
                        "show_legend": True,
                        "legend_size": "0"
                    },
                    "layout": {
                        "x": 0,
                        "y": 0,
                        "width": 4,
                        "height": 3
                    }
                },
                {
                    "definition": {
                        "type": "query_value",
                        "requests": [
                            {
                                "q": "sum:payment.completions{success:true}.as_count()",
                                "aggregator": "sum"
                            }
                        ],
                        "title": "Successful Payments (24h)",
                        "title_size": "16",
                        "title_align": "left",
                        "precision": 0
                    },
                    "layout": {
                        "x": 4,
                        "y": 0,
                        "width": 2,
                        "height": 2
                    }
                },
                {
                    "definition": {
                        "type": "query_value",
                        "requests": [
                            {
                                "q": "sum:payment.revenue{*}",
                                "aggregator": "sum"
                            }
                        ],
                        "title": "Total Revenue (24h)",
                        "title_size": "16",
                        "title_align": "left",
                        "precision": 2,
                        "custom_unit": "$"
                    },
                    "layout": {
                        "x": 6,
                        "y": 0,
                        "width": 2,
                        "height": 2
                    }
                },
                {
                    "definition": {
                        "type": "timeseries",
                        "requests": [
                            {
                                "q": "avg:payment.processing_time{*} by {payment_method}",
                                "display_type": "line"
                            }
                        ],
                        "title": "Average Payment Processing Time",
                        "title_size": "16",
                        "title_align": "left",
                        "yaxis": {
                            "label": "Time (ms)",
                            "scale": "linear",
                            "min": "auto",
                            "max": "auto"
                        }
                    },
                    "layout": {
                        "x": 0,
                        "y": 3,
                        "width": 4,
                        "height": 3
                    }
                },
                {
                    "definition": {
                        "type": "toplist",
                        "requests": [
                            {
                                "q": "top(sum:payment.attempts{*} by {currency}, 10, 'sum', 'desc')"
                            }
                        ],
                        "title": "Top Currencies by Volume"
                    },
                    "layout": {
                        "x": 4,
                        "y": 3,
                        "width": 4,
                        "height": 3
                    }
                }
            ],
            "layout_type": "ordered",
            "is_read_only": False,
            "notify_list": [],
            "reflow_type": "fixed"
        }
        
        response = api.Dashboard.create(**dashboard_config)
        return response
    
    def create_infrastructure_dashboard(self):
        """Create infrastructure monitoring dashboard"""
        
        dashboard_config = {
            "title": "PayPal Clone - Infrastructure Monitoring",
            "description": "Infrastructure and system health monitoring",
            "widgets": [
                {
                    "definition": {
                        "type": "hostmap",
                        "requests": {
                            "fill": {
                                "q": "avg:system.cpu.user{*} by {host}"
                            }
                        },
                        "title": "CPU Usage by Host"
                    },
                    "layout": {
                        "x": 0,
                        "y": 0,
                        "width": 6,
                        "height": 4
                    }
                },
                {
                    "definition": {
                        "type": "timeseries",
                        "requests": [
                            {
                                "q": "avg:database.query.execution_time{*} by {operation}",
                                "display_type": "line"
                            }
                        ],
                        "title": "Database Query Performance"
                    },
                    "layout": {
                        "x": 6,
                        "y": 0,
                        "width": 6,
                        "height": 4
                    }
                },
                {
                    "definition": {
                        "type": "timeseries",
                        "requests": [
                            {
                                "q": "avg:cache.hit_ratio{*}",
                                "display_type": "line"
                            }
                        ],
                        "title": "Cache Hit Ratio"
                    },
                    "layout": {
                        "x": 0,
                        "y": 4,
                        "width": 6,
                        "height": 3
                    }
                }
            ]
        }
        
        response = api.Dashboard.create(**dashboard_config)
        return response

dd_dashboards = DataDogDashboards()
```

## Alerting Configuration

### Alert Rules
```python
class DataDogAlerts:
    def __init__(self):
        initialize(
            api_key=os.getenv('DATADOG_API_KEY'),
            app_key=os.getenv('DATADOG_APP_KEY')
        )
    
    def create_payment_failure_alert(self):
        """Create alert for high payment failure rate"""
        
        alert_config = {
            "name": "High Payment Failure Rate",
            "message": """
            @slack-payments-alerts @pagerduty-payments
            
            Payment failure rate is above 5% for the last 10 minutes.
            
            This could indicate:
            - Database connectivity issues
            - External payment gateway problems
            - Fraud detection system issues
            
            Please investigate immediately.
            """,
            "query": "avg(last_10m):( sum:payment.completions{success:false}.as_count() / sum:payment.completions{*}.as_count() ) * 100 > 5",
            "type": "metric alert",
            "options": {
                "thresholds": {
                    "critical": 5.0,
                    "warning": 3.0
                },
                "notify_audit": False,
                "require_full_window": True,
                "notify_no_data": True,
                "no_data_timeframe": 20,
                "evaluation_delay": 60
            },
            "tags": ["service:payment", "severity:critical"]
        }
        
        response = api.Monitor.create(**alert_config)
        return response
    
    def create_response_time_alert(self):
        """Create alert for high API response times"""
        
        alert_config = {
            "name": "High API Response Time",
            "message": """
            @slack-engineering @pagerduty-engineering
            
            API response time is above 2 seconds for the last 5 minutes.
            
            Current p95 response time: {{value}}ms
            
            Please check:
            - Database performance
            - Cache hit rates
            - External service dependencies
            """,
            "query": "avg(last_5m):p95:api.response_time{*} > 2000",
            "type": "metric alert",
            "options": {
                "thresholds": {
                    "critical": 2000,
                    "warning": 1500
                },
                "notify_audit": False,
                "require_full_window": False,
                "notify_no_data": True,
                "no_data_timeframe": 10
            },
            "tags": ["service:api", "severity:warning"]
        }
        
        response = api.Monitor.create(**alert_config)
        return response
    
    def create_fraud_detection_alert(self):
        """Create alert for fraud detection system issues"""
        
        alert_config = {
            "name": "Fraud Detection System Down",
            "message": """
            @slack-security @pagerduty-security
            
            Fraud detection system appears to be down or not responding.
            
            All payments are currently being processed without fraud checks.
            This is a critical security issue.
            
            Immediate action required!
            """,
            "query": "avg(last_5m):sum:fraud.check{*}.as_count() < 1",
            "type": "metric alert",
            "options": {
                "thresholds": {
                    "critical": 1
                },
                "notify_audit": True,
                "require_full_window": True,
                "notify_no_data": True,
                "no_data_timeframe": 5
            },
            "tags": ["service:fraud", "severity:critical", "security:true"]
        }
        
        response = api.Monitor.create(**alert_config)
        return response

dd_alerts = DataDogAlerts()
```