## claude code
### about
- https://www.anthropic.com/claude-code
- https://docs.anthropic.com/en/home
- AI model by Anthropic, accessible via API calls  
- hosted by Anthropic or third-party providers like AWS Bedrock

### install
- install plugin : visual studio + vscode
- `npm install -g @anthropic-ai/claude-code`
- buy credit

### Use it (chat)
#### 1 prompt in terminal 
- claude

#### 2 prompt in web console
- https://console.anthropic.com/dashboard
- developer interface for building applications with Claude programmatically

#### 3 programmatically prompt

```python

# ✅=== Using Anthropic’s Official Python SDK ===

import anthropic
client = anthropic.Anthropic(api_key="your_api_key_here")
response = client.messages.create(
    model="claude-3-opus-20240229",  # or other Claude 3 models
    max_tokens=1000,
    messages=[{"role": "user", "content": "Explain JWT in simple terms"}],
)
print(response.content)

```

```python

# ✅=== Using Claude via AWS Bedrock ===

import boto3
client = boto3.client("bedrock-runtime", region_name="us-east-1")  # Adjust region
body = {
    "messages": [{"role": "user", "content": "Explain JWT in simple terms"}],
    "max_tokens": 1000,
}
response = client.invoke_model(
    modelId="anthropic.claude-3-sonnet-20240229",  # or other Claude models
    body=json.dumps(body),
    contentType="application/json",
)
print(response["body"].read())

```