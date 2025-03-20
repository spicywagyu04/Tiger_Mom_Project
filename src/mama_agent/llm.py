from openai import OpenAI
import base64

def encode_image(image_path):
    """
    Encode an image file in Base64.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def extract_json(json_data):
    """
    Extracts actual JSON content of an AI-generated JSON data delimited by ```json ```.
    """
    response = json_data.strip('` \n')

    if response.startswith('json'):
        response = response[4:]
        
    return response
    
def generate_image_to_text(model_id: str, system_prompt: str, input_image_path: str, json_output=True):
    """
    Reusable function for text generation from image inputs.
    Returns LLM image analysis response.
    """
    base64_image = encode_image(input_image_path)
    
    # messages payload
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
            "response_format": {"type": "json_object"}
        },
    ]

    # LLM inference
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=300,
        )
        result = response.choices[0].message.content
        
        if json_output:
            result = extract_json(result)
            
        return result
    except Exception as e:
        print("Error during classification:", e)
        
def generate_response(model_id: str, system_prompt: str, user_input: str, json_output=True):
    """
    Reusable function for traditional text completion tasks.
    Returns text response.
    """
    
    # messages payload
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_input,
            "response_format": {"type": "json_object"}
        },
    ]

    # LLM inference
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=300,
        )
        result = response.choices[0].message.content
        
        if json_output:
            result = extract_json(result)
            
        return result
    except Exception as e:
        print("Error during classification:", e)
        