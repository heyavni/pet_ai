from modules.wake import listen_for_wake_word
from modules.recognize_speech import recognize_speech
from modules.recognize_speech import recognize_speech
from modules.command_parser import CommandParser

def main():
    command_parser = CommandParser()

    while True:

        print("Waiting for wake word...")

        if listen_for_wake_word():  # Detect the wake word

            print("Listening for speech...")

            speech = recognize_speech()  # Start recognizing speech after the wake word

            if speech:

                print(f"Recognized speech: {speech}")

                # Parse the command
                parsed_command = command_parser.parse_command(speech)

                # Print the matched command details
                print(f"Matched Category: {parsed_command['category']}")
                print(f"Matched Pattern: {parsed_command.get('matched_pattern', 'N/A')}")
                
                # Respond
                if parsed_command['response']:
                    print(parsed_command['response'])
                
                # Execute any associated action
                action_result = command_parser.execute_action(parsed_command)

                # Explicitly print the action result for time commands
                if action_result:
                    print(action_result)
                
                # Check for system exit
                if action_result == "exit":
                    break
                # execute_action(speech)
            else:
                print("No speech recognized.")

if __name__ == "__main__":
    main()


