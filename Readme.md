# Keylogger Project

IThis is a Keylogger tool that security analysts could use to understand how keylogging strokes works and enhance forensic analysis techniques. It logs keystrokes and saves them to a file.

## Installation

### Prerequisites

Ensure you have Python 3 and pip installed on your Kali Linux system.

1. Open a terminal and update your package list:
    ```bash
    sudo apt update
    ```

2. Install Python 3 and pip if they are not already installed:
    ```bash
    sudo apt install python3 python3-pip
    ```

### Installing the Keylogger

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/keylogger_project.git
    cd keylogger_project
    ```

2. Make the `install.sh` script executable:
    ```bash
    chmod +x install.sh
    ```

3. Run the `install.sh` script to install the keylogger package:
    ```bash
    sudo ./install.sh
    ```

This script will copy the necessary files to `/opt/keylogger_project` and install the package using `pip`.

## Usage

### Running the Keylogger

1. Open a terminal.

2. Run the keylogger:
    ```bash
    keylogger
    ```

### Starting and Stopping Logging

Once the keylogger is running, you can use the following commands:

- To start logging keystrokes:
    ```bash
    Enter 'start' to start logging
    ```

- To stop logging keystrokes:
    ```bash
    Enter 'stop' to stop logging
    ```

- To exit the keylogger:
    ```bash
    Enter 'exit' to exit
    ```

### Saving Log Files

When you stop logging, you will be prompted to enter the directory path and filename to save the log file. The script ensures that the log file has write permissions restricted to the owner.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This keylogger is intended for educational purposes only. Unauthorized use of this software to capture keystrokes without permission is illegal and unethical. Use it responsibly and with permission from the owner of the system.
