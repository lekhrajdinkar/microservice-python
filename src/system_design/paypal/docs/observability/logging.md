# Logging Strategy

## Overview
Comprehensive logging strategy using structured logging with DataDog integration for centralized log management, analysis, and alerting in the PayPal clone system.

## Logging Architecture

```
┌─────────────────┐    JSON Logs     ┌─────────────────┐
│   Application   │─────────────────►│   DataDog       │
│   Services      │                  │   Log Agent     │
└─────────────────┘                  └─────────────────┘
         │                                     │
         │ Structured                          │ Parsed
         │ JSON                                │ Logs
         ▼                                     ▼
┌─────────────────┐                  ┌─────────────────┐
│   Log Files     │                  │   DataDog       │
│   (Kubernetes)  │                  │   Platform      │
└─────────────────┘                  └─────────────────┘
         │                                     │
         │ Container                           │ Indexed
         │ Logs                                │ & Searchable
         ▼                                     ▼
┌─────────────────┐                  ┌─────────────────┐
│   Kubernetes    │                  │   Log Analytics │
│   Log Driver    │                  │   & Alerting    │
└─────────────────┘                  └─────────────────┘
```

## Structured Logging Implementation

### Base Logger Configuration
```python
import structlog
import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from ddtrace import tracer
import os

# Configure structlog
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
        structlog.dev.ConsoleRenderer() if os.getenv('LOG_FORMAT') == 'console' 
        else structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

class PayPalCloneLogger:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = structlog.get_logger(service_name)
        self.base_context = {
            'service': service_name,
            'environment': os.getenv('ENVIRONMENT', 'production'),
            'version': os.getenv('APP_VERSION', '1.0.0'),
            'cluster': os.getenv('CLUSTER_NAME', 'paypal-clone')
        }
    
    def _enrich_log_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich log context with trace information and base context"""
        
        enriched_context = {**self.base_context, **context}
        
        # Add DataDog trace context
        span = tracer.current_span()
        if span:
            enriched_context.update({
                'dd.trace_id': str(span.trace_id),
                'dd.span_id': str(span.span_id),
                'dd.service': span.service or self.service_name
            })
        
        # Add correlation ID if available
        correlation_id = getattr(contextvars.get('correlation_id', None), 'get', lambda: None)()
        if correlation_id:
            enriched_context['correlation_id'] = correlation_id
        
        return enriched_context
    
    def info(self, message: str, **context):
        """Log info level message"""
        enriched_context = self._enrich_log_context(context)
        self.logger.info(message, **enriched_context)
    
    def warning(self, message: str, **context):
        """Log warning level message"""
        enriched_context = self._enrich_log_context(context)
        self.logger.warning(message, **enriched_context)
    
    def error(self, message: str, error: Optional[Exception] = None, **context):
        """Log error level message with optional exception details"""
        enriched_context = self._enrich_log_context(context)
        
        if error:
            enriched_context.update({
                'error.type': type(error).__name__,
                'error.message': str(error),
                'error.stack_trace': self._format_exception(error)
            })
        
        self.logger.error(message, **enriched_context)
    
    def debug(self, message: str, **context):
        """Log debug level message"""
        enriched_context = self._enrich_log_context(context)
        self.logger.debug(message, **enriched_context)
    
    def critical(self, message: str, **context):
        """Log critical level message"""
        enriched_context = self._enrich_log_context(context)
        self.logger.critical(message, **enriched_context)
    
    def _format_exception(self, error: Exception) -> str:
        """Format exception for logging"""
        import traceback
        return traceback.format_exc()

# Service-specific loggers
payment_logger = PayPalCloneLogger('payment-service')
user_logger = PayPalCloneLogger('user-service')
fraud_logger = PayPalCloneLogger('fraud-service')
notification_logger = PayPalCloneLogger('notification-service')
```

### Business Event Logging
```python
class BusinessEventLogger:
    def __init__(self):
        self.logger = PayPalCloneLogger('business-events')
    
    async def log_user_registration(self, user_data: Dict[str, Any]):
        """Log user registration event"""
        
        self.logger.info(
            "User registered successfully",
            event_type="user_registration",
            user_id=user_data['user_id'],
            email=user_data['email'],
            registration_method=user_data.get('method', 'email'),
            user_agent=user_data.get('user_agent'),
            ip_address=user_data.get('ip_address'),
            referrer=user_data.get('referrer')
        )
    
    async def log_payment_attempt(self, payment_data: Dict[str, Any]):
        """Log payment attempt"""
        
        self.logger.info(
            "Payment attempt initiated",
            event_type="payment_attempt",
            transaction_id=payment_data['transaction_id'],
            sender_id=payment_data['sender_id'],
            receiver_id=payment_data['receiver_id'],
            amount=payment_data['amount'],
            currency=payment_data['currency'],
            payment_method=payment_data['payment_method_type'],
            description=payment_data.get('description', ''),
            ip_address=payment_data.get('ip_address'),
            user_agent=payment_data.get('user_agent')
        )
    
    async def log_payment_completion(self, payment_result: Dict[str, Any]):
        """Log payment completion"""
        
        self.logger.info(
            "Payment completed",
            event_type="payment_completion",
            transaction_id=payment_result['transaction_id'],
            status=payment_result['status'],
            amount=payment_result['amount'],
            currency=payment_result['currency'],
            processing_time_ms=payment_result.get('processing_time_ms'),
            fees=payment_result.get('fees', 0),
            exchange_rate=payment_result.get('exchange_rate'),
            completion_timestamp=payment_result['completed_at']
        )
    
    async def log_fraud_detection(self, fraud_data: Dict[str, Any]):
        """Log fraud detection event"""
        
        log_level = 'warning' if fraud_data['action'] == 'review' else 'error'
        
        getattr(self.logger, log_level)(
            f"Fraud detection: {fraud_data['action']}",
            event_type="fraud_detection",
            transaction_id=fraud_data.get('transaction_id'),
            user_id=fraud_data['user_id'],
            risk_score=fraud_data['risk_score'],
            action=fraud_data['action'],
            risk_factors=fraud_data.get('risk_factors', []),
            model_version=fraud_data.get('model_version'),
            detection_time_ms=fraud_data.get('detection_time_ms')
        )
    
    async def log_kyc_verification(self, kyc_data: Dict[str, Any]):
        """Log KYC verification event"""
        
        self.logger.info(
            "KYC verification completed",
            event_type="kyc_verification",
            user_id=kyc_data['user_id'],
            verification_status=kyc_data['status'],
            verification_method=kyc_data['method'],
            document_types=kyc_data.get('document_types', []),
            verification_provider=kyc_data.get('provider'),
            processing_time_ms=kyc_data.get('processing_time_ms'),
            confidence_score=kyc_data.get('confidence_score')
        )

business_event_logger = BusinessEventLogger()
```

### Technical Event Logging
```python
class TechnicalEventLogger:
    def __init__(self):
        self.logger = PayPalCloneLogger('technical-events')
    
    async def log_database_operation(self, operation_data: Dict[str, Any]):
        """Log database operation"""
        
        log_level = 'error' if operation_data.get('error') else 'debug'
        
        getattr(self.logger, log_level)(
            f"Database operation: {operation_data['operation']}",
            event_type="database_operation",
            operation=operation_data['operation'],
            table=operation_data.get('table'),
            query_hash=operation_data.get('query_hash'),
            execution_time_ms=operation_data.get('execution_time_ms'),
            rows_affected=operation_data.get('rows_affected'),
            connection_pool_size=operation_data.get('connection_pool_size'),
            error=operation_data.get('error')
        )
    
    async def log_cache_operation(self, cache_data: Dict[str, Any]):
        """Log cache operation"""
        
        self.logger.debug(
            f"Cache operation: {cache_data['operation']}",
            event_type="cache_operation",
            operation=cache_data['operation'],
            key=cache_data['key'],
            hit=cache_data.get('hit'),
            response_time_ms=cache_data.get('response_time_ms'),
            cache_size=cache_data.get('cache_size'),
            ttl=cache_data.get('ttl')
        )
    
    async def log_api_request(self, request_data: Dict[str, Any]):
        """Log API request"""
        
        log_level = 'error' if request_data['status_code'] >= 400 else 'info'
        
        getattr(self.logger, log_level)(
            f"API request: {request_data['method']} {request_data['endpoint']}",
            event_type="api_request",
            method=request_data['method'],
            endpoint=request_data['endpoint'],
            status_code=request_data['status_code'],
            response_time_ms=request_data['response_time_ms'],
            request_size_bytes=request_data.get('request_size_bytes'),
            response_size_bytes=request_data.get('response_size_bytes'),
            user_id=request_data.get('user_id'),
            ip_address=request_data.get('ip_address'),
            user_agent=request_data.get('user_agent')
        )
    
    async def log_message_queue_operation(self, queue_data: Dict[str, Any]):
        """Log message queue operation"""
        
        log_level = 'error' if queue_data.get('error') else 'debug'
        
        getattr(self.logger, log_level)(
            f"Message queue: {queue_data['operation']}",
            event_type="message_queue_operation",
            queue_name=queue_data['queue_name'],
            operation=queue_data['operation'],
            message_id=queue_data.get('message_id'),
            processing_time_ms=queue_data.get('processing_time_ms'),
            queue_depth=queue_data.get('queue_depth'),
            retry_count=queue_data.get('retry_count'),
            error=queue_data.get('error')
        )
    
    async def log_external_service_call(self, service_data: Dict[str, Any]):
        """Log external service call"""
        
        log_level = 'error' if service_data.get('error') else 'info'
        
        getattr(self.logger, log_level)(
            f"External service call: {service_data['service_name']}",
            event_type="external_service_call",
            service_name=service_data['service_name'],
            endpoint=service_data['endpoint'],
            method=service_data['method'],
            status_code=service_data.get('status_code'),
            response_time_ms=service_data.get('response_time_ms'),
            retry_count=service_data.get('retry_count'),
            circuit_breaker_state=service_data.get('circuit_breaker_state'),
            error=service_data.get('error')
        )

technical_event_logger = TechnicalEventLogger()
```

### Security Event Logging
```python
class SecurityEventLogger:
    def __init__(self):
        self.logger = PayPalCloneLogger('security-events')
    
    async def log_authentication_attempt(self, auth_data: Dict[str, Any]):
        """Log authentication attempt"""
        
        log_level = 'warning' if not auth_data['success'] else 'info'
        
        getattr(self.logger, log_level)(
            f"Authentication attempt: {'success' if auth_data['success'] else 'failed'}",
            event_type="authentication_attempt",
            user_id=auth_data.get('user_id'),
            email=auth_data.get('email'),
            success=auth_data['success'],
            failure_reason=auth_data.get('failure_reason'),
            ip_address=auth_data['ip_address'],
            user_agent=auth_data.get('user_agent'),
            geolocation=auth_data.get('geolocation'),
            device_fingerprint=auth_data.get('device_fingerprint'),
            mfa_used=auth_data.get('mfa_used', False)
        )
    
    async def log_authorization_failure(self, authz_data: Dict[str, Any]):
        """Log authorization failure"""
        
        self.logger.warning(
            "Authorization failed",
            event_type="authorization_failure",
            user_id=authz_data['user_id'],
            resource=authz_data['resource'],
            action=authz_data['action'],
            required_permissions=authz_data.get('required_permissions', []),
            user_permissions=authz_data.get('user_permissions', []),
            ip_address=authz_data.get('ip_address'),
            endpoint=authz_data.get('endpoint')
        )
    
    async def log_suspicious_activity(self, activity_data: Dict[str, Any]):
        """Log suspicious activity"""
        
        self.logger.error(
            "Suspicious activity detected",
            event_type="suspicious_activity",
            user_id=activity_data.get('user_id'),
            activity_type=activity_data['activity_type'],
            risk_score=activity_data.get('risk_score'),
            indicators=activity_data.get('indicators', []),
            ip_address=activity_data.get('ip_address'),
            user_agent=activity_data.get('user_agent'),
            geolocation=activity_data.get('geolocation'),
            action_taken=activity_data.get('action_taken')
        )
    
    async def log_data_access(self, access_data: Dict[str, Any]):
        """Log sensitive data access"""
        
        self.logger.info(
            "Sensitive data accessed",
            event_type="data_access",
            user_id=access_data['user_id'],
            data_type=access_data['data_type'],
            resource_id=access_data.get('resource_id'),
            access_method=access_data['access_method'],
            ip_address=access_data.get('ip_address'),
            purpose=access_data.get('purpose')
        )
    
    async def log_security_incident(self, incident_data: Dict[str, Any]):
        """Log security incident"""
        
        self.logger.critical(
            "Security incident detected",
            event_type="security_incident",
            incident_id=incident_data['incident_id'],
            incident_type=incident_data['incident_type'],
            severity=incident_data['severity'],
            affected_users=incident_data.get('affected_users', []),
            affected_systems=incident_data.get('affected_systems', []),
            detection_method=incident_data.get('detection_method'),
            response_actions=incident_data.get('response_actions', []),
            estimated_impact=incident_data.get('estimated_impact')
        )

security_event_logger = SecurityEventLogger()
```

## Log Correlation and Context

### Request Correlation
```python
import contextvars
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Context variable for correlation ID
correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar('correlation_id')

class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate or extract correlation ID
        correlation_id = request.headers.get('X-Correlation-ID') or str(uuid.uuid4())
        
        # Set in context
        correlation_id_var.set(correlation_id)
        
        # Add to request state for access in handlers
        request.state.correlation_id = correlation_id
        
        # Process request
        response = await call_next(request)
        
        # Add correlation ID to response headers
        response.headers['X-Correlation-ID'] = correlation_id
        
        return response

class CorrelatedLogger:
    def __init__(self, base_logger: PayPalCloneLogger):
        self.base_logger = base_logger
    
    def _add_correlation_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Add correlation ID to log context"""
        
        correlation_id = correlation_id_var.get(None)
        if correlation_id:
            context['correlation_id'] = correlation_id
        
        return context
    
    def info(self, message: str, **context):
        context = self._add_correlation_context(context)
        self.base_logger.info(message, **context)
    
    def error(self, message: str, error: Optional[Exception] = None, **context):
        context = self._add_correlation_context(context)
        self.base_logger.error(message, error=error, **context)
    
    def warning(self, message: str, **context):
        context = self._add_correlation_context(context)
        self.base_logger.warning(message, **context)
    
    def debug(self, message: str, **context):
        context = self._add_correlation_context(context)
        self.base_logger.debug(message, **context)

# Usage
correlated_payment_logger = CorrelatedLogger(payment_logger)
```

### User Session Context
```python
class UserContextLogger:
    def __init__(self, base_logger: PayPalCloneLogger):
        self.base_logger = base_logger
    
    def with_user_context(self, user_id: str, session_id: str = None):
        """Create logger with user context"""
        
        class UserBoundLogger:
            def __init__(self, logger, user_id, session_id):
                self.logger = logger
                self.user_context = {
                    'user_id': user_id,
                    'session_id': session_id
                }
            
            def _add_user_context(self, context):
                return {**self.user_context, **context}
            
            def info(self, message: str, **context):
                self.logger.info(message, **self._add_user_context(context))
            
            def error(self, message: str, error: Exception = None, **context):
                self.logger.error(message, error=error, **self._add_user_context(context))
            
            def warning(self, message: str, **context):
                self.logger.warning(message, **self._add_user_context(context))
            
            def debug(self, message: str, **context):
                self.logger.debug(message, **self._add_user_context(context))
        
        return UserBoundLogger(self.base_logger, user_id, session_id)

# Usage
user_payment_logger = UserContextLogger(payment_logger)

async def process_user_payment(user_id: str, payment_data: dict):
    logger = user_payment_logger.with_user_context(user_id, payment_data.get('session_id'))
    
    logger.info("Processing payment", amount=payment_data['amount'])
    # ... payment processing logic
    logger.info("Payment completed successfully")
```

## Log Analysis and Monitoring

### Log-based Metrics
```python
class LogMetricsExtractor:
    def __init__(self):
        self.statsd = statsd
    
    async def extract_metrics_from_logs(self, log_entry: Dict[str, Any]):
        """Extract metrics from log entries"""
        
        event_type = log_entry.get('event_type')
        
        if event_type == 'payment_attempt':
            # Track payment attempts
            self.statsd.increment(
                'logs.payment.attempts',
                tags=[
                    f'currency:{log_entry.get("currency")}',
                    f'payment_method:{log_entry.get("payment_method")}'
                ]
            )
        
        elif event_type == 'payment_completion':
            # Track payment completions
            status = log_entry.get('status')
            self.statsd.increment(
                'logs.payment.completions',
                tags=[
                    f'status:{status}',
                    f'currency:{log_entry.get("currency")}'
                ]
            )
            
            # Track processing time
            processing_time = log_entry.get('processing_time_ms')
            if processing_time:
                self.statsd.histogram(
                    'logs.payment.processing_time',
                    processing_time,
                    tags=[f'status:{status}']
                )
        
        elif event_type == 'fraud_detection':
            # Track fraud detection
            action = log_entry.get('action')
            risk_score = log_entry.get('risk_score')
            
            self.statsd.increment(
                'logs.fraud.detections',
                tags=[f'action:{action}']
            )
            
            if risk_score:
                self.statsd.histogram(
                    'logs.fraud.risk_score',
                    risk_score,
                    tags=[f'action:{action}']
                )
        
        elif event_type == 'api_request':
            # Track API requests
            status_code = log_entry.get('status_code')
            endpoint = log_entry.get('endpoint')
            response_time = log_entry.get('response_time_ms')
            
            self.statsd.increment(
                'logs.api.requests',
                tags=[
                    f'endpoint:{endpoint}',
                    f'status_code:{status_code}'
                ]
            )
            
            if response_time:
                self.statsd.histogram(
                    'logs.api.response_time',
                    response_time,
                    tags=[f'endpoint:{endpoint}']
                )

log_metrics_extractor = LogMetricsExtractor()
```

### Log Alerting Rules
```python
class LogAlertingRules:
    def __init__(self):
        self.alert_rules = {
            'high_error_rate': {
                'query': 'status:error',
                'threshold': 100,  # errors per minute
                'window': '5m',
                'severity': 'warning'
            },
            'payment_failures': {
                'query': 'event_type:payment_completion status:failed',
                'threshold': 50,  # failed payments per minute
                'window': '5m',
                'severity': 'critical'
            },
            'fraud_blocks': {
                'query': 'event_type:fraud_detection action:block',
                'threshold': 10,  # blocked transactions per minute
                'window': '5m',
                'severity': 'warning'
            },
            'authentication_failures': {
                'query': 'event_type:authentication_attempt success:false',
                'threshold': 20,  # failed logins per minute
                'window': '5m',
                'severity': 'warning'
            },
            'security_incidents': {
                'query': 'event_type:security_incident',
                'threshold': 1,  # any security incident
                'window': '1m',
                'severity': 'critical'
            }
        }
    
    def get_datadog_monitor_config(self, rule_name: str) -> Dict[str, Any]:
        """Generate DataDog monitor configuration for log alert rule"""
        
        rule = self.alert_rules[rule_name]
        
        return {
            'name': f'Log Alert: {rule_name.replace("_", " ").title()}',
            'query': f'logs("{rule["query"]}").index("*").rollup("count").last("{rule["window"]}") > {rule["threshold"]}',
            'message': f'''
            @slack-alerts @pagerduty-{rule["severity"]}
            
            High rate of {rule_name.replace("_", " ")} detected in logs.
            
            Query: {rule["query"]}
            Threshold: {rule["threshold"]} events per {rule["window"]}
            
            Please investigate immediately.
            ''',
            'type': 'log alert',
            'options': {
                'thresholds': {
                    'critical': rule['threshold']
                },
                'notify_audit': rule['severity'] == 'critical',
                'require_full_window': True,
                'notify_no_data': False,
                'evaluation_delay': 60
            },
            'tags': [f'severity:{rule["severity"]}', f'source:logs']
        }

log_alerting_rules = LogAlertingRules()
```

## Log Retention and Archival

### Log Lifecycle Management
```python
class LogLifecycleManager:
    def __init__(self):
        self.s3_client = boto3.client('s3', region_name='us-east-1')
        self.log_bucket = 'paypal-clone-logs-archive'
    
    async def archive_old_logs(self, days_old: int = 30):
        """Archive logs older than specified days to S3"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        # Query DataDog for old logs
        from datadog import api
        
        query = f'@timestamp:<{cutoff_date.isoformat()}'
        
        # Export logs to S3
        export_request = {
            'query': query,
            'from': int((cutoff_date - timedelta(days=1)).timestamp() * 1000),
            'to': int(cutoff_date.timestamp() * 1000),
            'format': 'json'
        }
        
        # This would typically be done through DataDog's log export API
        # Implementation depends on DataDog's specific API
        
        logger.info(
            "Log archival initiated",
            cutoff_date=cutoff_date.isoformat(),
            estimated_logs=export_request
        )
    
    async def setup_log_retention_policy(self):
        """Setup automated log retention policy"""
        
        retention_policy = {
            'hot_storage': '7 days',    # Fast search and analysis
            'warm_storage': '30 days',  # Slower search, cost-effective
            'cold_storage': '1 year',   # Archive, compliance
            'deletion': '7 years'       # Legal requirement
        }
        
        logger.info(
            "Log retention policy configured",
            policy=retention_policy
        )

log_lifecycle_manager = LogLifecycleManager()
```

## Performance Optimization

### Log Sampling
```python
class LogSampler:
    def __init__(self, sample_rate: float = 0.1):
        self.sample_rate = sample_rate
        self.high_priority_events = {
            'security_incident',
            'fraud_detection',
            'payment_completion',
            'authentication_attempt'
        }
    
    def should_log(self, event_type: str, log_level: str) -> bool:
        """Determine if log should be written based on sampling rules"""
        
        # Always log high priority events
        if event_type in self.high_priority_events:
            return True
        
        # Always log errors and warnings
        if log_level in ['error', 'warning', 'critical']:
            return True
        
        # Sample other events
        import random
        return random.random() < self.sample_rate
    
    def adaptive_sampling(self, current_load: float) -> float:
        """Adjust sampling rate based on system load"""
        
        if current_load > 0.8:  # High load
            return 0.01  # 1% sampling
        elif current_load > 0.6:  # Medium load
            return 0.05  # 5% sampling
        else:  # Normal load
            return 0.1   # 10% sampling

log_sampler = LogSampler()

class SampledLogger(PayPalCloneLogger):
    def __init__(self, service_name: str):
        super().__init__(service_name)
        self.sampler = log_sampler
    
    def info(self, message: str, **context):
        event_type = context.get('event_type', 'general')
        if self.sampler.should_log(event_type, 'info'):
            super().info(message, **context)
    
    def debug(self, message: str, **context):
        event_type = context.get('event_type', 'general')
        if self.sampler.should_log(event_type, 'debug'):
            super().debug(message, **context)
    
    # Error, warning, and critical always logged
    def error(self, message: str, error: Optional[Exception] = None, **context):
        super().error(message, error=error, **context)
    
    def warning(self, message: str, **context):
        super().warning(message, **context)
    
    def critical(self, message: str, **context):
        super().critical(message, **context)

# Usage
sampled_payment_logger = SampledLogger('payment-service')
```