import os

def write_file(working_directory, file_path, content):
  abspath_working_directory = os.path.abspath(working_directory)
  abspath_file = os.path.abspath('/'.join([working_directory, file_path]))

  if not abspath_file.startswith(abspath_working_directory) or file_path.startswith('/'):
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
  
  directory = "/".join(abspath_file.split("/")[0:-1])
  if not os.path.exists(directory):
    os.makedirs(directory)
  try:
    with open(abspath_file, "w") as f:
      f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f"Error: writing to file: {e}"