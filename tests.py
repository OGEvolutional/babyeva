from functions.run_python import run_python_file

print('Test 1:')
print(run_python_file("calculator", "main.py"))

print('\nTest 2:')
print(run_python_file("calculator", "tests.py"))

print('\nTest 3 (outside working directory):')
print(run_python_file("calculator", "../main.py"))

print('\nTest 4 (nonexistent file):')
print(run_python_file("calculator", "nonexistent.py"))
