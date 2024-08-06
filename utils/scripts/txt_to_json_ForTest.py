import pprint
import json

test_data = []
title = None
label = None

# Open the file for reading
with open('datasets/clean/benchmark_data.txt', 'r') as f:
    lines = [line.strip() for line in f if line.strip()]  # Read and strip empty lines

# Iterate through the cleaned lines
i = 0
while i < len(lines):
    line = lines[i]

    # Check if the line starts with "--", which indicates a title
    if line.startswith("--"):
        title = line.replace("--", "").strip()  # Store the title (excluding "--")
        i += 1

        # Ensure there is a next line for the label
        if i < len(lines):
            label = int(lines[i][9])  # Store the label
            i += 1

            # Process content lines
            while i < len(lines) and not lines[i].startswith("--"):
                content = lines[i].strip()
                if content:  # Ignore empty content lines
                    test_data.append({
                        "content": content,
                        "type": title,
                        "label": label,
                    })
                i += 1
        else:
            break
    else:
        i += 1


with open("datasets/clean/test.json", "w") as jsonFile:
  json.dump(test_data, jsonFile, indent=4)
  print("Done!")