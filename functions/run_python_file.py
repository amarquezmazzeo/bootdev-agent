import os
import subprocess
import sys

from google.genai import types

# PYTHON_PATH = "venv/bin/python"

def run_python_file(working_directory, file_path, args = None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    # print(abs_file_path)
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.lower().endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = [sys.executable, abs_file_path]
        if args:
            commands.extend(args)
        completed_process = subprocess.run(
            commands,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=abs_working_dir)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

    if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
        return f"No output produced."
    formatted_result = f"STDOUT: {completed_process.stdout}\n"
    formatted_result += f"STDERR: {completed_process.stderr}"
    if completed_process.returncode != 0:
        formatted_result += f"\nProcess exited with code {completed_process.returncode}"
    return formatted_result

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Spins a subroutine and runs the specified python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the python file to be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments to pass to the python program, only if explicitly requested.",
            ),
        },
    ),
)