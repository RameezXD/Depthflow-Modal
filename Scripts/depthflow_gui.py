'''
# DepthFlow Modal Deployment Script
# To run the script, use the command:
modal serve dethflow_gui.py
'''

# Import necessary libraries
import modal
import subprocess

# Define the container image with required dependencies
image = (
    modal.Image.from_registry("nvidia/opengl:1.2-glvnd-runtime-ubuntu22.04", add_python="3.12")
    .apt_install("wget", "git", "ffmpeg")
    .run_commands("pip install depthflow==0.9.0.dev1") # using pre-release version (recommended)
    .run_commands("python3 -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124")
)

# Define the Modal application with its configuration
app = modal.App(
    name="depthflow-app",  # Application name
    image=image  # Use the defined container image
)

# Define the class for DepthFlow processing
@app.cls(
    cpu=4,   # Number of CPU cores (minimum 4 cores required) (set it to 12 for better performance)
    gpu="T4",  # Specify GPU type (only T4 is supported at the time of writing)
    memory=4096,  # Memory allocation in MB
    max_containers=4,  # Maximum number of containers
    allow_concurrent_inputs=8  # Allow concurrent inputs
)
class Depthflow:
    def __init__(self):
        self.running = True  # Initialize the running state

    @modal.enter()
    def setup_depthflow(self):
        # Start the DepthFlow Gradio server
        subprocess.Popen(
            ["python", "-m", "DepthFlow", "gradio"]
        )

    @modal.web_server(port=7860, startup_timeout=120)
    def ui(self):
        # Define the web server endpoint
        return "server is up!"

# Deploy the app
if __name__ == "__main__":
    app.deploy()
