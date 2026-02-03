import os

commands = [
    "ruff check . --fix",
    "ruff format .",
]

for cmd in commands:
    print(f"👉 Running: {cmd}")
    os.system(cmd)
