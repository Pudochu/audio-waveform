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