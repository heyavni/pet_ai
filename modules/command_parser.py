import re
import json
import os
import modules.actions as actions

class CommandParser:
    def __init__(self, commands_file='commands.json'):
        self.commands_file = commands_file
        self.commands = self.load_commands()

    def load_commands(self):
        """
        Load commands from a JSON file, creating a default one if it doesn't exist.
        """
        default_commands = {
    "greetings": [
        {
            "patterns": ["hello", "hi", "hey"],
            "response": "Hello! How can I help you?"
        },
        {
            "patterns": ["how are you"],
            "response": "I'm doing well, thank you for asking!"
        }
    ],
    "system_commands": [
        {
            "patterns": ["exit", "quit", "goodbye"],
            "response": "Goodbye!",
            "action": "exit"
        },
        {
            "patterns": ["what can you do", "help"],
            "response": "I can help with various tasks. Just ask me something!"
        }
    ],
    "time_commands": [
        {
            "patterns": ["what time is it", "current time"],
            "action": "get_current_time"
        }
    ],
    "dog_commands": [
        {
            "patterns": ["happy", "be happy"],
            "action": "happy"
        },
        {
            "patterns": ["walk", "start walking"],
            "action": "walk"
        },
        {
            "patterns": ["run", "start running"],
            "action": "run"
        },
        {
            "patterns": ["sit", "take a seat"],
            "action": "sit"
        },
        {
            "patterns": ["stand", "stop"],
            "action": "stand"
        },
        {
            "patterns": ["sleep", "take a nap"],
            "action": "sleep"
        }
    ]
}


        # If commands file doesn't exist, create it
        if not os.path.exists(self.commands_file):
            with open(self.commands_file, 'w') as f:
                json.dump(default_commands, f, indent=4)
            return default_commands

        # Load existing commands
        try:
            with open(self.commands_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return default_commands

    def parse_command(self, text):
        """
        Parse the input text and match against known command patterns.
        
        Args:
            text (str): The input text to parse
        
        Returns:
            dict: A dictionary containing the matched command details
        """
        # Normalize the input text
        text = text.lower().strip()

        # Check through all command categories
        for category, commands in self.commands.items():
            for command in commands:
                # Check if any pattern matches
                for pattern in command.get('patterns', []):
                    if re.search(pattern, text):
                        return {
                            "category": category,
                            "matched_pattern": pattern,
                            "response": command.get('response', ''),
                            "action": command.get('action')
                        }

        # If no command is found
        return {
            "category": "unknown",
            "response": "I'm sorry, I didn't understand that command.",
            "action": None
        }

    def execute_action(self, command):
        """
        Execute the action associated with a command.
        
        Args:
            command (dict): The command dictionary from parse_command
        
        Returns:
            str or None: The result of the action or None
        """
        if not command or not command.get('action'):
            return None

        # Define action methods
        action_methods = {
            "exit": actions._exit_system,
            "get_current_time": actions._get_current_time,
            "happy": actions._happy,
            "walk": actions._walk,
            "run": actions._run,
            "sit": actions._sit,
            "stand": actions._stand,
            "sleep": actions._sleep
        }

        # Execute the corresponding action
        action_func = action_methods.get(command['action'])
        if action_func:
            return action_func()
        return None

# import re
# import json
# import os

# class CommandParser:
#     def __init__(self, commands_file='commands.json'):
#         self.commands_file = commands_file
#         self.commands = self.load_commands()

#     def load_commands(self):
#         """
#         Load commands from a JSON file, creating a default one if it doesn't exist.
#         """
#         default_commands = {
#             "greetings": [
#                 {"patterns": ["hello", "hi", "hey"], "response": "Hello! How can I help you?"},
#                 {"patterns": ["how are you"], "response": "I'm doing well, thank you for asking!"}
#             ],
#             "system_commands": [
#                 {"patterns": ["exit", "quit", "goodbye"], "response": "Goodbye!", "action": "exit"},
#                 {"patterns": ["what can you do", "help"], "response": "I can help with various tasks. Just ask me something!"}
#             ],
#             "time_commands": [
#                 {"patterns": ["what time is it", "current time"], "action": "get_current_time"}
#             ]
#         }

#         # If commands file doesn't exist, create it
#         if not os.path.exists(self.commands_file):
#             with open(self.commands_file, 'w') as f:
#                 json.dump(default_commands, f, indent=4)
#             return default_commands

#         # Load existing commands
#         try:
#             with open(self.commands_file, 'r') as f:
#                 return json.load(f)
#         except (json.JSONDecodeError, FileNotFoundError):
#             return default_commands

#     def parse_command(self, text):
#         """
#         Parse the input text and match against known command patterns.
        
#         Args:
#             text (str): The input text to parse
        
#         Returns:
#             dict: A dictionary containing the matched command details
#         """
#         # Normalize the input text
#         text = text.lower().strip()

#         # Check through all command categories
#         for category, commands in self.commands.items():
#             for command in commands:
#                 # Check if any pattern matches
#                 for pattern in command.get('patterns', []):
#                     if re.search(pattern, text):
#                         return {
#                             "category": category,
#                             "matched_pattern": pattern,
#                             "response": command.get('response', ''),
#                             "action": command.get('action')
#                         }

#         # If no command is found
#         return {
#             "category": "unknown",
#             "response": "I'm sorry, I didn't understand that command.",
#             "action": None
#         }

#     def execute_action(self, command):
#         """
#         Execute the action associated with a command.
        
#         Args:
#             command (dict): The command dictionary from parse_command
        
#         Returns:
#             str or None: The result of the action or None
#         """
#         if not command or not command.get('action'):
#             return None

#         # Define action methods
#         action_methods = {
#             "exit": self._exit_system,
#             "get_current_time": self._get_current_time
#         }

#         # Execute the corresponding action
#         action_func = action_methods.get(command['action'])
#         if action_func:
#             return action_func()
#         return None

#     def _exit_system(self):
#         """
#         Handle system exit.
#         """
#         print("Exiting the system...")
#         return "exit"

#     def _get_current_time(self):
#         """
#         Get the current time.
#         """
#         import datetime
#         current_time = datetime.datetime.now().strftime("%I:%M %p")
#         return f"The current time is {current_time}"
