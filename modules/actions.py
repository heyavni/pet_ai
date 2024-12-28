import threading
import datetime
from pet_animation import perform_action

# Global variables to manage actions
current_action_thread = None
stop_event = threading.Event()
window_instance = None

def set_window_instance(window):
    """Set the window instance for animations"""
    global window_instance
    window_instance = window
    print(f"DEBUG: Actions module - Window instance set: {window_instance is not None}")

def stop_current_action():
    """Stop any currently running action"""
    global current_action_thread, stop_event
    if current_action_thread and current_action_thread.is_alive():
        print("DEBUG: Stopping current action")
        stop_event.set()
        current_action_thread.join()
        stop_event.clear()

def start_new_action(action):
    """Start a new action"""
    global current_action_thread, stop_event, window_instance
    
    if window_instance is None:
        print("DEBUG: Error - Window instance not set in actions module")
        return False

    print(f"DEBUG: Starting new action: {action}")
    # Stop current action if any
    stop_current_action()
    
    # Start new action
    stop_event.clear()
    try:
        current_action_thread = threading.Thread(
            target=perform_action,
            args=(window_instance, action, stop_event),
            daemon=True
        )
        current_action_thread.start()
        return True
    except Exception as e:
        print(f"DEBUG: Error starting action: {e}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return False

def _exit_system():
    """Handle system exit"""
    stop_current_action()
    print("DEBUG: Executing exit command")
    return "exit"

def _get_current_time():
    """Get the current time"""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"

def _happy():
    """Make the dog happy"""
    print("DEBUG: Executing happy command")
    if start_new_action("happy"):
        return "Making the dog happy!"
    return "Failed to make the dog happy - window not initialized"

def _walk():
    """Make the dog walk"""
    print("DEBUG: Executing walk command")
    if start_new_action("walk"):
        return "The dog is walking!"
    return "Failed to make the dog walk - window not initialized"

def _run():
    """Make the dog run"""
    print("DEBUG: Executing run command")
    if start_new_action("run"):
        return "The dog is running!"
    return "Failed to make the dog run - window not initialized"

def _sit():
    """Make the dog sit"""
    print("DEBUG: Executing sit command")
    if start_new_action("sit"):
        return "The dog is sitting!"
    return "Failed to make the dog sit - window not initialized"

def _stand():
    """Make the dog stand"""
    print("DEBUG: Executing stand command")
    if start_new_action("stand"):
        return "The dog is standing!"
    return "Failed to make the dog stand - window not initialized"

def _sleep():
    """Make the dog sleep"""
    print("DEBUG: Executing sleep command")
    if start_new_action("sleep"):
        return "The dog is sleeping!"
    return "Failed to make the dog sleep - window not initialized"