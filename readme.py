import os

*# Specify the directory you want to iterate through*
directory_path = 'hobbyfarm/contentmd/rgs-rancher-rodeo'

*# Define the output file name*
output_file = 'README.md'

*# Check if the specified path is a directory*
if os.path.isdir(directory_path):
    *# Open the output file for writing*
    with open(output_file, 'w', encoding='utf-8') as readme_file:
        *# Iterate through all files in the directory*
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            *# Check if the item in the directory is a file*
            if os.path.isfile(file_path):
                readme_file.write(f"## Contents of {filename}:\n\n")
                
                try:
                    *# Open and read the file with the appropriate encoding*
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_contents = file.read()
                        readme_file.write(file_contents)
                except UnicodeDecodeError:
                    *# Handle files that cannot be decoded as UTF-8*
                    readme_file.write("Unable to decode this file as UTF-8.\n\n")
                
                readme_file.write('\n\n' + '-' * 40 + '\n\n')  *# Separate files with a line of dashes*
else:
    print(f"{directory_path} is not a valid directory.")
