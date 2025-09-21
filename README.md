# Auto Subtitle Generator

This script automatically generates subtitles for video files using OpenAI's Whisper speech-to-text model.

## Features

- Extracts audio from video files.
- Transcribes the audio to text using Whisper.
- Generates subtitle files in SRT format.
- Processes a single video file or an entire directory of videos.
- Supports multiple Whisper models (tiny, base, small, medium, large).
- GPU (CUDA) acceleration for faster transcription.

## Setup

It is recommended to use a virtual environment to install the dependencies.

### Using `venv`

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install the required libraries from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### Using `conda`

1. Create a conda environment:
   ```bash
   conda create --name auto-subtitle python=3.10
   ```

2. Activate the conda environment:
   ```bash
   conda activate auto-subtitle
   ```

3. Install the required libraries from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

**Note:** You also need to have FFmpeg installed on your system. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html) or install it using a package manager like `apt` or `brew`. For GPU acceleration, you will also need to have a compatible version of PyTorch with CUDA support installed.


## Usage

To generate subtitles for a single video file:

```bash
python main.py /path/to/your/video.mp4
```

To generate subtitles for all video files in a directory:

```bash
python main.py /path/to/your/directory/
```

### Optional Arguments

You can also specify the Whisper model to use and an initial prompt.

**Model:**

The available models are `tiny`, `base`, `small`, `medium`, and `large`. The default model is `medium`.

```bash
python main.py /path/to/your/video.mp4 small
```

**Prompt:**

You can provide an initial prompt to the model to improve the transcription quality.

```bash
python main.py /path/to/your/video.mp4 medium "This is a video about Python programming."
```

## License

This project is licensed under the MIT License.
