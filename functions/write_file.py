import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    dir = os.path.dirname(abs_file_path)
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.isdir(dir):
        try:
            os.makedirs(dir)
        except Exception as e:
            return f"Error: Could not create directory {dir} - {e}"
    
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: Could not write content to {abs_file_path} - {e}"
        

    return f'Successfully wrote to "{abs_file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content provided to the file specified, using the content provided, constrained to the working directory. if the file already exists, it is overwritten. If the file does not exist, it is created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be overwritten, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The stream of text to overwrite the provided file with.",
            ),
        },
    ),
)
