import subprocess
import gradio as gr
import tempfile
from pathlib import Path
import os

# Check permissions and environment setup
print("Checking directory and file permissions...")
for path in ['/tmp', '/usr/share/fonts', '/root/.config', '/src/fonts', '/src/flagged']:
    if os.access(path, os.W_OK):
        print(f'Directory {path} is writable.')
    else:
        print(f'Error: Directory {path} is not writable.')

class Predictor:
    def predict(self,
        audio: str,
        bg_color: str = "#000000",
        fg_alpha: float = 0.75,
        bars_color: str = "#ffffff",
        bar_count: int = 100,
        bar_width: float = 0.4,
        caption_text: str = "",
    ) -> str:
        """Make waveform video from audio file"""
        waveform_video = gr.make_waveform(
            audio,
            bg_color=bg_color,
            fg_alpha=fg_alpha,
            bars_color=bars_color,
            bar_count=bar_count,
            bar_width=bar_width,
        )

        if caption_text == "" or caption_text is None:
            return waveform_video
        else:
            padded_waveform_path = tempfile.mktemp(suffix=".mp4")
            background_image_path = tempfile.mktemp(suffix=".png")
            final_video_path = tempfile.mktemp(suffix=".mp4")

            print("Running ffmpeg to add padding...")
            subprocess.run([
                'ffmpeg', '-y', '-i', waveform_video, '-vf',
                f'pad=width=1000:height=667:x=0:y=467:color={bg_color[1:]}',
                padded_waveform_path
            ], check=True)

            print("Creating an image using ImageMagick...")
            subprocess.run([
                'convert', '-background', bg_color, '-fill', bars_color, '-font', '/src/fonts/Roboto-Black.ttf',
                '-pointsize', '48', '-size', '900x367', '-gravity', 'center', f'caption:{caption_text}',
                '-bordercolor', bg_color, '-border', '40', background_image_path
            ], check=True)

            print("Overlaying the image on the padded waveform video...")
            subprocess.run([
                'ffmpeg', '-y', '-i', padded_waveform_path, '-i', background_image_path,
                '-filter_complex', 'overlay=0:0', final_video_path
            ], check=True)

        return final_video_path

# Gradio user interface
def gradio_predict(audio, bg_color, fg_alpha, bars_color, bar_count, bar_width, caption_text):
    predictor = Predictor()
    result = predictor.predict(
        audio=audio,
        bg_color=bg_color,
        fg_alpha=fg_alpha,
        bars_color=bars_color,
        bar_count=bar_count,
        bar_width=bar_width,
        caption_text=caption_text
    )
    return result

# Launch Gradio interface
interface = gr.Interface(
    fn=gradio_predict,
    inputs=[
        gr.Audio(source="upload", type="filepath", label="Audio File"),
        gr.Textbox(value="#000000", label="Background Color"),
        gr.Slider(0, 1, value=0.75, label="Foreground Opacity"),
        gr.ColorPicker(value="#ffffff", label="Bars Color"),
        gr.Slider(10, 500, value=100, step=1, label="Number of Bars"),
        gr.Slider(0, 1, value=0.4, step=0.1, label="Bar Width"),
        gr.Textbox(value="", label="Caption Text")
    ],
    outputs=gr.Video(label="Waveform Video"),
    live=False
)

if __name__ == "__main__":
    print("Starting Gradio interface...")
    interface.launch(server_name="0.0.0.0", server_port=7860)