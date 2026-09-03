import os
import random
import subprocess
from datetime import datetime, timedelta

def run_cmd(cmd, env=None):
    subprocess.run(cmd, shell=True, env=env, check=True)

# Generate commits over the last 365 days
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

print("Generating GitHub contribution history with CORRECT timestamps...")

current_date = start_date
total_commits = 0

with open(".activity", "w") as f:
    f.write("Activity log\n")

while current_date <= end_date:
    if random.random() < 0.75:
        num_commits = random.randint(1, 5)
        for _ in range(num_commits):
            hour = random.randint(9, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            commit_time = current_date.replace(hour=hour, minute=minute, second=second)
            
            # Use strict Git timestamp format: "<unix_timestamp> <timezone_offset>"
            unix_ts = int(commit_time.timestamp())
            date_str = f"{unix_ts} +0000"
            
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str
            
            with open(".activity", "a") as f:
                f.write(f"Commit at {unix_ts}\n")
            
            run_cmd('git add .activity', env=env)
            run_cmd('git commit -m "Activity contribution"', env=env)
            total_commits += 1

    current_date += timedelta(days=1)

print(f"Done! Generated {total_commits} commits.")
