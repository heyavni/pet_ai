import threading
import sys
import os
import time
import queue
from modules.wake import listen_for_wake_word
from modules.recognize_speech import recognize_speech
from modules.command_parser import CommandParser
from pet_animation import FloatingDogWindow, perform_action, dog_sprints

# Path to the initial dog image
dog_image_path = "/Users/avnisoni/pup_ai/resources/sprints/sprint4.png"

def main():
    print("\nDEBUG: Application startup sequence")
    print(f"DEBUG: Current working directory: {os.getcwd()}")
    print(f"DEBUG: Initial image path: {dog_image_path}")
    print(f"DEBUG: Image exists: {os.path.exists(dog_image_path)}")
    
    try:
        print("\nDEBUG: Initializing components")
        command_parser = CommandParser()
        
        print("DEBUG: Creating FloatingDogWindow")
        floating_window = FloatingDogWindow.alloc().initWithImagePath_(dog_image_path)
        if floating_window is None:
            print("DEBUG: Failed to create FloatingDogWindow")
            return

        print("DEBUG: Starting window initialization")
        
        # Create a queue for commands
        command_queue = queue.Queue()
        
        # Create a thread for handling commands
        def command_handler():
            while True:
                try:
                    stop_event = threading.Event()
                    current_action_thread = None
                    
                    print("\nDEBUG: Waiting for wake word")
                    wake_word = input()
                    
                    if wake_word.lower() == "hey pup":
                        print("DEBUG: Wake word detected")
                        speech = input()
                        
                        if speech:
                            command_queue.put(speech)
                except Exception as e:
                    print(f"DEBUG: Error in command handler: {e}")

        # Start command handler thread
        command_thread = threading.Thread(target=command_handler, daemon=True)
        command_thread.start()

        # Run the window and event loop on the main thread
        floating_window.run()
        
    except Exception as e:
        print(f"DEBUG: Critical error in main: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()


# def main():
#     command_parser = CommandParser()

#     while True:

#         print("Waiting for wake word...")

#         if listen_for_wake_word():  # Detect the wake word

#             print("Listening for speech...")

#             speech = recognize_speech()  # Start recognizing speech after the wake word

#             if speech:

#                 print(f"Recognized speech: {speech}")

#                 # Parse the command
#                 parsed_command = command_parser.parse_command(speech)

#                 # Print the matched command details
#                 print(f"Matched Category: {parsed_command['category']}")
#                 print(f"Matched Pattern: {parsed_command.get('matched_pattern', 'N/A')}")
                
#                 # Respond
#                 if parsed_command['response']:
#                     print(parsed_command['response'])
                
#                 # Execute any associated action
#                 action_result = command_parser.execute_action(parsed_command)

#                 # Explicitly print the action result for time commands
#                 if action_result:
#                     print(action_result)
                
#                 # Check for system exit
#                 if action_result == "exit":
#                     break
#                 # execute_action(speech)
#             else:
#                 print("No speech recognized.")

# if __name__ == "__main__":
#     main()


