from audioInput import inputAudio
from fileToMidi import AudioMidiConverter
import librosa

def main():
    ad = inputAudio()
    ad.start()
    ad.outputWav()
    # converter = AudioMidiConverter()
    # audio_data, _ = librosa.load("output.wav", sr=converter.sr)
    # notes = converter.convert(audio_data)
    # print("What instrument for output MIDI?\n0: Bass\n1: Guitar\n2: Rhythm")
    # program_name = int(input())
    # converter.save_midi(notes, "output.mid", program_name, converter.get_tempo('output.wav'))
    # print(converter.get_tempo('output.wav'))

if __name__ == "__main__":
    main()