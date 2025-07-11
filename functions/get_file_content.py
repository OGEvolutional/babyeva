import os
from functions.config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file within the working directory. Automatically truncates long files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
    
        full_path = os.path.normpath(os.path.join(working_directory, file_path))
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

    
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

     
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

    
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

    
        if len(content) > MAX_CHARS:
            truncated = content[:MAX_CHARS]
            truncated += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return truncated

        return content

    except Exception as e:
        return f'Error: {e}'