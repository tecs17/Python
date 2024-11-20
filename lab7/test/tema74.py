import sys
import os

if len(sys.argv) == 3:
    path = sys.argv[1]
    extension = sys.argv[2]
    print(f"path = {path}\nextension = {extension}")
else:
    print("insuficient arguments")
