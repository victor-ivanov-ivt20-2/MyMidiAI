import mido

from midi import Midi
def main():
    input_midi = mido.MidiFile('./midi/histo.mid', clip=True)
    mid = Midi(input_midi)
    mid.analyze()
    mid.save()

if __name__ == '__main__':
    main()