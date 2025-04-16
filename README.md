# DepthFlow Modal Integration

## Overview
This repository provides a very simple set of Python scripts to integrate the DepthFlow software with Modal, enabling efficient and scalable processing of images and videos. The scripts leverage Modal's serverless capabilities to deploy DepthFlow applications with GPU acceleration and concurrent processing.

## Features
- **Batch Processing**: Process multiple images into videos using DepthFlow with GPU acceleration.
- **Web Interface**: Deploy a Gradio-based web interface for DepthFlow.
- **Scalable Deployment**: Utilize Modal's serverless infrastructure for efficient resource management.
- **Logging**: Maintain success and error logs for processed files.

## Requirements
- Python 3.12
- Modal account and CLI installed
- NVIDIA GPU (T4 recommended) (as of right now it's the only one working )

## Scripts

### 1. `depth_bulk.py`
This script processes a batch of PNG images into MP4 videos using DepthFlow.

#### Usage
1. Place your PNG images in the `/data/images` directory.
2. Run the script:
   ```bash
   modal run depth_bulk.py
   ```
3. Processed videos will be saved in the `/data/videos` directory.

#### Key Features
- Automatically skips already processed files.
- Logs success and error messages in `/data/logs`.
- Configurable GPU, CPU, and memory allocation.

### 2. `depthflow_gui.py`
This script deploys a Gradio-based web interface for DepthFlow.

#### Usage
1. Run the script:
   ```bash
   modal serve depthflow_gui.py
   ```
2. Access the web interface at `http://localhost:7860`.

#### Key Features
- Provides a user-friendly web interface for DepthFlow.
- Supports concurrent inputs and multiple containers.

## Configuration
Both scripts use a pre-configured Modal container image with the following dependencies:
- `depthflow==0.9.0.dev1`
- `torch==2.6.0` (CUDA 12.4)
- `wget`, `git`, `ffmpeg`

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- [Modal](https://modal.com) for providing serverless infrastructure.
- [DepthFlow](https://github.com/depthflow) for the image-to-video processing software.
