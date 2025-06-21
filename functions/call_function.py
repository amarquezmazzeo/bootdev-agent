from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .write_file import write_file
from .run_python_file import run_python_file

from google.genai import types



def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map = {
    'get_file_content': get_file_content,
    'get_files_info': get_files_info,
    'write_file': write_file,
    'run_python_file': run_python_file
}

    function_args['working_directory'] = 'calculator'

    if function_name in function_map:
        function_result = function_map[function_name](**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )