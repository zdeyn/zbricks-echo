#!/usr/bin/env python3
import sys
import glob

def read_files(file_patterns):
    files = []
    for pattern in file_patterns:
        files.extend(glob.glob(pattern))
    
    for file in files:
        try:
            with open(file, 'r') as f:
                print(f"### {file} ###")
                print(f.read())
                print()  # Add a newline for separation between files
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"An error occurred while reading {file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python combine_files.py <file1> <file2> ...")
    else:
        read_files(sys.argv[1:])
