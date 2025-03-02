import os 
import re

file = "blue-star-ltdannual-report-2023-24-analysis.md"

def cleanup(file):
    # First read the content
    with open(file, "r") as f:
        content = f.read()

    # Count original lines
    original_lines = len(content.splitlines())
    print(f"Original line count: {original_lines}")

    # Filter out lines containing "<!-- image -->"
    content = '\n'.join(line for line in content.splitlines() 
                                if "<!-- image -->" not in line)

    content = '\n'.join(line for line in content.splitlines() 
                                if "<unknown>" not in line)

    # Filter out lines containing "thank you" (case insensitive)
    content = '\n'.join(line for line in content.splitlines() 
                                if not re.search(r'thank\s*you', line, re.IGNORECASE))

    # Remove phone numbers (common formats)
    content = re.sub(r'\+?[\d\s\(\)\-\.]{10,}', '', content)

    # Remove lines with less than 3 characters
    content = '\n'.join(line for line in content.splitlines() 
                                if len(line.strip()) >= 3)

    # Remove navigation elements and page numbers
    content = re.sub(r'Company Overview[^\n]+\n+', '', content)
    content = re.sub(r'Notice \(Contd\.\)', '', content)
    content = re.sub(r'\| \d+ \|', '', content)

    # Remove corporate information section at the end
    content = re.sub(r'## CORPORATE INFORMATION[\s\S]+$', '', content)

    # Remove excessive whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Remove notice section which is not relevant for analysis
    content = re.sub(r'## NOTICE[\s\S]+?## STATEMENT PURSUANT TO SECTION 102\(1\) OF THE COMPANIES ACT, 2013', '', content)
    content = re.sub(r'## STATEMENT PURSUANT TO SECTION 102\(1\) OF THE COMPANIES ACT, 2013[\s\S]+?(?=## )', '', content)

    # Remove annexures
    content = re.sub(r'## ANNEXURE[\s\S]+?(?=## )', '', content)

    # Clean up table formatting
    content = re.sub(r'\|\s*\|\s*\|', '|', content)

    # Convert financial tables to a cleaner format
    # This is a more complex operation that may need customization based on your specific tables

    # Remove repetitive headers in tables
    content = re.sub(r'\| Particulars\| Particulars\|', '| Particulars |', content)

    # Clean up director information tables that aren't relevant for financial analysis
    content = re.sub(r'\|\s*Sr\.\s*No\.\s*\|[\s\S]+?(?=##)', '', content)

    # Remove auditor statements
    content = re.sub(r'As per our report of even date[\s\S]+?Date : May \d+, 2024', '', content)

    # Remove Meeting Notifications and Scrip Codes
    content = re.sub(r"(?s)Scrip Code:.*?Sub:.*?\n", "", content)

    # Remove Forward-looking statements and similar disclaimers
    content = re.sub(r"(?s)FORWARD-LOOKING STATEMENT.*?obligation to update.*?\n", "", content)

    # Remove Governance sections or legal boilerplate
    content = re.sub(r"(?s)Board of Directors.*?Financial Statements.*?\n", "", content)

    # Remove page contents or index
    content = re.sub(r"(?s)## Contents.*?## FORWARD-LOOKING STATEMENT", "", content)

    # Remove any duplicate line breaks
    content = re.sub(r"\n{2,}", "\n\n", content)

    # Count final lines
    final_lines = len(content.splitlines())
    print(f"Final line count: {final_lines}")
    print(f"Removed {original_lines - final_lines} lines")

    # Write back the filtered content
    with open(file, "w") as f:
        f.write(content)

    print(f"Successfully cleaned {file}")


import os
from collections import defaultdict

def check_similar_filenames(directory):
    # Store filenames by their first 10 characters
    prefix_map = defaultdict(list)
    
    # Walk through the directory
    for filename in os.listdir(directory):
        if filename.endswith('.md'):  # Only check markdown files
            # Get first 10 chars of filename
            prefix = filename[:5]
            prefix_map[prefix].append(filename)
    
    # Check for duplicates
    duplicates_found = False
    for prefix, filenames in prefix_map.items():
        if len(filenames) > 1:
            duplicates_found = True
            print(f"\nFiles starting with '{prefix}':")
            for fname in filenames:
                print(f"  - {fname}")
    
    if not duplicates_found:
        print("No files found with matching first 10 characters.")

if __name__ == "__main__":
    posts_dir = "content/posts"
    print(f"Checking files in {posts_dir}...")
    check_similar_filenames(posts_dir)