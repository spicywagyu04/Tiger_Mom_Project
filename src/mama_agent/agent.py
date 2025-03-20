import json

def is_focused(file_path="./history/focus_history.jsonl"):
    """
    Reads the last three JSON objects from a JSONL file and returns True
    if the 'focus_status' field is "true" (case-sensitive) for all three objects.
    Otherwise, it returns False.
    """
    all_records = []
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    json_obj = json.loads(line)
                    all_records.append(json_obj)
                except json.JSONDecodeError:
                    continue

    if len(all_records) < 3:
        return True

    last_three = all_records[-3:]
    return any(
        obj.get("focus_status", "").strip().lower() == "true" 
        for obj in last_three
    )
