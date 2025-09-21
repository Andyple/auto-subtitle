import os
import sys
from moviepy import AudioFileClip
import whisper
import time
from pathlib import Path

def extract_audio(video_path, audio_path):
    """Extract audio from video file and save as WAV"""
    try:
        video = AudioFileClip(video_path)
        video.write_audiofile(audio_path, codec='pcm_s16le')
        return True
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")
        return False

def transcribe_audio(audio_path, model_name='medium', device='cuda', prompt=None):
    """Transcribe audio using Whisper AI model with GPU support"""
    try:
        model = whisper.load_model(model_name, device=device)
        result = model.transcribe(audio_path, fp16=True, initial_prompt=prompt)
        return result["segments"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def format_time(seconds):
    """Convert seconds to SRT time format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')

def create_subtitle_file(segments, output_path):
    """Create SRT subtitle file from segments"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                start = segment['start']
                end = segment['end']
                text = segment['text'].strip()
                
                f.write(f"{i}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{text}\n\n")
        return True
    except Exception as e:
        print(f"Error creating subtitle file: {e}")
        return False

def process_video_file(video_path, model_name='medium', prompt=None):
    """Process a single video file to generate subtitles"""
    print(f"\nProcessing: {video_path}")
    
    base_name = os.path.splitext(video_path)[0]
    srt_path = f"{base_name}.srt"
    
    if os.path.exists(srt_path):
        print(f"Subtitles already exist: {srt_path}")
        return True

    temp_dir = os.path.dirname(video_path)
    audio_path = os.path.join(temp_dir, "temp_audio.wav")
    
    if not extract_audio(video_path, audio_path):
        return False

    segments = transcribe_audio(audio_path, model_name, prompt=prompt)
    if not segments:
        os.remove(audio_path)
        return False

    success = create_subtitle_file(segments, srt_path)
    os.remove(audio_path)
    
    if success:
        print(f"Successfully created subtitles: {srt_path}")
    return success


def process_directory(root_dir, model_name='medium', prompt=None):
    """Recursively process all video files in directory"""
    video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv')
    processed_files = 0
    skipped_files = 0
    failed_files = 0
    
    print(f"\nScanning directory: {root_dir}")
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(video_extensions):
                video_path = os.path.join(root, file)
                if process_video_file(video_path, model_name, prompt):
                    processed_files += 1
                else:
                    failed_files += 1
            else:
                skipped_files += 1
    
    print("\nProcessing complete!")
    print(f"Total videos found: {processed_files + failed_files}")
    print(f"Successfully processed: {processed_files}")
    print(f"Failed to process: {failed_files}")
    print(f"Skipped non-video files: {skipped_files}")

def main():
    start_time = time.time()
    if len(sys.argv) < 2:
        print("Usage: python video_subtitler.py <directory_or_file> [model_name] [prompt]")
        print("Available models: tiny, base, small, medium, large")
        sys.exit(1)

    target_path = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else 'medium'
    prompt = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(target_path):
        print(f"Error: Path not found - {target_path}")
        sys.exit(1)

    if os.path.isfile(target_path):
        process_video_file(target_path, model_name, prompt)
    else:
        process_directory(target_path, model_name, prompt)
    end_time = time.time()
    elapsed = end_time - start_time
    minutes, seconds = divmod(elapsed, 60)
    print(f"\nTotal processing time: {int(minutes)} minutes {seconds:.2f} seconds")


if __name__ == "__main__":
    main()