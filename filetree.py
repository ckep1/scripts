import os
import fnmatch
import sys

def parse_gitignore(gitignore_path):
    patterns = []
    with open(gitignore_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if line.startswith('/'):
                    line = line.lstrip('/')
                patterns.append(line)
    # Add default ignore patterns
    patterns.append('.git')
    return patterns

def should_ignore(path, patterns, is_dir):
    for pattern in patterns:
        if pattern.endswith('/'):
            # Strip trailing slash for directory patterns
            pattern = pattern.rstrip('/')
            if is_dir and (fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern)):
                return True
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def directory_map(dir_path, patterns, prefix=""):
    result = []
    for root, dirs, files in os.walk(dir_path, topdown=True):
        relative_root = os.path.relpath(root, dir_path)
        
        if relative_root == ".":
            relative_root = ""
        
        if should_ignore(relative_root, patterns, is_dir=True):
            dirs[:] = []  # Clear dirs to prevent further os.walk in this branch
            continue
        
        level = root.replace(dir_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        sub_indent = ' ' * 4 * (level + 1)
        result.append(f"{indent}{os.path.basename(root)}/")
        
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(relative_root, d), patterns, is_dir=True)]
        
        for f in files:
            file_path = os.path.join(relative_root, f)
            if not should_ignore(file_path, patterns, is_dir=False):
                result.append(f"{sub_indent}{f}")
    return result

def get_unique_filename(directory, base_name, extension):
    number = 0
    while True:
        if number == 0:
            filename = f"{base_name}{extension}"
        else:
            filename = f"{base_name}{number}{extension}"
        if not os.path.exists(os.path.join(directory, filename)):
            return filename
        number += 1

def main():
    dir_path = os.getcwd()
    save_to_file = False

    # Parse arguments
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == '-savefile':
                save_to_file = True
            else:
                dir_path = arg
    
    if not os.path.isdir(dir_path):
        print(f'Error: The directory "{dir_path}" does not exist.')
        return

    gitignore_path = os.path.join(dir_path, '.gitignore')
    patterns = parse_gitignore(gitignore_path) if os.path.exists(gitignore_path) else []
    directory_structure = directory_map(dir_path, patterns)

    if save_to_file:
        base_name = f"dir_{os.path.basename(os.path.normpath(dir_path))}"
        output_filename = get_unique_filename(dir_path, base_name, '.md')
        with open(os.path.join(dir_path, output_filename), 'w', encoding='utf-8') as output_file:
            for line in directory_structure:
                output_file.write(line + '\n')
        print(f'Directory structure saved to "{output_filename}"')
    else:
        for line in directory_structure:
            print(line)

if __name__ == "__main__":
    main()
