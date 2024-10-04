import librosa
import numpy as np
import mido
from mido import Message, MidiFile, MidiTrack

try:
    y,sr = librosa.load('output.wav')
except:
    print("Audio file not found")
    exit()
y_harmonic, y_percussive = librosa.effects.hpss(y)

pitches, voiced_flags, voiced_probs = librosa.pyin(y_harmonic, fmin=librosa.note_to_hz('E2'), fmax=librosa.note_to_hz('E7'))

midi_notes = librosa.hz_to_midi(pitches)

midi_notes_filtered = midi_notes[~np.isnan(midi_notes)]
midi_notes_filtered = midi_notes_filtered[(midi_notes_filtered >= 21) & (midi_notes_filtered <= 100)]

note_names = librosa.midi_to_note(midi_notes_filtered)

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

merged_notes = []
previous_note = None
current_duration = 0
for note in midi_notes_filtered:
    
    if note == previous_note:
        current_duration += 720
    else:
        if previous_note is not None:
            merged_notes.append((previous_note, current_duration))
        previous_note = note
        current_duration = 480
if previous_note is not None:
    merged_notes.append((previous_note, current_duration))
for note, duration in merged_notes:
    track.append(Message('note_on', note=int(note), velocity=64, time=0))
    # Note off message
    track.append(Message('note_off', note=int(note), velocity=64, time=duration))
    # if merged_notes and merged_notes[-1] == note:
    #     last_note = merged_notes.pop()
    #     merged_notes.append((note, 720))
    # else:
    #     merged_notes.append((note, 480))
    # if int(note) not in added_notes:
    #     track.append(Message('note_on', note=int(note), velocity=64, time=0))
    #     track.append(Message('note_off', note=int(note), velocity=64, time=480))
    #     track.append(Message('note_off', note=int(note), velocity=0, time=240))
    #     added_notes.add(int(note))

mid.save('output.mid')

print("MIDI file saved as 'output.mid'")
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