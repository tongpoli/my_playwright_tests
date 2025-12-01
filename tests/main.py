# main.py
import subprocess
import sys

# Run pytest with HTML report
subprocess.run([sys.executable, "-m", "pytest", "tests", "--html=playwright-report.html", "--self-contained-html", "--disable-warnings"])
