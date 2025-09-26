import os
import shutil
import sys
from textnode import *
from website import generate_page



def main():
    basepath  = sys.argv[1] if len(sys.argv) > 1 else "/"   
    print("Base path: " + basepath)

    target_directory = "docs"
    print("Target directory: " + target_directory)
    
    print("Starting site generation...")
    print(f"Clearing out {target_directory} directory...")
    delete_everything_in_target(target_directory)
    
    print("Copying static files to target directory...")
    copy_everything_to_target(target_directory)
    
    print("Generating pages...")
    generate_pages_recursive("content", "template.html", target_directory)

    print("Site generation complete.")

#
# file operations helpers
#

def delete_everything_in_target(target_directory):
    # Deletes everything in the target directory
    if not os.path.exists(target_directory):
        print(f"Target directory {target_directory} does not exist, nothing to clean")
        return

    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def copy_everything_to_target(target_directory):
    copy_folder_recursively("static", target_directory)

def copy_folder_recursively(src, dest):
    try:
        for file in os.listdir(src):
            src_file = os.path.join(src, file)
            dest_file = os.path.join(dest, file)
            if os.path.isdir(src_file):
                if not os.path.exists(dest_file):
                    os.makedirs(dest_file)
                copy_folder_recursively(src_file, dest_file)
            else:
                shutil.copy2(src_file, dest_file)
    except Exception as e:
        print(f'Failed to copy from {src} to {dest}. Reason: {e}')

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    #find every file in dir_path_content
    print(f"Current working directory: {os.getcwd()}")
    print(f"Generating pages from content directory {dir_path_content} using template {template_path} into destination directory {dest_dir_path}")
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                content_path = os.path.join(root, file)
                #determine relative path from dir_path_content
                rel_path = os.path.relpath(content_path, dir_path_content)
                #determine destination path
                dest_path = os.path.join(dest_dir_path, rel_path)
                dest_path = dest_path[:-3] + ".html" #change .md to .html
                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                print(f"Generating page: {content_path} -> {dest_path}")
                generate_page(content_path, template_path, dest_path, dest_dir_path)

if __name__ == "__main__":
    main()