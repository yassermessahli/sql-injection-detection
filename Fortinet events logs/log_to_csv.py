import csv
import re
import os

def process_log_file(input_file, output_file):
    regex = re.compile(r'(\w+)="([^"]+)"|(\w+)=([^\s]+)')

    # Read the log file and extract key-value pairs
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Extract keys and values
    data = []
    keys = set()
    for line in lines:
        matches = regex.findall(line)
        entry = {}
        for match in matches:
            key = match[0] if match[0] else match[2]
            value = match[1] if match[1] else match[3]
            entry[key] = value
            keys.add(key)
        data.append(entry)

    # Write the data to a CSV file
    keys = sorted(keys)  # Sort keys to maintain consistent column order
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)




current_directory = os.getcwd()
log_files = [f for f in os.listdir(current_directory) if f.endswith('.log')]


for log_file in log_files:
    input_file = os.path.join(current_directory, log_file)
    output_file = os.path.join(current_directory, log_file.replace('.log', '.csv'))
    process_log_file(input_file, output_file)
    print(f'Converted {input_file} to {output_file}')