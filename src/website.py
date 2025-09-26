import os
from blocks import *

def extract_title(markdown):
    # Extracts the title from the markdown content
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block_to_blocktype(block) == BlockType.HEADING:
            # make sure it's an h1
            if not re.match(r"^#\s", block):
                continue

            # Remove leading # and any leading/trailing whitespace
            title = re.sub(r"^#\s", "", block).strip()
            return title

    raise ValueError("No title found in markdown content")

def generate_page(from_path, template_path, dest_path, dest_dir_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    markdown_content = ""
    template = ""

    #read md
    try:
        with open(from_path, 'r') as file:
            markdown_content = file.read()
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Other error {e}")

    #read template
    try:
        with open(template_path, 'r') as file:
            template = file.read()
    except FileNotFoundError:
        print("template not found")
    except Exception as e:
        print("Other error with template {e}")

    title = extract_title(markdown_content)

    html_content = markdown_to_html_node(markdown_content).to_html()
    #replace {{ Title }} and {{ Content }} in template with title and html_content
    title_to_replace = "{{ Title }}"
    content_to_replace = "{{ Content }}"
    template = template.replace(title_to_replace, title)
    template = template.replace(content_to_replace, html_content)

    #replace href="/ with href="{from_path}/"
    template = re.sub(r'href="/', f'href="{dest_dir_path}/', template)
    #replace src="/ with src="{from_path}/"
    template = re.sub(r'src="/', f'src="{dest_dir_path}/', template)


    #if directories in dest_path do not exist, create them
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        print(f"Directory {dest_dir} does not exist, creating it")
        os.makedirs(dest_dir)

    try:
        with open(dest_path, 'w') as file:
            print(f"Writing file to path {dest_path}")
            file.write(template)
    except Exception as e:
        print(f"Error {e} when writing file to path {dest_path}")
    
    
