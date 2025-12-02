def count_log_messages(logfile_path):
    # Dictionary to keep track of the message counts
    messages = {
        "ST code Compilation success, waiting for validation": 0,
        "ST code generation failed": 0,
        "SMV code compilation failed": 0,
        "SMV Validation failed": 0,
        "SMV Validation successful": 0
    }

    # Try to open and read the logfile
    try:
        with open(logfile_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Increment the count for each message found in the line
                for message in messages:
                    if message in line:
                        messages[message] += 1
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    # Print the results
    for message, count in messages.items():
        print(f"{message}: {count}")

def main():
    # Ask the user to enter the log file path
    log_file_path = input("Enter the path to your log file: ")
    # Call the function to count messages in the log file
    count_log_messages(log_file_path)

if __name__ == "__main__":
    main()
