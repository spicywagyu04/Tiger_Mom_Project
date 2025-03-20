# process.py
from capture import screenshots
from mama_agent import classifiers, agent
from history import history_write

def process_screenshot(timestamp, user_task, distractions):
    # Take a screenshot and save it.
    screenshots.capture_screenshot()
    path = "./capture/screenshots/screenshot.png"
    
    # Classify screenshot content.
    screenshot_classification = classifiers.classify_screenshot(image_path=path)
    history_write.append_jsonl(result=screenshot_classification,
                               timestamp=timestamp,
                               file_path="./history/screenshot_history.jsonl")
    print("screenshot_classification:", screenshot_classification)
    
    # Classify whether the user is focused on the given task, passing distractions
    focus_classification = classifiers.classify_focus(classification=screenshot_classification, 
                                                      task=user_task,
                                                      distractions=distractions)
    history_write.append_jsonl(result=focus_classification,
                               timestamp=timestamp,
                               file_path="./history/focus_history.jsonl")
    print("focus_classification:", focus_classification)
    
    # Mama agent checks the focus status based on recent screenshots.
    locked_in = agent.is_focused()
    
    # Instead of printing a message, we return the focus status.
    return locked_in