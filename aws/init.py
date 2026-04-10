import boto3
import json
import os

client = boto3.client("bedrock-runtime", region_name="us-east-1")


def invoke_model(prompt, model_id, temperature=0.3, max_tokens=1000):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )

    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]