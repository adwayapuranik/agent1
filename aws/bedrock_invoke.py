import boto3
import json


def invoke_model(prompt, config):
    client = boto3.client(
        "bedrock-runtime",
        region_name=config["model"]["aws_region"]
    )
    
    model_id = config["model"]["id"]
    
    body = {
        "messages": [
            {"role": "user", "content": [{"text": prompt}]}
        ],
        "inferenceConfig": {
            "max_new_tokens": config["model"]["max_tokens"],
            "temperature": config["model"]["temperature"],
            "topP": 0.1,
            "stopSequences": []
        }
    }
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    response_body = json.loads(response["body"].read())
    return response_body["output"]["message"]["content"][0]["text"]