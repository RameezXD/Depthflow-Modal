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
        # tmp path basically it resolves the issue with gradio interface where the videostakes forever to load due gradio's network limitations sometimes.
        # Define custom temp path (e.g., /vol/tmp if you have a Modal volume or any location you want)
        custom_tmp = "/vol/tmp"
        os.makedirs(custom_tmp, exist_ok=True)

        env = os.environ.copy()
        env["TMPDIR"] = custom_tmp
        
        # Start the DepthFlow Gradio server
        subprocess.Popen(
            ["python", "-m", "DepthFlow", "gradio"]
            env=env,  # Pass the modified environment variables
        )

    @modal.web_server(port=7860, startup_timeout=120)
    def ui(self):
        # Define the web server endpoint
        return "Depthflow is up!"

# Deploy the app
if __name__ == "__main__":
    app.deploy()
