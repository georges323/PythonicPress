import os
import shutil

from markdown_block_parser import extract_title
from markdown_page_parser import markdown_to_html_node


def main():
    refresh_static_content()

    print('------')

    generate_page('./content/index.md', './template.html', './public/index.html')

def generate_page(from_path, template_path, dest_path):
    from_path_abs = os.path.abspath(from_path)
    dest_path_abs = os.path.abspath(dest_path)
    template_path_abs = os.path.abspath(template_path)

    print(f'Generating page from {from_path_abs} to {dest_path_abs} using {template_path_abs}')

    with open(from_path_abs, 'r') as f:
        markdown = f.read()

        with open(template_path_abs, 'r') as t:
            template_path_contents = t.read()

            html_content = markdown_to_html_node(markdown).to_html()
            markdown_title = extract_title(markdown)

            template_path_contents = template_path_contents.replace('{{ Title }}', markdown_title)
            template_path_contents = template_path_contents.replace('{{ Content }}', html_content)

            parent_dirs = os.path.dirname(dest_path_abs)
            os.makedirs(parent_dirs, exist_ok=True)

            with open(dest_path_abs, 'w') as d:
                d.write(template_path_contents)

def refresh_static_content(source='./static', destination='./public'):
    source_abs = os.path.abspath('./static')
    print(f'Source Ablosute Path: {source_abs}')

    destination_abs = os.path.abspath('./public')
    print(f'Destination Ablosute Path: {destination_abs}')

    if os.path.exists(destination_abs) and os.path.isdir(destination_abs):
        print(f'Deleting Directory: {destination_abs}')
        delete_path(destination_abs)

    print(f'Creating Directory: {destination_abs}')
    os.mkdir(destination_abs)

    print(f'Copying Directory {source_abs} to {destination_abs}')
    copy_path(source_abs, destination_abs)


def copy_path(source, destination):
    if os.path.isfile(source):
        shutil.copy(source, destination)
        return

    child_paths= os.listdir(source)
    for child_path in child_paths:
        new_path_abs = os.path.join(destination, os.path.basename(child_path)) 
        child_path_abs = os.path.join(source, child_path)
        if os.path.isdir(child_path_abs):
            os.mkdir(new_path_abs)

        copy_path(child_path_abs, new_path_abs)

def delete_path(path):
    if os.path.isfile(path):
        os.remove(path)
        return
    
    child_paths = os.listdir(path)
    for child_path in child_paths:
        child_abs_path = os.path.join(path, child_path)
        delete_path(child_abs_path)

        if os.path.isdir(child_abs_path):
            os.rmdir(child_abs_path)

    os.rmdir(path)

if __name__ == "__main__":
    main()
