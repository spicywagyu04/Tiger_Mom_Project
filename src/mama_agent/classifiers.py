from mama_agent import constants, llm

def classify_screenshot(image_path: str):
    """
    Classify the screenshot using the GPT-4O model with vision capabilities.
    """
    response = llm.generate_image_to_text(model_id=constants.MODEL_ID, 
                               system_prompt=constants.SYS_SINGLE_PROMPT, 
                               input_image_path=image_path)
    return response

def classify_focus(classification: str, task: str, distractions):
    """
    Classify whether or not the user is still focused on their task based on a given
    screenshot classification, the user's task, and the user's common distractions
    """
    distraction_string = "\n".join(f"- {item}" for item in distractions)
    user_query = classification + "\n\ntask: " + task + "\n\ndistractions:\n" + distraction_string
    response = llm.generate_response(model_id="gpt-4o-mini", 
                                     system_prompt=constants.SYS_FOCUS_PROMPT,
                                     user_input=user_query)
    
    return response
