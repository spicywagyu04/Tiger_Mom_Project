import json

def append_jsonl(result, timestamp, file_path):
    """
    result: Must be JSON format
    Writes new screenshot classification to screenshot history file
    """
    if isinstance(result, str):
        result = json.loads(result)
        
    result_with_timestamp = {
        "timestamp": timestamp,
        **result
    }
    with open(file_path, 'a') as f:
        f.write(json.dumps(result_with_timestamp) + "\n")
