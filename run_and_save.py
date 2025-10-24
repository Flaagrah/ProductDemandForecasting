import subprocess
import sys
import os

# Set UTF-8 encoding for output
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Run the LLM call and capture output
result = subprocess.run([
    sys.executable, '-m', 'LLM_Client.llm_call'
], capture_output=True, text=True, encoding='utf-8')

# Save to file with UTF-8 encoding
with open('LLM_Client/output.txt', 'w', encoding='utf-8') as f:
    f.write(result.stdout)
    if result.stderr:
        f.write(f"\n\nError output:\n{result.stderr}")

print("Output saved to LLM_Client/output.txt")
