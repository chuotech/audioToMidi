from audioInput import inputAudio
from fileToMidi import AudioMidiConverter
import librosa

def main():
    ad = inputAudio()
    ad.start()
    ad.outputWav()
    converter = AudioMidiConverter()
    audio_data, _ = librosa.load("output.wav", sr=converter.sr)
    notes = converter.convert(audio_data)
    converter.save_midi(notes, "output.mid")
    


if __name__ == "__main__":
    main()