import os
import shutil

from markdown_page_parser import markdown_to_html_node

def generate_pages_recursively(from_dir_path, template_path, dest_dir_path):
    if os.path.isfile(from_dir_path):
        print(f'yoo: {dest_dir_path}')
        generate_page(from_dir_path, template_path, dest_dir_path)
        return

    for filename in os.listdir(from_dir_path):
        from_path = os.path.join(from_dir_path, filename)

        if os.path.isdir(from_path):
            dest_path = os.path.join(dest_dir_path, filename)
            os.mkdir(dest_path)
        else:
            dest_path = os.path.join(dest_dir_path, filename.replace('.md', '.html'))

        generate_pages_recursively(from_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def extract_title(markdown):
    blocks = markdown.split("\n\n")

    if len(blocks) < 2 and not blocks[0].startswith('# '):
        raise ValueError('There needs to be an `h1` header at the start of the page!')

    return blocks[0].split('# ')[1]

def copy_files(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files(from_path, dest_path)


