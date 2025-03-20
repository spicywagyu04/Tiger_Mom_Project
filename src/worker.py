# worker.py
import time
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from process import process_screenshot

class Worker(QThread):
    log_signal = pyqtSignal(str)
    alert_signal = pyqtSignal(str)  # Signal for focus alerts
    
    def __init__(self, user_task, distractions, initial_delay=10):
        super().__init__()
        self.user_task = user_task
        self.distractions = distractions
        self.initial_delay = initial_delay  # Configurable initial delay in seconds
        self.running = True
    
    def run(self):
        # Log the start with the initial delay and interval information
        self.log_signal.emit(f"Starting screenshot capture every 10 seconds after an initial delay of {self.initial_delay} seconds.")
        
        # Implement the initial delay
        for _ in range(self.initial_delay):
            if not self.running:
                return  # Exit if stopped during the delay
            time.sleep(1)
        
        # Main screenshot capture loop
        while self.running:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            locked_in = process_screenshot(timestamp, self.user_task, self.distractions)
            self.log_signal.emit(f"Processed screenshot at {timestamp} for task: {self.user_task}")
            
            # If the user is not focused, emit an alert and stop
            if not locked_in:
                self.alert_signal.emit("LOCK IN SON!!!")
                self.running = False
                break
            
            # Sleep for 10 seconds between screenshots
            for _ in range(10):
                if not self.running:
                    break
                time.sleep(1)
    
    def stop(self):
        self.running = False
        self.wait()  # Wait for the thread to finish