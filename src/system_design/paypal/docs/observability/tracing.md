# Distributed Tracing

## Overview
Comprehensive distributed tracing strategy using DataDog APM to track requests across microservices, identify performance bottlenecks, and troubleshoot issues in the PayPal clone system.

## Tracing Architecture

```
┌─────────────────┐    Trace Data    ┌─────────────────┐
│   Application   │─────────────────►│   DataDog       │
│   Services      │                  │   APM Agent     │
└─────────────────┘                  └─────────────────┘
         │                                     │
         │ Spans                               │ Processed
         │ & Traces                            │ Traces
         ▼                                     ▼
┌─────────────────┐                  ┌─────────────────┐
│   Service A     │◄────────────────►│   DataDog       │
│   (Payment)     │    Correlation   │   APM Platform  │
└─────────────────┘                  └─────────────────┘
         │                                     │
         │ Downstream                          │ Analytics
         │ Calls                               │ & Insights
         ▼                                     ▼
┌─────────────────┐                  ┌─────────────────┐
│   Service B     │                  │   Performance   │
│   (Fraud)       │                  │   Monitoring    │
└─────────────────┘                  └─────────────────┘
```

## DataDog APM Integration

### Tracer Configuration
```python
from ddtrace import config, patch_all, tracer
from ddtrace.ext import http, sql, errors
import os
import time
from typing import Dict, Any, Optional, Callable
from functools import wraps

# Configure DataDog APM
config.env = os.getenv('DD_ENV', 'production')
config.service = os.getenv('DD_SERVICE', 'paypal-clone')
config.version = os.getenv('DD_VERSION', '1.0.0')

# Configure service-specific settings
config.fastapi['service_name'] = 'paypal-clone-api'
config.fastapi['distributed_tracing'] = True
config.fastapi['analytics_enabled'] = True
config.fastapi['analytics_sample_rate'] = 1.0

config.sqlalchemy['service_name'] = 'paypal-clone-db'
config.sqlalchemy['analytics_enabled'] = True

config.redis['service_name'] = 'paypal-clone-cache'
config.redis['analytics_enabled'] = True

config.httpx['service_name'] = 'paypal-clone-http'
config.httpx['distributed_tracing'] = True

# Patch all supported libraries
patch_all()

# Configure tracer
tracer.configure(
    hostname=os.getenv('DD_AGENT_HOST', 'datadog-agent.datadog.svc.cluster.local'),
    port=int(os.getenv('DD_TRACE_AGENT_PORT', '8126')),
    https=False,
    priority_sampling=True,
    analytics_enabled=True,
    debug=os.getenv('DD_TRACE_DEBUG', 'false').lower() == 'true'
)

# Set global tags
tracer.set_tags({
    'cluster': os.getenv('CLUSTER_NAME', 'paypal-clone'),
    'region': os.getenv('AWS_REGION', 'us-east-1'),
    'deployment': os.getenv('DEPLOYMENT_ID', 'unknown')
})

class TracingManager:
    def __init__(self):
        self.tracer = tracer
    
    def trace_function(self, 
                      service_name: str = None, 
                      resource_name: str = None,
                      span_type: str = None,
                      tags: Dict[str, Any] = None):
        """Decorator for tracing functions with custom configuration"""
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                span_name = resource_name or f"{func.__module__}.{func.__name__}"
                
                with self.tracer.trace(
                    span_name,
                    service=service_name or config.service,
                    span_type=span_type
                ) as span:
                    # Add function metadata
                    span.set_tag('function.name', func.__name__)
                    span.set_tag('function.module', func.__module__)
                    
                    # Add custom tags
                    if tags:
                        for key, value in tags.items():
                            span.set_tag(key, value)
                    
                    try:
                        start_time = time.time()
                        result = await func(*args, **kwargs)
                        execution_time = (time.time() - start_time) * 1000
                        
                        span.set_tag('function.execution_time_ms', execution_time)
                        span.set_tag('function.result', 'success')
                        
                        return result
                        
                    except Exception as e:
                        span.set_tag('function.result', 'error')
                        span.set_tag(errors.ERROR_MSG, str(e))
                        span.set_tag(errors.ERROR_TYPE, type(e).__name__)
                        span.set_tag(errors.ERROR_STACK, traceback.format_exc())
                        span.error = 1
                        raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                span_name = resource_name or f"{func.__module__}.{func.__name__}"
                
                with self.tracer.trace(
                    span_name,
                    service=service_name or config.service,
                    span_type=span_type
                ) as span:
                    # Add function metadata
                    span.set_tag('function.name', func.__name__)
                    span.set_tag('function.module', func.__module__)
                    
                    # Add custom tags
                    if tags:
                        for key, value in tags.items():
                            span.set_tag(key, value)
                    
                    try:
                        start_time = time.time()
                        result = func(*args, **kwargs)
                        execution_time = (time.time() - start_time) * 1000
                        
                        span.set_tag('function.execution_time_ms', execution_time)
                        span.set_tag('function.result', 'success')
                        
                        return result
                        
                    except Exception as e:
                        span.set_tag('function.result', 'error')
                        span.set_tag(errors.ERROR_MSG, str(e))
                        span.set_tag(errors.ERROR_TYPE, type(e).__name__)
                        span.set_tag(errors.ERROR_STACK, traceback.format_exc())
                        span.error = 1
                        raise
            
            # Return appropriate wrapper based on function type
            import asyncio
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def get_current_trace_context(self) -> Dict[str, str]:
        """Get current trace context for propagation"""
        
        span = self.tracer.current_span()
        if span:
            return {
                'dd-trace-id': str(span.trace_id),
                'dd-span-id': str(span.span_id),
                'dd-parent-id': str(span.parent_id) if span.parent_id else '',
                'dd-sampling-priority': str(span.context.sampling_priority or 1)
            }
        return {}
    
    def inject_trace_context(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Inject trace context into HTTP headers"""
        
        context = self.get_current_trace_context()
        headers.update(context)
        return headers

tracing_manager = TracingManager()
```

### Business Process Tracing
```python
class PaymentTracing:
    def __init__(self):
        self.tracer = tracer
        self.tracing_manager = tracing_manager
    
    @tracing_manager.trace_function(
        service_name='payment-service',
        resource_name='payment.process_payment',
        span_type='business_logic',
        tags={'business_process': 'payment_processing'}
    )
    async def trace_payment_flow(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace complete payment processing flow"""
        
        span = self.tracer.current_span()
        
        # Add business context to span
        span.set_tag('payment.transaction_id', payment_data['transaction_id'])
        span.set_tag('payment.amount', payment_data['amount'])
        span.set_tag('payment.currency', payment_data['currency'])
        span.set_tag('payment.sender_id', payment_data['sender_id'])
        span.set_tag('payment.receiver_id', payment_data['receiver_id'])
        span.set_tag('payment.payment_method', payment_data['payment_method_type'])
        
        try:
            # Step 1: Validate payment
            validation_result = await self._trace_payment_validation(payment_data)
            span.set_tag('payment.validation_result', validation_result['valid'])
            
            if not validation_result['valid']:
                span.set_tag('payment.failure_reason', 'validation_failed')
                span.set_tag('payment.validation_errors', validation_result.get('errors', []))
                return {'success': False, 'error': 'Validation failed'}
            
            # Step 2: Fraud detection
            fraud_result = await self._trace_fraud_detection(payment_data)
            span.set_tag('payment.fraud_risk_score', fraud_result['risk_score'])
            span.set_tag('payment.fraud_action', fraud_result['action'])
            
            if fraud_result['action'] == 'block':
                span.set_tag('payment.failure_reason', 'fraud_blocked')
                span.set_tag('payment.fraud_factors', fraud_result.get('risk_factors', []))
                return {'success': False, 'error': 'Payment blocked due to fraud risk'}
            
            # Step 3: Process payment
            processing_result = await self._trace_payment_processing(payment_data)
            span.set_tag('payment.processing_result', 'success')
            span.set_tag('payment.final_status', processing_result['status'])
            
            # Step 4: Post-processing
            await self._trace_post_processing(processing_result)
            
            return processing_result
            
        except Exception as e:
            span.set_tag('payment.failure_reason', 'processing_error')
            span.set_tag(errors.ERROR_MSG, str(e))
            span.set_tag(errors.ERROR_TYPE, type(e).__name__)
            span.error = 1
            raise
    
    async def _trace_payment_validation(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace payment validation step"""
        
        with self.tracer.trace('payment.validation', service='validation-service') as span:
            span.set_tag('validation.amount', payment_data['amount'])
            span.set_tag('validation.currency', payment_data['currency'])
            span.set_tag('validation.sender_id', payment_data['sender_id'])
            
            # Balance validation
            balance_result = await self._trace_balance_validation(payment_data)
            span.set_tag('validation.balance_sufficient', balance_result['sufficient'])
            
            # Limits validation
            limits_result = await self._trace_limits_validation(payment_data)
            span.set_tag('validation.within_limits', limits_result['within_limits'])
            
            # Payment method validation
            method_result = await self._trace_payment_method_validation(payment_data)
            span.set_tag('validation.payment_method_valid', method_result['valid'])
            
            # Overall validation result
            valid = (balance_result['sufficient'] and 
                    limits_result['within_limits'] and 
                    method_result['valid'])
            
            span.set_tag('validation.overall_result', valid)
            
            return {
                'valid': valid,
                'balance_check': balance_result,
                'limits_check': limits_result,
                'method_check': method_result
            }
    
    async def _trace_balance_validation(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace balance validation with database query"""
        
        with self.tracer.trace('database.balance_check', service='database') as span:
            span.set_tag(sql.QUERY, 'SELECT balance FROM wallets WHERE user_id = ? AND currency = ?')
            span.set_tag('db.user_id', payment_data['sender_id'])
            span.set_tag('db.currency', payment_data['currency'])
            span.set_tag('db.operation', 'select')
            span.set_tag('db.table', 'wallets')
            
            # Simulate database query
            start_time = time.time()
            
            # Mock balance check (in real implementation, query database)
            current_balance = 1000.00  # Mock balance
            required_amount = payment_data['amount']
            sufficient = current_balance >= required_amount
            
            query_time = (time.time() - start_time) * 1000
            span.set_tag('db.query_time_ms', query_time)
            span.set_tag('db.current_balance', current_balance)
            span.set_tag('db.required_amount', required_amount)
            span.set_tag('db.sufficient_balance', sufficient)
            
            return {
                'sufficient': sufficient,
                'current_balance': current_balance,
                'required_amount': required_amount
            }
    
    async def _trace_fraud_detection(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace fraud detection process"""
        
        with self.tracer.trace('fraud.detection', service='fraud-service') as span:
            span.set_tag('fraud.transaction_id', payment_data['transaction_id'])
            span.set_tag('fraud.amount', payment_data['amount'])
            span.set_tag('fraud.sender_id', payment_data['sender_id'])
            span.set_tag('fraud.payment_method', payment_data['payment_method_type'])
            
            # Risk scoring
            risk_result = await self._trace_risk_scoring(payment_data)
            span.set_tag('fraud.risk_score', risk_result['score'])
            span.set_tag('fraud.risk_factors', risk_result['factors'])
            
            # Decision making
            decision_result = await self._trace_fraud_decision(risk_result)
            span.set_tag('fraud.decision', decision_result['action'])
            span.set_tag('fraud.confidence', decision_result['confidence'])
            
            return {
                'risk_score': risk_result['score'],
                'action': decision_result['action'],
                'risk_factors': risk_result['factors'],
                'confidence': decision_result['confidence']
            }
    
    async def _trace_risk_scoring(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace risk scoring algorithms"""
        
        with self.tracer.trace('fraud.risk_scoring', service='fraud-service') as span:
            span.set_tag('risk_scoring.model_version', '2.1.0')
            
            # Velocity check
            velocity_score = await self._trace_velocity_check(payment_data)
            span.set_tag('risk_scoring.velocity_score', velocity_score)
            
            # Device analysis
            device_score = await self._trace_device_analysis(payment_data)
            span.set_tag('risk_scoring.device_score', device_score)
            
            # Amount analysis
            amount_score = await self._trace_amount_analysis(payment_data)
            span.set_tag('risk_scoring.amount_score', amount_score)
            
            # Calculate overall risk score
            overall_score = (velocity_score + device_score + amount_score) / 3
            risk_factors = []
            
            if velocity_score > 70:
                risk_factors.append('high_velocity')
            if device_score > 70:
                risk_factors.append('suspicious_device')
            if amount_score > 70:
                risk_factors.append('unusual_amount')
            
            span.set_tag('risk_scoring.overall_score', overall_score)
            span.set_tag('risk_scoring.risk_factors', risk_factors)
            
            return {
                'score': overall_score,
                'factors': risk_factors,
                'component_scores': {
                    'velocity': velocity_score,
                    'device': device_score,
                    'amount': amount_score
                }
            }
    
    async def _trace_payment_processing(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trace actual payment processing"""
        
        with self.tracer.trace('payment.processing', service='payment-service') as span:
            transaction_id = payment_data['transaction_id']
            span.set_tag('processing.transaction_id', transaction_id)
            
            # Reserve funds
            reserve_result = await self._trace_funds_reservation(payment_data)
            span.set_tag('processing.funds_reserved', reserve_result['success'])
            
            if not reserve_result['success']:
                span.set_tag('processing.failure_reason', 'funds_reservation_failed')
                raise Exception('Failed to reserve funds')
            
            # Execute transfer
            transfer_result = await self._trace_funds_transfer(payment_data)
            span.set_tag('processing.transfer_completed', transfer_result['success'])
            
            if not transfer_result['success']:
                # Rollback reservation
                await self._trace_funds_rollback(payment_data)
                span.set_tag('processing.failure_reason', 'transfer_failed')
                raise Exception('Failed to transfer funds')
            
            # Update transaction status
            await self._trace_transaction_update(transaction_id, 'completed')
            span.set_tag('processing.final_status', 'completed')
            
            return {
                'success': True,
                'transaction_id': transaction_id,
                'status': 'completed',
                'amount': payment_data['amount'],
                'currency': payment_data['currency']
            }

payment_tracing = PaymentTracing()
```

### Database Query Tracing
```python
class DatabaseTracing:
    def __init__(self):
        self.tracer = tracer
    
    async def trace_database_operation(self, 
                                     operation: str, 
                                     table: str, 
                                     query: str,
                                     params: Dict[str, Any] = None) -> Any:
        """Trace database operations with detailed context"""
        
        with self.tracer.trace(f'database.{operation}', service='database') as span:
            # Add SQL context
            span.set_tag(sql.QUERY, query)
            span.set_tag('db.operation', operation)
            span.set_tag('db.table', table)
            span.set_tag('db.type', 'postgresql')
            
            # Add query parameters (sanitized)
            if params:
                sanitized_params = self._sanitize_params(params)
                span.set_tag('db.params', sanitized_params)
            
            try:
                start_time = time.time()
                
                # Execute query (mock implementation)
                result = await self._execute_query(query, params)
                
                execution_time = (time.time() - start_time) * 1000
                span.set_tag('db.execution_time_ms', execution_time)
                span.set_tag('db.rows_affected', len(result) if isinstance(result, list) else 1)
                span.set_tag('db.result', 'success')
                
                return result
                
            except Exception as e:
                span.set_tag('db.result', 'error')
                span.set_tag(errors.ERROR_MSG, str(e))
                span.set_tag(errors.ERROR_TYPE, type(e).__name__)
                span.error = 1
                raise
    
    def _sanitize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize parameters to avoid logging sensitive data"""
        
        sensitive_keys = {'password', 'ssn', 'card_number', 'cvv', 'token'}
        sanitized = {}
        
        for key, value in params.items():
            if any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
                sanitized[key] = '[REDACTED]'
            else:
                sanitized[key] = str(value)[:100]  # Truncate long values
        
        return sanitized
    
    async def _execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        """Mock query execution"""
        # In real implementation, this would execute the actual query
        await asyncio.sleep(0.01)  # Simulate query time
        return [{'id': 1, 'result': 'success'}]

database_tracing = DatabaseTracing()
```

### External Service Tracing
```python
class ExternalServiceTracing:
    def __init__(self):
        self.tracer = tracer
    
    async def trace_http_request(self, 
                               service_name: str,
                               method: str,
                               url: str,
                               headers: Dict[str, str] = None,
                               data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Trace HTTP requests to external services"""
        
        with self.tracer.trace(f'http.{method.lower()}', service=f'external-{service_name}') as span:
            # Add HTTP context
            span.set_tag(http.METHOD, method)
            span.set_tag(http.URL, url)
            span.set_tag('http.service_name', service_name)
            
            # Inject trace context into headers
            if headers is None:
                headers = {}
            
            headers = tracing_manager.inject_trace_context(headers)
            
            try:
                start_time = time.time()
                
                # Make HTTP request (mock implementation)
                response = await self._make_http_request(method, url, headers, data)
                
                request_time = (time.time() - start_time) * 1000
                span.set_tag('http.request_time_ms', request_time)
                span.set_tag(http.STATUS_CODE, response['status_code'])
                span.set_tag('http.response_size', len(str(response.get('body', ''))))
                
                if response['status_code'] >= 400:
                    span.set_tag('http.error', True)
                    span.set_tag(errors.ERROR_MSG, f"HTTP {response['status_code']}")
                
                return response
                
            except Exception as e:
                span.set_tag('http.error', True)
                span.set_tag(errors.ERROR_MSG, str(e))
                span.set_tag(errors.ERROR_TYPE, type(e).__name__)
                span.error = 1
                raise
    
    async def _make_http_request(self, method: str, url: str, 
                               headers: Dict[str, str], 
                               data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock HTTP request"""
        # In real implementation, use httpx or similar
        await asyncio.sleep(0.1)  # Simulate network delay
        return {
            'status_code': 200,
            'body': {'result': 'success'},
            'headers': {'content-type': 'application/json'}
        }

external_service_tracing = ExternalServiceTracing()
```

## Custom Span Annotations

### Business Metrics in Spans
```python
class BusinessSpanAnnotator:
    def __init__(self):
        self.tracer = tracer
    
    def annotate_payment_span(self, span, payment_data: Dict[str, Any]):
        """Add business-specific annotations to payment spans"""
        
        # Financial metrics
        span.set_tag('business.revenue', payment_data.get('fees', 0))
        span.set_tag('business.transaction_value', payment_data['amount'])
        span.set_tag('business.currency', payment_data['currency'])
        
        # Customer metrics
        span.set_tag('business.customer_tier', payment_data.get('customer_tier', 'standard'))
        span.set_tag('business.customer_lifetime_value', payment_data.get('customer_ltv', 0))
        
        # Product metrics
        span.set_tag('business.product_category', 'p2p_payment')
        span.set_tag('business.payment_channel', payment_data.get('channel', 'web'))
        
        # Geographic metrics
        span.set_tag('business.sender_country', payment_data.get('sender_country', 'US'))
        span.set_tag('business.receiver_country', payment_data.get('receiver_country', 'US'))
        span.set_tag('business.cross_border', 
                    payment_data.get('sender_country') != payment_data.get('receiver_country'))
    
    def annotate_user_span(self, span, user_data: Dict[str, Any]):
        """Add user-specific annotations to spans"""
        
        # User characteristics
        span.set_tag('business.user_segment', user_data.get('segment', 'retail'))
        span.set_tag('business.user_tenure_days', user_data.get('tenure_days', 0))
        span.set_tag('business.kyc_level', user_data.get('kyc_level', 'basic'))
        
        # Behavioral metrics
        span.set_tag('business.monthly_transaction_count', user_data.get('monthly_txn_count', 0))
        span.set_tag('business.monthly_transaction_volume', user_data.get('monthly_txn_volume', 0))
        
        # Risk metrics
        span.set_tag('business.risk_score', user_data.get('risk_score', 0))
        span.set_tag('business.fraud_history', user_data.get('has_fraud_history', False))

business_annotator = BusinessSpanAnnotator()
```

### Performance Annotations
```python
class PerformanceSpanAnnotator:
    def __init__(self):
        self.tracer = tracer
    
    def annotate_performance_metrics(self, span, metrics: Dict[str, Any]):
        """Add performance metrics to spans"""
        
        # Resource utilization
        span.set_tag('performance.cpu_usage_percent', metrics.get('cpu_usage', 0))
        span.set_tag('performance.memory_usage_mb', metrics.get('memory_usage', 0))
        span.set_tag('performance.disk_io_mb', metrics.get('disk_io', 0))
        
        # Database performance
        span.set_tag('performance.db_connection_time_ms', metrics.get('db_connection_time', 0))
        span.set_tag('performance.db_query_count', metrics.get('db_query_count', 0))
        span.set_tag('performance.db_total_time_ms', metrics.get('db_total_time', 0))
        
        # Cache performance
        span.set_tag('performance.cache_hit_ratio', metrics.get('cache_hit_ratio', 0))
        span.set_tag('performance.cache_response_time_ms', metrics.get('cache_response_time', 0))
        
        # Network performance
        span.set_tag('performance.network_latency_ms', metrics.get('network_latency', 0))
        span.set_tag('performance.bandwidth_usage_mbps', metrics.get('bandwidth_usage', 0))

performance_annotator = PerformanceSpanAnnotator()
```

## Trace Analysis and Optimization

### Trace Analytics
```python
class TraceAnalytics:
    def __init__(self):
        self.datadog_api = datadog.api
    
    async def analyze_payment_traces(self, time_range: str = '1h') -> Dict[str, Any]:
        """Analyze payment processing traces for insights"""
        
        # Query traces from DataDog
        query = f'service:payment-service operation_name:payment.process_payment @duration:>{time_range}'
        
        traces = await self._query_traces(query, time_range)
        
        analysis = {
            'total_traces': len(traces),
            'avg_duration_ms': sum(t['duration'] for t in traces) / len(traces) if traces else 0,
            'error_rate': len([t for t in traces if t.get('error')]) / len(traces) if traces else 0,
            'p95_duration_ms': self._calculate_percentile(traces, 95),
            'p99_duration_ms': self._calculate_percentile(traces, 99),
            'slowest_operations': self._find_slowest_operations(traces),
            'error_patterns': self._analyze_error_patterns(traces)
        }
        
        return analysis
    
    async def _query_traces(self, query: str, time_range: str) -> list:
        """Query traces from DataDog API"""
        
        # Mock implementation - in reality, use DataDog API
        return [
            {'duration': 150, 'error': False, 'operation': 'payment.validation'},
            {'duration': 300, 'error': False, 'operation': 'payment.processing'},
            {'duration': 500, 'error': True, 'operation': 'payment.processing'},
        ]
    
    def _calculate_percentile(self, traces: list, percentile: int) -> float:
        """Calculate percentile of trace durations"""
        
        if not traces:
            return 0
        
        durations = sorted([t['duration'] for t in traces])
        index = int((percentile / 100) * len(durations))
        return durations[min(index, len(durations) - 1)]
    
    def _find_slowest_operations(self, traces: list, limit: int = 5) -> list:
        """Find slowest operations in traces"""
        
        operation_times = {}
        for trace in traces:
            op = trace.get('operation', 'unknown')
            if op not in operation_times:
                operation_times[op] = []
            operation_times[op].append(trace['duration'])
        
        # Calculate average duration per operation
        avg_times = {
            op: sum(times) / len(times) 
            for op, times in operation_times.items()
        }
        
        # Sort by average duration
        slowest = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)
        return slowest[:limit]
    
    def _analyze_error_patterns(self, traces: list) -> Dict[str, Any]:
        """Analyze error patterns in traces"""
        
        error_traces = [t for t in traces if t.get('error')]
        
        if not error_traces:
            return {'total_errors': 0}
        
        error_operations = {}
        for trace in error_traces:
            op = trace.get('operation', 'unknown')
            error_operations[op] = error_operations.get(op, 0) + 1
        
        return {
            'total_errors': len(error_traces),
            'error_by_operation': error_operations,
            'error_rate_by_operation': {
                op: count / len([t for t in traces if t.get('operation') == op])
                for op, count in error_operations.items()
            }
        }

trace_analytics = TraceAnalytics()
```

### Trace-based Alerting
```python
class TraceAlerting:
    def __init__(self):
        self.alert_rules = {
            'high_payment_latency': {
                'query': 'service:payment-service operation_name:payment.process_payment',
                'metric': 'p95(duration)',
                'threshold': 2000,  # 2 seconds
                'window': '5m'
            },
            'payment_error_rate': {
                'query': 'service:payment-service operation_name:payment.process_payment',
                'metric': 'error_rate',
                'threshold': 0.05,  # 5%
                'window': '10m'
            },
            'database_slow_queries': {
                'query': 'service:database operation_name:database.*',
                'metric': 'p95(duration)',
                'threshold': 1000,  # 1 second
                'window': '5m'
            }
        }
    
    def create_datadog_apm_alerts(self):
        """Create APM-based alerts in DataDog"""
        
        alerts = []
        
        for alert_name, config in self.alert_rules.items():
            alert_config = {
                'name': f'APM Alert: {alert_name.replace("_", " ").title()}',
                'query': f'trace.{config["query"]}.{config["metric"]} > {config["threshold"]}',
                'message': f'''
                @slack-engineering @pagerduty-performance
                
                High {config["metric"]} detected for {config["query"]}
                
                Threshold: {config["threshold"]}
                Window: {config["window"]}
                
                Please investigate performance issues.
                ''',
                'type': 'trace-analytics alert',
                'options': {
                    'thresholds': {
                        'critical': config['threshold']
                    },
                    'notify_audit': False,
                    'require_full_window': True,
                    'notify_no_data': False
                },
                'tags': ['source:apm', 'severity:warning']
            }
            
            alerts.append(alert_config)
        
        return alerts

trace_alerting = TraceAlerting()
```

## Trace Sampling and Performance

### Intelligent Sampling
```python
class TraceSampler:
    def __init__(self):
        self.base_sample_rate = 0.1  # 10% default
        self.high_priority_operations = {
            'payment.process_payment',
            'fraud.detection',
            'user.authentication'
        }
    
    def get_sample_rate(self, operation_name: str, context: Dict[str, Any]) -> float:
        """Determine sampling rate based on operation and context"""
        
        # Always sample high-priority operations
        if operation_name in self.high_priority_operations:
            return 1.0
        
        # Sample errors at higher rate
        if context.get('error'):
            return 0.5
        
        # Sample slow operations at higher rate
        if context.get('duration_ms', 0) > 1000:
            return 0.8
        
        # Sample based on user tier
        user_tier = context.get('user_tier', 'standard')
        if user_tier == 'premium':
            return 0.3
        elif user_tier == 'enterprise':
            return 0.5
        
        # Default sampling
        return self.base_sample_rate
    
    def configure_priority_sampling(self):
        """Configure priority sampling rules"""
        
        # Set sampling rules
        tracer.configure(
            priority_sampling=True,
            analytics_enabled=True
        )
        
        # Custom sampling rules can be set here
        # This would typically be done through DataDog agent configuration

trace_sampler = TraceSampler()
```