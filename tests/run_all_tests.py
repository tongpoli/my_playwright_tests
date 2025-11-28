import subprocess

# List of test scripts
test_files = [
    "requests_get.py",
    "requests_post.py",
    "requests_put.py",
    "requests_delete.py",
    "playwright_get.py",
    "playwright_post.py",
    "playwright_put.py",
    "playwright_delete.py",
    "UIandAPI.py"
]

for file in test_files:
    print(f"\nRunning {file}...")
    result = subprocess.run(["python", file], capture_output=True, text=True)
    print(result)
    print(result.stdout)
    if result.returncode != 0:
        print(f"[Failed]] {file} failed with error:")
        print(result.stderr)
    else:
        print(f"[PASS]{file} passed!")