import os
import pyaudio
import wave
from pydub import AudioSegment
import asyncio
from shazamio import Shazam

# Parameters for recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "mic_recording.wav"

# Function to record audio from microphone
def record_audio_from_mic():
    audio = pyaudio.PyAudio()

    # Open the audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print(f"Recording audio from microphone for {RECORD_SECONDS} seconds...")

    frames = []

    # Capture audio in chunks for the specified duration
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording complete.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data to a .wav file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Load the .wav file into an AudioSegment object
    return AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)

# Function to save snippet of the audio
def save_snippet(audio_segment, duration_ms=5000):
    snippet = audio_segment[:duration_ms]
    snippet_path = os.path.abspath("snippet.wav")  # Get full path to snippet.wav
    snippet.export(snippet_path, format="wav")
    print(f"Snippet saved as '{snippet_path}'.")
    return snippet_path

# Asynchronous function to recognize the song using Shazamio
async def recognize_song(filename):
    if os.path.exists(filename):  # Check if the file exists before calling Shazamio
        shazam = Shazam()
        print(f"Identifying song from file: {filename}")
        out = await shazam.recognize(r'C:\Users\Tristen Dsouza\Desktop\snippet.wav')
        if out and "track" in out:
            print("Song found!")
            print(f"Song: {out['track']['title']}")
            print(f"Artist: {out['track']['subtitle']}")
        else:
            print("Song not recognized.")
    else:
        print(f"File '{filename}' does not exist!")

if __name__ == "__main__":
    # Record audio from the microphone
    recorded_audio = record_audio_from_mic()

    # Save the first 5 seconds as a snippet
    snippet_filename = save_snippet(recorded_audio)

    # Print the snippet path (for debugging purposes)
    print(f"Snippet filename: {snippet_filename}")

    # Run async song recognition function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(recognize_song(snippet_filename))
