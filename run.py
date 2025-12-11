import subprocess
import sys

def main():
    """Run the Streamlit application"""
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app/streamlit_app.py"
    ])

if __name__ == "__main__":
    main()