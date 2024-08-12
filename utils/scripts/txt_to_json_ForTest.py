"""
Process benchmark data from a text file and converts it into a JSON file.
The input text file should follow a specific format with benchmark types, labels, and content lines.
The output JSON file will contain a list of dictionaries, each representing a content line with its associated type and label.

Input File Format:
------------------
-- Benchmark type 1 --
-- Label [l] --
Content line 1
Content line 2
...
-- Benchmark type 2 --
-- Label [l] --
Content line 1
Content line 2
...

Output JSON Format:
-------------------
[
    {
        "content": "Content line 1",
        "type": "Benchmark type 1",
        "label": l
    },
    {
        "content": "Content line 2",
        "type": "Benchmark type 1",
        "label": l
    },
    ...
]

Usage:
------
Ensure the input text file is located at 'datasets/clean/benchmark_data.txt'.
Run the script to generate 'datasets/clean/test.json'.
"""

import json

def process_benchmark_data(input_file, output_file):
    """
    Processes the benchmark data from the input text file and writes it to the output JSON file.

    Args:
        input_file (str): Path to the input text file containing benchmark data.
        output_file (str): Path to the output JSON file to write the processed data.
    """
    test_data = []
    title = None
    label = None

    # Open the file for reading
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]  # Read and strip empty lines

    # Iterate through the cleaned lines
    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if the line starts with "--", which indicates a title
        if line.startswith("--"):
            title = line.replace("--", "").strip()  # Store the clean title (excluding "--")
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

    # Save the data to a JSON file
    with open(output_file, "w") as jsonFile:
        json.dump(test_data, jsonFile, indent=4)
        print("Done!")

if __name__ == "__main__":
    input_file = 'datasets/clean/benchmark_data.txt'
    output_file = 'datasets/clean/test.json'
    process_benchmark_data(input_file, output_file)