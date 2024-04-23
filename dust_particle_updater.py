import os
import re

def update_particle_command(command):
    # Regex patterns to find old Minecraft particle commands and replace them with new format
    pattern_dust = r'(\b(?:minecraft:)?dust\b) (-?\d*\.?\d*) (-?\d*\.?\d*) (-?\d*\.?\d*) (-?\d*\.?\d*)'
    pattern_transition = r'(\b(?:minecraft:)?dust_color_transition\b) (-?\d*\.?\d*) (-?\d*\.?\d*) (-?\d*\.?\d*) (-?\d*\.?\d*) (-?\d*\.?\d*) (-?\d*\.?\d*) (-?\d*\.?\d*)'

    def replacer_dust(match):
        command = match.group(1)
        rgb1, rgb2, rgb3, scale = match.group(2), match.group(3), match.group(4), match.group(5)
        return f'{command}{{color:[{rgb1},{rgb2},{rgb3}],scale:{scale}}}'

    def replacer_transition(match):
        command = match.group(1)
        from_r, from_g, from_b, scale, to_r, to_g, to_b = match.group(2), match.group(3), match.group(4), match.group(5), match.group(6), match.group(7), match.group(8)
        return f'{command}{{from_color:[{from_r}f, {from_g}f, {from_b}f], scale:{scale}f, to_color:[{to_r}f, {to_g}f, {to_b}f]}}'

    command = re.sub(pattern_dust, replacer_dust, command)
    command = re.sub(pattern_transition, replacer_transition, command)
    return command

def process_files(directory):
    # Collect all .mcfunction files
    files_to_process = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mcfunction"):
                files_to_process.append(os.path.join(root, file))

    total_files = len(files_to_process)
    print(f"Found {total_files} '.mcfunction' files to process.")

    # Ask for user confirmation before processing
    confirmation = input("Do you want to proceed with updating these files? (yes/no): ")
    if confirmation.lower() != 'yes':
        print("Process aborted by the user.")
        return

    # Process each file
    for index, file_path in enumerate(files_to_process):
        print(f"Processing ({index + 1}/{total_files}): {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        updated_content = update_particle_command(content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

    print("All files have been processed successfully.")

# Automatically use the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))
process_files(script_directory)
