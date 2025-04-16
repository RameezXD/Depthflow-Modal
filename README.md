🌌 DepthFlow Modal Integration
Overview

This repository provides a minimal Python interface to run DepthFlow — the soul of this project — on Modal's serverless GPU infrastructure.

Think of this as bringing the magic of Immersity AI to the open-source world — powered by DepthFlow, crafted by BrokenSource, and simply deployed via a script anyone can run.

All credit for the core functionality goes to DepthFlow, a remarkable open-source tool for image-to-video transformation using motion and depth inference. This repo merely wraps it in a Modal deployment for ease of use and scaling.
✨ Features

- ⚙️ Batch Processing — Convert multiple images into videos using DepthFlow with GPU acceleration.

- 🌐 Web Interface — Gradio-powered GUI for easy access and real-time previews.

- 📦 Serverless Scaling — Run on Modal’s on-demand infrastructure with parallel processing.

- 📁 Logging — Track processed files and errors via structured logs.


🔧 Requirements

- Python 3.12

- Modal account with CLI installed

- NVIDIA GPU (T4 recommended for now)

📜 Scripts
1. depthflow_bulk.py

- Batch-converts PNG images in /data/images to MP4 videos using DepthFlow.

🔹 Usage

- Place your PNG images in the /data/images directory.

Run the script:

      modal run depth_bulk.py

- Processed videos will be saved in /data/videos.

✅ Highlights

- Automatically skips already processed images.

- Logs success and errors to /data/logs.

- Customizable hardware allocation (CPU, GPU, memory).

2. depthflow_gui.py

- Launches a Gradio web interface for DepthFlow.

🔹 Usage

Run the script:

    modal serve depthflow_gui.py

✅ Highlights

- Real-time image-to-video interface.

- Supports concurrent users and container scaling.

⚙️ Modal Configuration

- Both scripts use a pre-built Modal container with the following:

- depthflow==0.9.0.dev1

- torch==2.6.0 (CUDA 12.4)

- Tools: wget, git, ffmpeg

🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for improvements or fixes.
📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
🙏 Acknowledgments

🎥 DepthFlow — the soul of this project. Without it, there is no magic. Like Immersity AI, but open-source and written buy Brokensoure (https://github.com/BrokenSource).

☁️ Modal — for enabling seamless, serverless GPU computing.
