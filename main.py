from audioInput import inputAudio
from fileToMidi import AudioMidiConverter
import librosa
# from ISMIRLCVR.chord_recognition import chord_recognition
def main():
    ad = inputAudio()
    ad.start()
    ad.outputWav()
    # chords = [[0.0, 0.7198185941043084, 'N'], 
    #           [0.7198185941043084, 4.504671201814059, 'F:maj'], 1
    #           [4.504671201814059, 8.893242630385489, 'C:maj'], 
    #           [8.893242630385489, 12.051156462585034, 'E:maj']]
    # converter = AudioMidiConverter()
    # converter.chord_transcription(chords)
    # audio_data, _ = librosa.load("output.wav", sr=converter.sr)
    # notes = converter.convert(audio_data)
    # print("What instrument for output MIDI?\n0: Bass\n1: Guitar\n2: Rhythm")
    # program_name = int(input())
    # converter.save_midi(notes, "output.mid", program_name, converter.get_tempo('output.wav'))
    # print(converter.get_tempo('metronome-loop-46242.mp3'))

if __name__ == "__main__":
    main()