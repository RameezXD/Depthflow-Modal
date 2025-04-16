'''
# This script processes images using DepthFlow and Modal in bulk.
# You can upload your images to modal volume like this:
modal volume put "volume-name" ./local/path/to/images ./images(remote path)
check modal docs for more details.
# To run the script, use the command:
modal run deth_bulk.py 
'''

# Import necessary libraries
import modal
import subprocess
import os
from tqdm import tqdm
import logging

# Define the container image with required dependencies
image = (
    modal.Image.from_registry("nvidia/opengl:1.2-glvnd-runtime-ubuntu22.04", add_python="3.12")
    .apt_install("wget", "git", "ffmpeg")
    .run_commands("pip install depthflow==0.9.0.dev1")
    .run_commands("python3 -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124")
)

# Create a persistent volume for storing data
volume = modal.Volume.from_name("depthflow", create_if_missing=True)

# Define the Modal application with its configuration
app = modal.App(
    "depthflow-processor",  # Application name
    image=image  # Use the defined container image
)

# Define the processing function with resource requirements
@app.function(
    gpu="T4",  # Specify GPU type (only T4 is supported at the time of writing)
    cpu=4,  # Number of CPU cores (minimum 4 cores required) (set it to 12 for better performance)
    memory=4096,  # Memory allocation in MB
    volumes={"/data": volume},  # Mount the volume to the container
    timeout=3600,  # Timeout in seconds (adjust as needed)
    max_containers=4,  # Maximum number of containers
    allow_concurrent_inputs=8  # Allow concurrent inputs
)
def process_images():
    # Create necessary directories in the mounted volume
    os.makedirs("/data/images", exist_ok=True)
    os.makedirs("/data/videos", exist_ok=True)
    os.makedirs("/data/logs", exist_ok=True)

    # Setup logging for success and error logs
    success_logger = logging.getLogger('success')
    error_logger = logging.getLogger('error')

    success_logger.setLevel(logging.INFO)
    error_logger.setLevel(logging.ERROR)

    success_handler = logging.FileHandler('/data/logs/success.log')
    error_handler = logging.FileHandler('/data/logs/error.log')

    success_logger.addHandler(success_handler)
    error_logger.addHandler(error_handler)

    # Read already processed files from the success log
    processed_files = set()
    if os.path.exists('/data/logs/success.log'):
        with open('/data/logs/success.log', 'r') as f:
            for line in f:
                if 'Successfully processed:' in line:
                    processed_file = line.split('Successfully processed:')[-1].strip()
                    processed_files.add(processed_file)

    # Define input and output folders
    input_folder = "/data/images"
    output_folder = "/data/videos"

    # Get list of unprocessed PNG files change png to jpg if you want to process jpg files or any file
    png_files = [f for f in os.listdir(input_folder) 
                 if f.endswith('.png') and f not in processed_files]
    print(f"Found {len(png_files)} new PNG files to process")

    # Process each PNG file
    for file in tqdm(png_files, desc="Processing images"):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file.replace('.png', '.mp4'))

        # Define the DepthFlow command
        command = [
            "depthflow", "h264",
            "--preset", "slow",
            "orbital", "--intensity", "1", "--depth", "0.4",
            "input", "-i", input_path,
            "main", "-t", "5",
            "-o", output_path,
            "-q", "100",
            "--fps", "60"
        ]  # Use -h to determine the height of the video

        try:
            # Run the DepthFlow command
            subprocess.run(command, check=True)

            # Verify the video file exists and is not empty
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                success_logger.info(f"Successfully processed: {file}")
                print(f"\nProcessed: {file}")
            else:
                raise Exception("Video file not created or empty")
        except Exception as e:
            # Log errors and clean up failed output files
            error_msg = f"Error processing {file}: {str(e)}"
            error_logger.error(error_msg)
            print(f"\nError: {error_msg}")
            if os.path.exists(output_path):
                os.remove(output_path)

# Entry point for the script
if __name__ == "__main__":
    with app.run():
        process_images.remote()