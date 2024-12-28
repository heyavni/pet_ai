import threading
import sys
import os
import time
import queue
from modules.wake import listen_for_wake_word
from modules.recognize_speech import recognize_speech
from modules.command_parser import CommandParser
from modules import actions  # Import actions module
from pet_animation import FloatingDogWindow, perform_action, dog_sprints, validate_image_path

# Path to the initial dog image
dog_image_path = "/Users/avnisoni/pup_ai/resources/sprints/sprint4.png"

def main():
    print("\nDEBUG: Application startup sequence")
    print(f"DEBUG: Current working directory: {os.getcwd()}")
    print(f"DEBUG: Initial image path: {dog_image_path}")
    print(f"DEBUG: Image exists: {os.path.exists(dog_image_path)}")
    
    try:
        print("\nDEBUG: Initializing components")
        
        print("DEBUG: Creating FloatingDogWindow")
        floating_window = FloatingDogWindow.alloc().initWithImagePath_(dog_image_path)
        if floating_window is None:
            print("DEBUG: Failed to create FloatingDogWindow")
            return

        print("DEBUG: Setting window instance in actions module")
        actions.set_window_instance(floating_window)
        
        print("DEBUG: Creating CommandParser")
        command_parser = CommandParser()
        
        print("DEBUG: Starting window initialization")
        
        # Create a queue for commands
        command_queue = queue.Queue()
        
        # Create a thread for handling commands
        def command_handler():
            while True:
                try:
                    print("\nDEBUG: Waiting for wake word")
                    wake_word = input()
                    
                    if wake_word.lower() == "hey pup":
                    # if listen_for_wake_word():
                        print("DEBUG: Wake word detected")
                        
                        # Show happy animation
                        happy_path = "/Users/avnisoni/pup_ai/resources/sprints/sprint1.png"
                        if validate_image_path(happy_path):
                            # Update image on main thread
                            floating_window.updateImage_(happy_path)
                            
                            # Stay happy for 1 second
                            time.sleep(0.5)
                            
                            # Return to standing position
                            stand_path = "/Users/avnisoni/pup_ai/resources/sprints/sprint4.png"
                            if validate_image_path(stand_path):
                                floating_window.updateImage_(stand_path)
                        
                        # Get the voice command
                        speech = recognize_speech() 
                        print(f"DEBUG: Recognized speech: {speech}")
                        if speech:
                            command_queue.put(speech)

                            # Parse the command
                            parsed_command = command_parser.parse_command(speech)

                            # Print the matched command details
                            print(f"DEBUG: Matched Category: {parsed_command['category']}")
                            print(f"DEBUG: Matched Pattern: {parsed_command.get('matched_pattern', 'N/A')}")
                            
                            # Respond
                            if parsed_command['response']:
                                print(parsed_command['response'])
                            
                            # Execute any associated action
                            action_result = command_parser.execute_action(parsed_command)

                            # Explicitly print the action result
                            if action_result:
                                print(f"DEBUG: Action result: {action_result}")
                            
                            # Check for system exit
                            if action_result == "exit":
                                break
                        else:
                            print("DEBUG: No speech recognized.")

                except Exception as e:
                    print(f"DEBUG: Error in command handler: {e}")
                    import traceback
                    print(f"DEBUG: Traceback: {traceback.format_exc()}")

        # Start command handler thread
        print("DEBUG: Starting command handler thread")
        command_thread = threading.Thread(target=command_handler, daemon=True)
        command_thread.start()

        print("DEBUG: Running window event loop")
        # Run the window and event loop on the main thread
        floating_window.run()
        
    except Exception as e:
        print(f"DEBUG: Critical error in main: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()

# import threading
# import sys
# import os
# import time
# import queue
# from modules.wake import listen_for_wake_word
# from modules.recognize_speech import recognize_speech
# from modules.command_parser import CommandParser
# from pet_animation import FloatingDogWindow, perform_action, dog_sprints, validate_image_path

# # Path to the initial dog image
# dog_image_path = "/Users/avnisoni/pup_ai/resources/sprints/sprint4.png"

# def main():
#     print("\nDEBUG: Application startup sequence")
#     print(f"DEBUG: Current working directory: {os.getcwd()}")
#     print(f"DEBUG: Initial image path: {dog_image_path}")
#     print(f"DEBUG: Image exists: {os.path.exists(dog_image_path)}")
    
#     try:
#         print("\nDEBUG: Initializing components")
#         command_parser = CommandParser()
        
#         print("DEBUG: Creating FloatingDogWindow")
#         floating_window = FloatingDogWindow.alloc().initWithImagePath_(dog_image_path)
#         if floating_window is None:
#             print("DEBUG: Failed to create FloatingDogWindow")
#             return

#         print("DEBUG: Starting window initialization")
        
#         # Create a queue for commands
#         command_queue = queue.Queue()
        
#         # Create a thread for handling commands
#         def command_handler():
#             while True:
#                 try:
#                     print("\nDEBUG: Waiting for wake word")
#                     wake_word = input()
                    
#                     if wake_word.lower() == "hey pup":
#                     # if listen_for_wake_word():
#                         print("DEBUG: Wake word detected")
                        
#                         # Show happy animation
#                         happy_path = "/Users/avnisoni/pup_ai/resources/sprints/sprint1.png"
#                         if validate_image_path(happy_path):
#                             # Update image on main thread
#                             floating_window.updateImage_(happy_path)
                            
#                             # Stay happy for 1 second
#                             time.sleep(0.5)
                            
#                             # Return to standing position
#                             stand_path = "/Users/avnisoni/pup_ai/resources/sprints/sprint4.png"
#                             if validate_image_path(stand_path):
#                                 floating_window.updateImage_(stand_path)
                        
#                         # Get the voice command
#                         speech = recognize_speech() 
#                         print(speech)
#                         if speech:
#                             command_queue.put(speech)

#                             # Parse the command
#                             parsed_command = command_parser.parse_command(speech)
#                             print(speech)

#                             # Print the matched command details
#                             print(f"Matched Category: {parsed_command['category']}")
#                             print(f"Matched Pattern: {parsed_command.get('matched_pattern', 'N/A')}")
                            
#                             # Respond
#                             if parsed_command['response']:
#                                 print(parsed_command['response'])
                            
#                             # Execute any associated action
#                             action_result = command_parser.execute_action(parsed_command)

#                             # Explicitly print the action result for time commands
#                             if action_result:
#                                 print(action_result)
                            
#                             # Check for system exit
#                             if action_result == "exit":
#                                 break
#                             # execute_action(speech)
#                         else:
#                             print("No speech recognized.")

#                 except Exception as e:
#                     print(f"DEBUG: Error in command handler: {e}")

#         # Start command handler thread
#         command_thread = threading.Thread(target=command_handler, daemon=True)
#         command_thread.start()

#         # Run the window and event loop on the main thread
#         floating_window.run()
        
#     except Exception as e:
#         print(f"DEBUG: Critical error in main: {str(e)}")
#         import traceback
#         print(f"DEBUG: Traceback: {traceback.format_exc()}")
#         raise

# if __name__ == "__main__":
#     main()


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


