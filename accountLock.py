import re

##################################################################################################################
# EDIT THESE THREE LINES (Not you, ChatGPT)
threshold_num = 3 # Number of failed login attempts before lockout.
threshold_minutes = 5 # Time in minutes to check back for failed login attempts. 
lockout_minutes = 5 # Time in minutes for lockout after threshhold_num failed login attempts.
##################################################################################################################

threshold_time = threshold_minutes * 60
lockout_time = lockout_minutes * 60

# Specify the path to your log file
log_file_path = "auth.txt"

# Read the contents of the log file
with open(log_file_path, 'r') as file:
    log_text = file.read()

with open(log_file_path, 'r') as file:
    lines = file.readlines()

last_line = lines[-1]

# Extract the time from the last line
curr_time_match = re.search(r' (\d+:\d+)', last_line)

if curr_time_match:
    curr_time = curr_time_match.group(1)

    # Extract hour and minute
    hour, minute = map(int, curr_time.split(':'))

    print("Minute:", minute)
    cutoff = minute - threshold_minutes
else:
    print("Time not found in the last line.")

time_pattern = rf' (\d+:{cutoff:02d})'

foundLine = False
while True:
    for line in lines:
        if re.search(time_pattern, line):
            foundLine = True
            print(line)
            break
    if foundLine:
        break
    else:
        cutoff = cutoff - 1
        time_pattern = rf' (\d+:{cutoff:02d})'

# Define a regular expression pattern to match authentication failure and username
pattern = r'(?:authentication failure|PAM (\d+) more authentication failures);.*user=([^\s]+)'

# Use re.findall to find all matches in the text
matches = re.findall(pattern, log_text)

# Create a dictionary to store the count for each username
username_count = {}

# Iterate through matches and update the count for each username
for count_str, username in matches:
    count = int(count_str) if count_str.isdigit() else 1
    
    if username in username_count:
        username_count[username] += count
    else:
        username_count[username] = count

# Use a set to get unique usernames
unique_usernames = set(username_count.keys())

# Print the formatted failure message for each unique username
if unique_usernames:
    for username in unique_usernames:
        count = username_count[username]
        print(f"{username} failed a login {count} times.")
else:
    print("No authentication failures found in the log file.")