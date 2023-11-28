import re
import subprocess
import time

##################################################################################################################
# EDIT THESE THREE LINES
threshold_num = 3 # Number of failed login attempts before lockout.
threshold_minutes = 5 # Time in minutes to check back for failed login attempts. 
lockout_minutes = 1 # Time in minutes for lockout after threshhold_num failed login attempts.
##################################################################################################################

lockout_time = lockout_minutes * 30

log_file_path = "/var/log/auth.log"

banned_users = {}
cantBan = {}

while True:
    # Read the contents of the log file.
    with open(log_file_path, 'r') as file:
        log_text = file.read()

    with open(log_file_path, 'r') as file:
        lines = file.readlines()

    last_line = lines[-1]

    # Extract the time from the last line.
    curr_time_match = re.search(r' (\d+:\d+)', last_line)

    if curr_time_match:
        curr_time = curr_time_match.group(1)

        # Extract hour and minute.
        hour, minute = map(int, curr_time.split(':'))

        cutoff = minute - threshold_minutes
    else:
        print("Time not found in the last line.")

    # Segregate text by date.
    date_match = re.search(r'Nov (\d+)', last_line)

    if date_match:
        date = int(date_match.group(1))
    
    time_pattern = rf'Nov {date:d}'

    found_line = False
    restartLoop = False
    while True:
        for line in lines:
            if re.search(time_pattern, line):
                start_index = lines.index(line)
                found_line = True
                break
        if (found_line):
            break
        restartLoop = True
        break

    if restartLoop:
        continue

    lines = lines[start_index:]
        
    # Segregate text by time.
    time_pattern = rf' (\d+:{cutoff:02d})'

    found_line = False
    while True:
        for line in lines:
            if re.search(time_pattern, line):
                found_line = True
                start_index = lines.index(line)
                break
        if found_line:
            break
        else:
            cutoff = cutoff - 1
            time_pattern = rf' (\d+:{cutoff:02d})'

    log_text = ''.join(lines[start_index:])

    # Define a regular expression pattern to match authentication failure and username.
    pattern = r'(?:authentication failure|PAM (\d+) more authentication failures);.*user=([^\s]+)'

    matches = re.findall(pattern, log_text)

    # Create a dictionary to store the count for each username.
    username_count = {}

    # Iterate through matches and update the count for each username.
    for count_str, username in matches:
        count = int(count_str) if count_str.isdigit() else 1
        
        if username in username_count:
            username_count[username] += count
        else:
            username_count[username] = count

    # Use a set to get unique usernames.
    unique_usernames = set(username_count.keys())

    # Ban necessary users.
    if unique_usernames:
        for username in unique_usernames:
            count = username_count[username]
            if count >= threshold_num and (username not in banned_users) and (username not in cantBan):
                print(f"{username} failed a login {count} times.")
                print(f"{username} has been locked out for {lockout_time} seconds!")
                subprocess.run(['sudo', '/usr/sbin/usermod', '--lock', username])
                banned_users[username] = time.time()
                cantBan[username] = time.time()
    else:         
        continue

    current_time = time.time()
    for username, ban_time in list(cantBan.items()):
        if (current_time - ban_time) > lockout_time and (username in banned_users) and (username in cantBan):
            cantBan[username] = time.time()
            subprocess.run(['sudo', '/usr/sbin/usermod', '--unlock', username])
            print(f"{username} was unblocked!")
            del banned_users[username]

        # Remove the user from the banned list after being unbanned for 60 seconds.
        if (current_time - cantBan[username]) > 60:
            print("60 seconds have passed! User can be banned again.")
            del cantBan[username]