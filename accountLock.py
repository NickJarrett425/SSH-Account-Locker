import re

log_text = "Nov 27 15:03:14 VM sshd[3129]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=10.0.2.6  user=seed"

# Define a regular expression pattern to match the username
pattern = r'user=([^ ]+)'

# Use re.search to find the pattern in the text
match = re.search(pattern, log_text)

# Extract the username if a match is found
if match:
    username = match.group(1)
    print("Username:", username)
else:
    print("Username not found in the log text.")
