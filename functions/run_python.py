import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    try:
    
        full_path = os.path.normpath(os.path.join(working_directory, file_path))
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

    
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'

    
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

    
        result = subprocess.run(
            ["python", os.path.basename(full_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory,
        )

        output = ""

        if result.stdout:
            output += f'STDOUT:\n{result.stdout}'
        if result.stderr:
            output += f'STDERR:\n{result.stderr}'
        if result.returncode != 0:
            output += f'\nProcess exited with code {result.returncode}'

        if not output.strip():
            return "No output produced."

        return output.strip()

    except Exception as e:
        return f"Error: executing Python file: {e}"
