import os, subprocess

def run_python_file(working_directory, file_path):
  abspath_working_directory = os.path.abspath(working_directory)
  abspath_file = os.path.abspath(os.path.join(working_directory, file_path))
  if not abspath_file.startswith(abspath_working_directory):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.exists(abspath_file):
    return f'Error: File "{file_path}" not found.'

  if abspath_file[-3:] != ".py":
    return f'Error: "{file_path}" is not a Python file.'
  
  try:
    process = subprocess.run(timeout=30, capture_output=True, args=['python3', abspath_file], text=True)
    results = ""
    if process.stdout != "":
      results += "STDOUT:\n"
      results += f"{process.stdout}\n"
    if process.stderr != "":
      results += "STDERR:\n"
      results += f"{process.stderr}\n"
    if process.returncode != 0:
      results += f"Process exited with code {process.returncode}\n"
    if results == "":
      return "No output produced."
    return results

  except Exception as e:
    f"Error: executing Python file: {e}"