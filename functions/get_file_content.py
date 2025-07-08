import os

def get_file_content(working_directory, file_path):
  abspath_working_directory = os.path.abspath(working_directory)
  abspath_file = os.path.abspath('/'.join([working_directory, file_path]))
  # print("====================")
  # print(f"working: {working_directory}, abs: {abspath_working_directory}")
  # print(f"directory: {file_path}, abs: {abspath_file}")

  if not abspath_file.startswith(abspath_working_directory):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(abspath_file):
    return f'Error: File not found or is not a regular file: "{file_path}"'
  
  # read file
  MAX_CHARS = 10000

  with open(abspath_file, "r") as f:
    file_content_string = f.read(MAX_CHARS)
  
  file_content_string += f"[...File \"{file_path}\" truncated at 10000 characters]"

  return file_content_string