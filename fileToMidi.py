import librosa
import numpy as np
import mido
from collections.abc import MutableSequence
from madmom.features import CNNOnsetProcessor, OnsetPeakPickingProcessor
from mido import Message, MidiFile, MidiTrack

class audioToMidi():
    def __init__(self, wav_file, midi_file, tempo=120):
        self.wav_file = wav_file
        self.midi_file = midi_file
        self.tempo = tempo
        self.sr = None
        self.y = None
        self.onset_times = None

    def load_audio(self):
        """Load the audio file."""
        self.y, self.sr = librosa.load(self.wav_file)
        print(f"Loaded audio file: {self.wav_file}")

    def detect_onsets(self):
        """Detect onsets in the audio file."""
        onset_processor = CNNOnsetProcessor()
        onset_probs = onset_processor(self.y)
        self.onset_times = OnsetPeakPickingProcessor(threshold=0.1)(onset_probs)
        print(f"Detected {len(self.onset_times)} onsets.")

    def convert_to_midi(self):
        """Convert the detected onsets to MIDI format."""
        midi = mido.MidiFile()
        track = mido.MidiTrack()
        midi.tracks.append(track)

        # Add a program change (set instrument)
        track.append(mido.Message('program_change', program=24))  # Change to desired instrument

        for onset_time in self.onset_times:
            ticks = int(onset_time * self.sr / 2)  # Adjust based on your desired ticks per beat
            note = 60  # Fixed note (Middle C) for demonstration; you can enhance this.
            track.append(mido.Message('note_on', note=note, velocity=64, time=ticks))
            track.append(mido.Message('note_off', note=note, velocity=64, time=ticks + 100))  # Note duration

        self.midi = midi
        print(f"Converted to MIDI format.")

    def save_midi(self):
        """Save the MIDI file to disk."""
        self.midi.save(self.midi_file)
        print(f'MIDI file saved as: {self.midi_file}')

    def process(self):
        """Complete processing from audio to MIDI."""
        self.load_audio()
        self.detect_onsets()
        self.convert_to_midi()
        self.save_midi()

# try:
#     y,sr = librosa.load('output.wav')
# except:
#     print("Audio file not found")
#     exit()
# y_harmonic, y_percussive = librosa.effects.hpss(y)

# pitches, voiced_flags, voiced_probs = librosa.pyin(y_harmonic, fmin=librosa.note_to_hz('E2'), fmax=librosa.note_to_hz('E7'))

# midi_notes = librosa.hz_to_midi(pitches)

# midi_notes_filtered = midi_notes[~np.isnan(midi_notes)]
# midi_notes_filtered = midi_notes_filtered[(midi_notes_filtered >= 21) & (midi_notes_filtered <= 100)]

# note_names = librosa.midi_to_note(midi_notes_filtered)

# mid = MidiFile()
# track = MidiTrack()
# mid.tracks.append(track)

# merged_notes = []
# previous_note = None
# current_duration = 0
# for note in midi_notes_filtered:
    
#     if note == previous_note:
#         current_duration += 720
#     else:
#         if previous_note is not None:
#             merged_notes.append((previous_note, current_duration))
#         previous_note = note
#         current_duration = 480
# if previous_note is not None:
#     merged_notes.append((previous_note, current_duration))
# for note, duration in merged_notes:
#     track.append(Message('note_on', note=int(note), velocity=64, time=0))
#     # Note off message
#     track.append(Message('note_off', note=int(note), velocity=64, time=duration))
#     # if merged_notes and merged_notes[-1] == note:
#     #     last_note = merged_notes.pop()
#     #     merged_notes.append((note, 720))
#     # else:
#     #     merged_notes.append((note, 480))
#     # if int(note) not in added_notes:
#     #     track.append(Message('note_on', note=int(note), velocity=64, time=0))
#     #     track.append(Message('note_off', note=int(note), velocity=64, time=480))
#     #     track.append(Message('note_off', note=int(note), velocity=0, time=240))
#     #     added_notes.add(int(note))

# mid.save('output.mid')

# print("MIDI file saved as 'output.mid'")
# print(note_names)
# # Beat tracking example
# import librosa
# import numpy as np

# # Step 1: Load the audio file
# y, sr = librosa.load(librosa.ex('trumpet'))
# # This is the actual audio: https://freesound.org/people/sorohanro/sounds/77711/
# # You might consider finding a simpler melody, but monophonic files like this are good

# # Step 2: Harmonic-Percussive Source Separation (optional, but helps in isolating pitch)
# y_harmonic, y_percussive = librosa.effects.hpss(y)

# # Step 3: Perform pitch tracking
# # librosa uses a method called `pyin` (Probabilistic YIN)
# # It estimates the pitch for each frame
# pitches, voiced_flags, voiced_probs = librosa.pyin(y_harmonic, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

# # Step 4: Convert frequencies (Hz) to musical notes
# # librosa provides a utility to map frequencies to MIDI note numbers
# midi_notes = librosa.hz_to_midi(pitches)

# # Filter out unvoiced frames
# midi_notes_filtered = midi_notes[~np.isnan(midi_notes)]

# # Step 5: Convert MIDI numbers to note names
# note_names = librosa.midi_to_note(midi_notes_filtered)

# # Output the notes
# print(note_names)