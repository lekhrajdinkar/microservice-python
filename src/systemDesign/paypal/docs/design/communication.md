# Communication Patterns

## Overview
AWS-native communication patterns for microservices architecture using SQS, EventBridge, and API Gateway for reliable, scalable inter-service communication.

## Communication Architecture

```
┌─────────────────┐    REST/gRPC    ┌─────────────────┐
│   API Gateway   │◄──────────────►│  User Service   │
└─────────────────┘                └─────────────────┘
         │                                   │
         │ REST                              │ Events
         ▼                                   ▼
┌─────────────────┐                ┌─────────────────┐
│Payment Service  │                │  EventBridge    │
└─────────────────┘                └─────────────────┘
         │                                   │
         │ SQS                               │ Events
         ▼                                   ▼
┌─────────────────┐    Events      ┌─────────────────┐
│Transaction Svc  │◄──────────────►│Notification Svc │
└─────────────────┘                └─────────────────┘
```

## Synchronous Communication

### 1. REST API Communication
**Service-to-service HTTP calls for immediate responses**

```python
# HTTP client configuration
import httpx
from typing import Optional

class ServiceClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={"Content-Type": "application/json"}
        )
    
    async def get_user_profile(self, user_id: str) -> Optional[dict]:
        """Get user profile from User Service"""
        try:
            response = await self.client.get(f"/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to get user profile: {e}")
            return None
    
    async def validate_payment_method(self, method_id: str, user_id: str) -> bool:
        """Validate payment method with Account Service"""
        try:
            response = await self.client.post(
                "/payment-methods/validate",
                json={"method_id": method_id, "user_id": user_id}
            )
            return response.status_code == 200
        except httpx.HTTPError:
            return False

# Service discovery with AWS Service Discovery
user_service = ServiceClient("http://user-service.paypal.local:8000")
account_service = ServiceClient("http://account-service.paypal.local:8000")
```

### 2. gRPC Communication
**High-performance internal communication**

```python
# gRPC service definition (proto file)
"""
syntax = "proto3";

service WalletService {
    rpc GetBalance(BalanceRequest) returns (BalanceResponse);
    rpc UpdateBalance(UpdateBalanceRequest) returns (UpdateBalanceResponse);
    rpc TransferFunds(TransferRequest) returns (TransferResponse);
}

message BalanceRequest {
    string wallet_id = 1;
    string currency = 2;
}

message BalanceResponse {
    double balance = 1;
    double available_balance = 2;
    double frozen_balance = 3;
}
"""

# gRPC client implementation
import grpc
from . import wallet_pb2_grpc, wallet_pb2

class WalletServiceClient:
    def __init__(self, server_address: str):
        self.channel = grpc.aio.insecure_channel(server_address)
        self.stub = wallet_pb2_grpc.WalletServiceStub(self.channel)
    
    async def get_balance(self, wallet_id: str, currency: str) -> dict:
        """Get wallet balance via gRPC"""
        request = wallet_pb2.BalanceRequest(
            wallet_id=wallet_id,
            currency=currency
        )
        
        try:
            response = await self.stub.GetBalance(request)
            return {
                "balance": response.balance,
                "available_balance": response.available_balance,
                "frozen_balance": response.frozen_balance
            }
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {e}")
            raise
    
    async def transfer_funds(self, from_wallet: str, to_wallet: str, amount: float):
        """Transfer funds between wallets"""
        request = wallet_pb2.TransferRequest(
            from_wallet_id=from_wallet,
            to_wallet_id=to_wallet,
            amount=amount
        )
        
        response = await self.stub.TransferFunds(request)
        return response.success

# gRPC server implementation
class WalletServiceServer(wallet_pb2_grpc.WalletServiceServicer):
    async def GetBalance(self, request, context):
        balance_data = await get_wallet_balance(request.wallet_id, request.currency)
        
        return wallet_pb2.BalanceResponse(
            balance=balance_data["balance"],
            available_balance=balance_data["available_balance"],
            frozen_balance=balance_data["frozen_balance"]
        )
```

### 3. GraphQL Federation
**Unified API for client applications**

```python
# GraphQL schema federation
import strawberry
from typing import List, Optional

@strawberry.type
class User:
    id: str
    email: str
    first_name: str
    last_name: str
    
    @strawberry.field
    async def wallets(self) -> List["Wallet"]:
        return await get_user_wallets(self.id)

@strawberry.type
class Wallet:
    id: str
    currency: str
    balance: float
    
    @strawberry.field
    async def transactions(self, limit: int = 10) -> List["Transaction"]:
        return await get_wallet_transactions(self.id, limit)

@strawberry.type
class Transaction:
    id: str
    amount: float
    currency: str
    status: str
    created_at: str

# Federated schema
@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: str) -> Optional[User]:
        return await get_user_by_id(id)
    
    @strawberry.field
    async def transaction(self, id: str) -> Optional[Transaction]:
        return await get_transaction_by_id(id)

schema = strawberry.federation.Schema(query=Query)
```

## Asynchronous Communication

### 1. AWS SQS Message Queues
**Reliable message delivery between services**

```python
import boto3
import json
from typing import Dict, Any

class SQSMessageHandler:
    def __init__(self):
        self.sqs = boto3.client('sqs', region_name='us-east-1')
        self.queues = {
            'payment_processing': 'https://sqs.us-east-1.amazonaws.com/123456789/payment-processing',
            'transaction_events': 'https://sqs.us-east-1.amazonaws.com/123456789/transaction-events',
            'notification_queue': 'https://sqs.us-east-1.amazonaws.com/123456789/notifications',
            'audit_queue': 'https://sqs.us-east-1.amazonaws.com/123456789/audit-logs'
        }
    
    async def send_payment_event(self, event_data: Dict[str, Any]):
        """Send payment processing event"""
        message = {
            'event_type': 'payment_initiated',
            'transaction_id': event_data['transaction_id'],
            'sender_id': event_data['sender_id'],
            'receiver_id': event_data['receiver_id'],
            'amount': event_data['amount'],
            'currency': event_data['currency'],
            'timestamp': event_data['timestamp']
        }
        
        response = await self.sqs.send_message(
            QueueUrl=self.queues['payment_processing'],
            MessageBody=json.dumps(message),
            MessageAttributes={
                'event_type': {
                    'StringValue': 'payment_initiated',
                    'DataType': 'String'
                },
                'priority': {
                    'StringValue': 'high',
                    'DataType': 'String'
                }
            }
        )
        
        return response['MessageId']
    
    async def process_messages(self, queue_name: str, handler_func):
        """Process messages from SQS queue"""
        queue_url = self.queues[queue_name]
        
        while True:
            response = await self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20,  # Long polling
                MessageAttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            
            for message in messages:
                try:
                    # Process message
                    message_body = json.loads(message['Body'])
                    await handler_func(message_body)
                    
                    # Delete message after successful processing
                    await self.sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    
                except Exception as e:
                    logger.error(f"Failed to process message: {e}")
                    # Message will be retried or sent to DLQ
```

### 2. AWS EventBridge
**Event-driven architecture for domain events**

```python
import boto3
from datetime import datetime

class EventBridgePublisher:
    def __init__(self):
        self.eventbridge = boto3.client('events', region_name='us-east-1')
        self.event_bus_name = 'paypal-clone-events'
    
    async def publish_transaction_event(self, event_type: str, transaction_data: dict):
        """Publish transaction events to EventBridge"""
        
        event_detail = {
            'transaction_id': transaction_data['transaction_id'],
            'sender_id': transaction_data['sender_id'],
            'receiver_id': transaction_data['receiver_id'],
            'amount': transaction_data['amount'],
            'currency': transaction_data['currency'],
            'status': transaction_data['status'],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        response = await self.eventbridge.put_events(
            Entries=[
                {
                    'Source': 'paypal-clone.transaction-service',
                    'DetailType': f'Transaction {event_type}',
                    'Detail': json.dumps(event_detail),
                    'EventBusName': self.event_bus_name,
                    'Resources': [
                        f'arn:aws:paypal-clone:transaction:{transaction_data["transaction_id"]}'
                    ]
                }
            ]
        )
        
        return response['Entries'][0]['EventId']
    
    async def publish_user_event(self, event_type: str, user_data: dict):
        """Publish user events"""
        
        event_detail = {
            'user_id': user_data['user_id'],
            'email': user_data.get('email'),
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        await self.eventbridge.put_events(
            Entries=[
                {
                    'Source': 'paypal-clone.user-service',
                    'DetailType': f'User {event_type}',
                    'Detail': json.dumps(event_detail),
                    'EventBusName': self.event_bus_name
                }
            ]
        )

# Event handlers for different services
class TransactionEventHandler:
    def __init__(self):
        self.eventbridge = EventBridgePublisher()
    
    async def handle_payment_completed(self, transaction_data: dict):
        """Handle payment completion event"""
        
        # Update wallet balances
        await self.update_wallet_balances(transaction_data)
        
        # Send notification
        await self.send_completion_notification(transaction_data)
        
        # Log audit event
        await self.log_audit_event(transaction_data)
        
        # Publish completion event
        await self.eventbridge.publish_transaction_event(
            'completed', 
            transaction_data
        )
```

### 3. Dead Letter Queues (DLQ)
**Handle failed message processing**

```python
class DLQHandler:
    def __init__(self):
        self.sqs = boto3.client('sqs')
        self.dlq_url = 'https://sqs.us-east-1.amazonaws.com/123456789/payment-dlq'
    
    async def process_dlq_messages(self):
        """Process messages from Dead Letter Queue"""
        
        response = await self.sqs.receive_message(
            QueueUrl=self.dlq_url,
            MaxNumberOfMessages=10
        )
        
        messages = response.get('Messages', [])
        
        for message in messages:
            try:
                # Analyze failure reason
                failure_reason = await self.analyze_failure(message)
                
                # Attempt manual processing or alert operations
                if failure_reason == 'temporary_error':
                    await self.retry_message(message)
                else:
                    await self.alert_operations(message, failure_reason)
                
                # Remove from DLQ
                await self.sqs.delete_message(
                    QueueUrl=self.dlq_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
                
            except Exception as e:
                logger.error(f"Failed to process DLQ message: {e}")
```

## Circuit Breaker Pattern

### Implementation for Service Resilience
```python
import asyncio
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        return (
            self.last_failure_time and
            datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout)
        )
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage with service calls
user_service_breaker = CircuitBreaker(failure_threshold=3, timeout=30)

async def get_user_with_breaker(user_id: str):
    return await user_service_breaker.call(
        user_service.get_user_profile,
        user_id
    )
```

## Saga Pattern for Distributed Transactions

### Choreography-based Saga
```python
class PaymentSaga:
    def __init__(self):
        self.eventbridge = EventBridgePublisher()
        self.sqs = SQSMessageHandler()
    
    async def initiate_payment_saga(self, payment_data: dict):
        """Start payment processing saga"""
        
        saga_id = str(uuid.uuid4())
        
        # Step 1: Reserve funds
        await self.eventbridge.publish_transaction_event(
            'funds_reservation_requested',
            {
                'saga_id': saga_id,
                'transaction_id': payment_data['transaction_id'],
                'sender_wallet_id': payment_data['sender_wallet_id'],
                'amount': payment_data['amount']
            }
        )
    
    async def handle_funds_reserved(self, event_data: dict):
        """Handle successful funds reservation"""
        
        # Step 2: Process payment
        await self.eventbridge.publish_transaction_event(
            'payment_processing_requested',
            {
                'saga_id': event_data['saga_id'],
                'transaction_id': event_data['transaction_id'],
                'receiver_wallet_id': event_data['receiver_wallet_id'],
                'amount': event_data['amount']
            }
        )
    
    async def handle_payment_failed(self, event_data: dict):
        """Handle payment failure - compensate"""
        
        # Compensating action: Release reserved funds
        await self.eventbridge.publish_transaction_event(
            'funds_release_requested',
            {
                'saga_id': event_data['saga_id'],
                'transaction_id': event_data['transaction_id'],
                'sender_wallet_id': event_data['sender_wallet_id'],
                'amount': event_data['amount']
            }
        )
```

## Message Serialization

### Avro Schema for Message Consistency
```python
import avro.schema
import avro.io
import io

# Avro schema for transaction events
transaction_schema = avro.schema.parse("""
{
    "type": "record",
    "name": "TransactionEvent",
    "fields": [
        {"name": "transaction_id", "type": "string"},
        {"name": "event_type", "type": "string"},
        {"name": "sender_id", "type": "string"},
        {"name": "receiver_id", "type": "string"},
        {"name": "amount", "type": "double"},
        {"name": "currency", "type": "string"},
        {"name": "timestamp", "type": "long"},
        {"name": "metadata", "type": {"type": "map", "values": "string"}}
    ]
}
""")

class AvroMessageSerializer:
    def __init__(self, schema):
        self.schema = schema
    
    def serialize(self, data: dict) -> bytes:
        """Serialize data to Avro binary format"""
        writer = avro.io.DatumWriter(self.schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(data, encoder)
        return bytes_writer.getvalue()
    
    def deserialize(self, data: bytes) -> dict:
        """Deserialize Avro binary data"""
        reader = avro.io.DatumReader(self.schema)
        bytes_reader = io.BytesIO(data)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        return reader.read(decoder)
```

## Service Mesh Integration

### AWS App Mesh Configuration
```yaml
# Virtual service definition
VirtualService:
  Type: AWS::AppMesh::VirtualService
  Properties:
    MeshName: paypal-clone-mesh
    VirtualServiceName: payment-service.paypal.local
    Spec:
      Provider:
        VirtualRouter:
          VirtualRouterName: payment-service-router

# Virtual router for load balancing
VirtualRouter:
  Type: AWS::AppMesh::VirtualRouter
  Properties:
    MeshName: paypal-clone-mesh
    VirtualRouterName: payment-service-router
    Spec:
      Listeners:
        - PortMapping:
            Port: 8000
            Protocol: http

# Route configuration
Route:
  Type: AWS::AppMesh::Route
  Properties:
    MeshName: paypal-clone-mesh
    VirtualRouterName: payment-service-router
    RouteName: payment-service-route
    Spec:
      HttpRoute:
        Match:
          Prefix: /
        Action:
          WeightedTargets:
            - VirtualNode: payment-service-v1
              Weight: 90
            - VirtualNode: payment-service-v2
              Weight: 10
```

## Monitoring Communication

### Distributed Tracing
```python
from ddtrace import tracer

@tracer.wrap("payment.process")
async def process_payment(payment_data: dict):
    """Process payment with distributed tracing"""
    
    with tracer.trace("payment.validate") as span:
        span.set_tag("user_id", payment_data["sender_id"])
        span.set_tag("amount", payment_data["amount"])
        
        # Validate payment
        is_valid = await validate_payment(payment_data)
        span.set_tag("validation_result", is_valid)
    
    if is_valid:
        with tracer.trace("payment.execute") as span:
            result = await execute_payment(payment_data)
            span.set_tag("transaction_id", result["transaction_id"])
            return result
```

### Communication Metrics
```python
# Custom metrics for communication patterns
communication_metrics = {
    "api_request_duration": "histogram",
    "message_queue_depth": "gauge",
    "circuit_breaker_state": "gauge",
    "saga_completion_rate": "counter",
    "grpc_request_count": "counter",
    "websocket_connections": "gauge"
}
```