## Waveform Video Generator
This project provides a web-based interface for generating waveform videos from audio files using Gradio. The application utilizes FFmpeg and ImageMagick to overlay captions and customize the appearance of the waveform. The environment is set up using a Docker container for ease of deployment.

### Features
- Upload an audio file to generate a waveform video.
- Customize the background color, foreground opacity, bars color, number of bars, and bar width.
- Option to add a caption text overlay on the waveform video.

### Installation

To run this project locally, ensure you have Docker installed and follow the steps below:

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Build the Docker container
docker build -t waveform-video-generator .

# Run the Docker container
docker run -p 7860:7860 waveform-video-generator
```

The Gradio interface should be accessible at `http://0.0.0.0:7860` in your web browser.

### Usage

1. Upload your audio file.
2. Customize the waveform video by adjusting the parameters:
    - Background Color
    - Foreground Opacity
    - Bars Color
    - Number of Bars
    - Bar Width
    - Caption Text (optional)
3. Click on the submit button to generate the waveform video.
4. Download the generated waveform video.

### Code Overview

#### app.py
The core functionality of the application is defined in the `app.py` file. The `Predictor` class contains the `predict` method, which generates the waveform video using Gradio, FFmpeg, and ImageMagick. The Gradio interface is configured to accept various input parameters to customize the waveform video's appearance.

#### Dockerfile
The `Dockerfile` sets up the required environment to run the application. It installs system dependencies such as FFmpeg and ImageMagick, as well as the necessary Python packages. The Docker container ensures that all necessary dependencies are available and configured correctly.

```dockerfile
FROM python:3.9-slim

# Install system packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    fontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pip packages
RUN pip install gradio==3.50.2

# Set environment variables for matplotlib and fontconfig
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV FONTCONFIG_PATH=/etc/fonts

# Create needed directories with correct permissions
RUN mkdir -p /tmp/matplotlib /usr/share/fonts /src/fonts /root/.config /src/flagged && \
    chmod -R 777 /tmp /usr/share/fonts /root/.config /src/fonts /src/flagged

# Copy the rest of the application code
COPY . /src

# Set the working directory
WORKDIR /src

# Set the entry point to run the prediction script
ENTRYPOINT ["python", "app.py"]
```

### Contributing
Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

### License
This project is licensed under the MIT License.

---

By following the steps mentioned in the installation section, you should be able to run the Waveform Video Generator locally and leverage its features for creating customized waveform videos.

For any further queries or support, please raise an issue on the GitHub repository. Happy coding!
