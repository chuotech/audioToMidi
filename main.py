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
    converter.save_midi(notes, "output.mid", converter.get_tempo('output.wav'))
    print(converter.get_tempo('output.wav'))
# y,sr = librosa.load('output.wav', duration = 10)

# onset_env = librosa.onset.onset_strength(y=y, sr=sr)
# tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)
# print(tempo)

if __name__ == "__main__":
    main()