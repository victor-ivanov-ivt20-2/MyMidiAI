import mido as md


class Midi:
    ticks = 480
    tempo = 500000
    messages = []
    def __init__(self, input_midi):
        self.input_midi = input_midi

    def secondsToTicks(self, time, ticks, tempo):
        return int(round(md.second2tick(time, ticks, tempo)))

    def analyze(self):
        for msg in self.input_midi:
            tick = self.secondsToTicks(msg.time, self.ticks, self.tempo)
            if not msg.is_meta and (msg.type == 'note_on' or msg.type == 'note_off'):
                self.messages.append(md.Message(
                    msg.type, channel=msg.channel, note=msg.note, velocity=msg.velocity, time=tick))
            elif (msg.type == 'set_tempo'):
                self.tempo = msg.tempo
                self.messages.append(md.MetaMessage(
                    'set_tempo', tempo=self.tempo, time=tick))
            elif (msg.type == 'time_signature'):
                self.ticks = msg.numerator * 120
        self.messages.append(md.MetaMessage('end_of_track', time=tick))
    
    def save(self):
        output_midi = md.MidiFile()
        track = md.MidiTrack()
        output_midi.tracks.append(track)
        for msg in self.messages:
            track.append(msg)
        output_midi.save('./generated_midi/new_midi.mid')