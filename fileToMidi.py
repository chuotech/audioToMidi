import librosa
import numpy as np
import mido
import pretty_midi
from mido import Message, MidiFile, MidiTrack


class Note:
    def __init__(self, velocity, midi_note, start, end):
        self.velocity = velocity
        self.midi_note = midi_note
        self.start = start
        self.end = end

class AudioMidiConverter:
    def __init__(self, raga_map=None, root='E5', sr=16000, note_min='B1', note_max='E5', frame_size=2048,
                 hop_length=441, outlier_coeff=2):
        self.fmin = librosa.note_to_hz(note_min)
        self.fmax = librosa.note_to_hz(note_max)
        self.hop_length = hop_length
        self.frame_size = frame_size
        self.raga_map = np.array(raga_map) if raga_map else None
        self.sr = sr
        self.root = librosa.note_to_midi(root)
        self.m = outlier_coeff
        self.empty_arr = np.array([])

    def convert(self, y, return_onsets=False, velocity=100):
        f0, voiced_flag, voiced_prob = librosa.pyin(y, fmin=self.fmin * 0.9, fmax=self.fmax * 1.1, sr=self.sr,
                                                    frame_length=self.frame_size, hop_length=self.hop_length)
        if len(f0) == 0:
            print("No f0")
            if return_onsets:
                return self.empty_arr, self.empty_arr
            return self.empty_arr

        pitch = librosa.hz_to_midi(f0)
        pitch[np.isnan(pitch)] = 0
        onsets = self.get_onsets(y)
        notes = np.zeros(len(onsets), dtype=int)
        for i in range(len(onsets) - 1):
            notes[i] = np.round(np.nanmedian(pitch[onsets[i]: onsets[i + 1]]))
        notes[-1] = np.round(np.nanmedian(pitch[onsets[-1]:]))

        onsets = onsets[notes > 0] * self.hop_length / self.sr
        notes = notes[notes > 0]

        if len(notes) > 0:
            if self.raga_map is not None:
                notes = self.filter_raga(notes)
            notes = self.fix_outliers(notes, m=self.m)

        temp = []
        for i in range(len(notes)):
            temp.append(Note(velocity, notes[i], start=onsets[i], end=onsets[i] + 0.1))

        if return_onsets:
            return temp, onsets

        return temp

    def save_midi(self, notes, filename, tempo):
        midi_data = pretty_midi.PrettyMIDI()

    # Create an Instrument instance (for example, Piano)
        instrument = pretty_midi.Instrument(program=35)  # Change to desired instrument

    # Set the tempo

    # Define ticks per beat
        ticks_per_beat = 30  # This should match your previous setup

        # Create notes
        for note in notes:
            # Use pretty_midi to create Note objects
            start_time = note.start
            end_time = note.end

        # Create a Note object with the MIDI note number, start and end times
            midi_note = pretty_midi.Note(
                velocity=note.velocity,
                pitch=note.midi_note,
                start=start_time,
                end=end_time
            )

        # Add the note to the instrument
            instrument.notes.append(midi_note)

     # Add the instrument to the PrettyMIDI object
        midi_data.instruments.append(instrument)

        # Write the MIDI data to a file
        midi_data.write(filename)
        print(f"MIDI file saved as: {filename}")
        # """Save the detected notes to a MIDI file."""
        # midi_file = MidiFile()
        # track = MidiTrack()
        # midi_file.tracks.append(track)

        # # Add a program change (set instrument)
        # track.append(mido.Message('program_change', program=35))  # Change to desired instrument

        # ticks_per_beat = 60  # Example ticks per beat
        # seconds_per_beat = 60.0 / tempo # Assuming a default tempo of 120 BPM

        # for note in notes:
        #     note_start_tick = int(note.start / seconds_per_beat * ticks_per_beat)
        #     note_end_tick = int(note.end / seconds_per_beat * ticks_per_beat)

        #     track.append(mido.Message('note_on', note=note.midi_note, velocity=note.velocity, time=note_start_tick))
        #     track.append(mido.Message('note_off', note=note.midi_note, velocity=note.velocity, time=note_end_tick))

        # midi_file.save(filename)
        # print(f"MIDI file saved as: {filename}")

    def filter_raga(self, _notes):
        filtered_notes = _notes.copy()
        _n = _notes - self.root
        code = (_n + 12) % 12
        filtered_notes = filtered_notes[self.raga_map[code] == 1]
        return filtered_notes

    def get_onsets(self, y, threshold=0.01):
        onset_env = librosa.onset.onset_strength(y=y, sr=self.sr, hop_length=self.hop_length)
        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=self.sr, hop_length=self.hop_length, backtrack=True)
        return np.unique(np.hstack([0, onsets]))

    def fix_outliers(self, notes, m):
        median = np.median(notes)
        mad = np.median(np.abs(notes - median))
        lower_bound = median - m * mad
        upper_bound = median + m * mad
        return notes[(notes >= lower_bound) & (notes <= upper_bound)]

    @staticmethod
    def get_tempo(filename):
        y,sr = librosa.load(filename, duration = 10)

        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)
        return tempo[0]
    # def process(self):
    #     """Complete processing from audio to MIDI."""
    #     self.load_audio()
    #     self.detect_onsets()
    #     self.convert_to_midi()
    #     self.save_midi()

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