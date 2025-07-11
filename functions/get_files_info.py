import os
from google.genai import types



def get_files_info(working_directory, directory=None):
    try:
        
        directory = directory or "."

        
        full_path = os.path.normpath(os.path.join(working_directory, directory))

        
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        
        result_lines = []
        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                result_lines.append(
                    f'- {entry}: file_size={size} bytes, is_dir={is_dir}'
                )
            except Exception as e:
                return f'Error: {e}'

        return "\n".join(result_lines)

    except Exception as e:
        return f'Error: {e}'

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