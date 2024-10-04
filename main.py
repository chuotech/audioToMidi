from audioInput import inputAudio
from fileToMidi import audioToMidi

def main():
    # ad = inputAudio()
    # ad.start()
    # ad.outputWav()
    am = audioToMidi('output.wav', 'output.mid')
    am.process()
    


if __name__ == "__main__":
    main()