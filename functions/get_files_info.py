import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = ''
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(abs_working_dir, directory))
    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'
    dir_list = os.listdir(abs_dir)
    dir_deets = ""
    for file in dir_list:
        file_path = os.path.join(abs_dir, file)
        file_size = os.path.getsize(file_path)
        is_dir = not os.path.isfile(file_path)
        dir_deets += f"{file}: file_size={file_size} bytes, is_dir={is_dir}\n"
    return dir_deets

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)