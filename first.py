import wave
import pyaudio
import math

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"
audio = pyaudio.PyAudio()

print("Record Device List:")
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if (audio.get_device_info_by_host_api_device_index(0,i).get("maxInputChannels")) > 0:
        print("Input Device ID: ",  i, ", ", audio.get_device_info_by_host_api_device_index(0,i).get("name"))
index = int(input())
print("Recording with: "+str(index))
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=index, frames_per_buffer=CHUNK)
print("Recording...")
Recordframes = []
for i in range(0, math.ceil(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    Recordframes.append(data)
print("Recording Finished!")
stream.stop_stream()
stream.close()
audio.terminate()


with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(Recordframes))
print(f"Audio saved as {WAVE_OUTPUT_FILENAME}")