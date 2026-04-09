import boto3
import json


def invoke_model(prompt, config):
    client = boto3.client(
        "bedrock-runtime",
        region_name=config["model"]["aws_region"]
    )
    
    model_id = config["model"]["id"]
    
    if "anthropic" in model_id:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": config["model"]["max_tokens"],
            "temperature": config["model"]["temperature"],
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"]
    
    elif "amazon.nova" in model_id:
        body = {
            "messages": [
                {"role": "user", "content": [{"text": prompt}]}
            ],
            "inferenceConfig": {
                "max_new_tokens": config["model"]["max_tokens"],
                "temperature": config["model"]["temperature"]
            }
        }
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        response_body = json.loads(response["body"].read())
        return response_body["output"]["message"]["content"][0]["text"]
    
    else:
        raise ValueError(f"Unsupported model: {model_id}")