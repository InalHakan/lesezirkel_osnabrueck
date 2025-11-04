#!/usr/bin/env python3
"""
Script to help save the logo image to the static directory.
Run this script and then manually copy your logo image to static/images/logo.png
"""

import os
import shutil

def save_logo():
    static_images_dir = "static/images"
    
    # Ensure the directory exists
    os.makedirs(static_images_dir, exist_ok=True)
    
    print(f"Static images directory is ready: {static_images_dir}")
    print("Please manually copy your logo file to: static/images/logo.png")
    print("The template has been updated to use the new logo!")
    
    # List current files in the directory
    if os.path.exists(static_images_dir):
        print("\nCurrent files in static/images/:")
        for file in os.listdir(static_images_dir):
            print(f"  - {file}")

if __name__ == "__main__":
    save_logo()