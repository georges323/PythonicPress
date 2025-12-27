import os
import shutil
import sys

from generator import copy_files, generate_page, generate_pages_recursively

dir_path_public = './docs'
dir_path_source = './static'
dir_path_content = './content'
template_file_path = './template.html'

def main():
    basepath = sys.argv[1]
    print(f"BasePath: {basepath}")

    if os.path.exists(dir_path_public):
        print(f"Deleting public directory: {dir_path_public}")
        shutil.rmtree(dir_path_public)
    
    print(f"Copying to public directory from {dir_path_source}")
    copy_files(dir_path_source, dir_path_public)

    generate_pages_recursively(
        basepath,
        dir_path_content,
        template_file_path, 
        dir_path_public
    )

if __name__ == "__main__":
    main()
