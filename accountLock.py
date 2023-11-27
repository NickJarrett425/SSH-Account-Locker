import re

# Specify the path to your log file
log_file_path = "auth.txt"

# Read the contents of the log file
with open(log_file_path, 'r') as file:
    log_text = file.read()

# Define a regular expression pattern to match the authentication failure and username
pattern = r'authentication failure;.*user=([^\s]+)'

# Use re.findall to find all matches in the text
matches = re.findall(pattern, log_text)

# Print the usernames for each authentication failure
if matches:
    for username in matches:
        print("Username:", username)
else:
    print("No authentication failures found in the log file.")
