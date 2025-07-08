import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from available_functions import available_functions
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from prompts import system_prompt
from config import WORKING_DIR

def main():
  if len(sys.argv) < 2:
    sys.exit(1)

  verbose = "--verbose" in sys.argv

  load_dotenv()
  api_key = os.environ.get("GEMINI_API_KEY")

  user_prompt = sys.argv[1]

  messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
  ]

  client = genai.Client(api_key=api_key)

  MAX_ITERS = 20
  iters = 0
  while True:
      iters += 1
      if iters > MAX_ITERS:
          print(f"Maximum iterations ({MAX_ITERS}) reached.")
          sys.exit(1)

      try:
          final_response = generate_content(client, messages, verbose)
          if final_response:
              print("Final response:")
              print(final_response)
              break
      except Exception as e:
          print(f"Error in generate_content: {e}")

def generate_content(client, messages, verbose):
  response = client.models.generate_content(
    config=types.GenerateContentConfig(
      tools=[available_functions], system_instruction=system_prompt),
    model='gemini-2.0-flash-001', 
    contents=messages,
  )

  if response.candidates:
    for candidate in response.candidates:
      messages.append(candidate.content)

  if not response.function_calls:
      return response.text
  
  function_responses = []
  for function_call in response.function_calls:
    function_call_result = call_function(function_call)
    
    if not function_call_result or not function_call_result.parts or len(function_call_result.parts) == 0:
      raise Exception("Fatal error: function_call_result is empty")
    
    function_responses.append(function_call_result.parts[0])

    if verbose:
      print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
      print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
      print(f"-> {function_call_result.parts[0].function_response.response["result"]}")

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

  messages.append(types.Content(role="tool", parts=function_responses))

def call_function(function_call_part, verbose=False):
  if verbose:
    print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
  else:
    print(f" - Calling function: {function_call_part.name}")

  function_dic = {
    "get_file_content": get_file_content, 
    "get_files_info": get_files_info, 
    "run_python_file": run_python_file, 
    "write_file": write_file, 
  }
  args = dict(function_call_part.args)
  args["working_directory"] = WORKING_DIR

  if function_call_part.name not in function_dic:
    return types.Content(
      role="tool",
      parts=[
          types.Part.from_function_response(
              name=function_call_part.name,
              response={"error": f"Unknown function: {function_call_part.name}"},
          )
        ],
    ) 

  result = function_dic[function_call_part.name](**args)
  return types.Content(
      role="tool",
      parts=[
          types.Part.from_function_response(
              name=function_call_part.name,
              response={"result": result},
          )
      ],
  )

if __name__ == "__main__":
  main()