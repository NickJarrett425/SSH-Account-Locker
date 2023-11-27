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

# Use a set to get unique usernames
unique_usernames = set(matches)

# Print the formatted failure message for each unique username
if unique_usernames:
    for username in unique_usernames:
        print(f"{username} failed a login {matches.count(username)} times.")
else:
    print("No authentication failures found in the log file.")