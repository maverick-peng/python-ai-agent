
import os

def get_files_info(working_directory, directory=None):

  abspath_working_directory = os.path.abspath(working_directory)
  abspath_directory = abspath_working_directory
  if directory:
    abspath_directory = os.path.abspath('/'.join([working_directory, directory]))
  # print("====================")
  # print(f"working: {working_directory}, abs: {abspath_working_directory}")
  # print(f"directory: {directory}, abs: {abspath_directory}")

  if not abspath_directory.startswith(abspath_working_directory):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  
  if not os.path.isdir(abspath_directory):
    return f'Error: "{directory}" is not a directory'
  
  results = []
  for item in os.listdir(abspath_directory):
    item_path = os.path.join(abspath_directory, item)
    results.append(f"- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}")

  return '\n'.join(results)