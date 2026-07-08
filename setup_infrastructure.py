"""Create storage directories"""

import os
from pathlib import Path

# Create storage structure
storage_dirs = [
    "storage/logs",
    "storage/memory",
    "storage/configs",
    "storage/staging",
]

for dir_path in storage_dirs:
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {dir_path}")

print("\n✅ Storage structure initialized!")
