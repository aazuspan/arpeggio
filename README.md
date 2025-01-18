[![Build status](https://github.com/aazuspan/arpeggio/actions/workflows/ci.yaml/badge.svg)](https://github.com/aazuspan/arpeggio/actions/workflows/ci.yaml)

# Arpeggio

A toy domain-specific language and interpreter for music synthesis.

## The Language

Arpeggio source code is written in an `arp` file. Each `arp` file corresponds to a **song**. Songs are composed of one or more **tracks**. Tracks are composed of one or more **lines**. Lines are composed of one or more **notes**. A simple song with one track and one line of four notes can be written as:

```
track
    | 1 2 3 4
end
```

### Musical Notation

Arpeggio songs are composed in diatonic keys. Notes are referenced by their integer **interval** within the chosen key. For example, in the default key of C major, the melody `1 2 3 4` plays the first, second, third, and fourth interval: `C D E F`. Any integer interval or **rest** `&` is a valid note. The timing and octave of notes can be modified by adding suffixes.

#### Note Duration

Each note is held for one sixteenth note based on the song tempo. Notes can be extended an additional sixteenth note with a **continue** `.` symbol. For example, the following plays four quarter notes:

```
    | 1 . . . 1 . . . 1 . . . 1 . . .
```

#### Note Octave

The octave of a note can be modified by following it with an **octave modifier** `_ - + *`. For example, the following line plays two octaves below and above middle C:

```
    | 1_. . . 1-. . . 1+. . . 1*. . .
```

#### Lines and Repeats

Lines can be repeated by placing a **repeat modifier** at the end. The following plays a descending C major scale four times:

```
    | 1+. 7 . 6 . 5 . 4 . 3 . 2 . 1 . [x4]
```

Lines can be any length. For readability, it usually makes sense to split lines at the end of the measure, and to make all lines the same length so that notes line up vertically.

The key and tempo of a song are adjustable through [configuration options](#configuration). Time signatures in Arpeggio are defined only by how the user arranges beats; there's no built-in concept of a measure.

### Syntax

Arpeggio programs have a top-level global scope where song configuration is defined track blocks are created. For example:

```
@bpm 90

track
    | 1 2 3 4
end
```

`@bpm 90` marks a song-level configuration option named `bpm` with a value `90`, which sets the tempo of the song. 

Everything between `track` and `end` is a **track block**. A track block can include track-level configuration and lines of notes. Lines begin with a `|` and contain notes as integer intervals or rests `&`. Notes can be followed by modifiers like `+` or continue `.` symbols. Lines can optionally end with a repeat symbol `[xN]`, where N is the number of times to repeat the line.

Comments begin with a `~` and are ignored by the parser. Whitespace is used for aesthetics and lining up notes, but is ignored by the parser. 

Here's a valid program that uses all of these syntax features:

```
@bpm 120

~ This is the melody track
track
    @instrument triangle

    | 3+2+1+. 6 & 5 . [x3]
    | 3 . 2 . . . 1 .
end


~ This track plays chords
track
    @chords

    | & & 1 & & & 1 & [x3]
    | & & 2 . . . 1 &
end
```

### Configuration

Song- and track-level options are configurable with `@` options placed in the appropriate scope.

#### Song Configuration

- `@key`: The musical key to play the song in, written as `tonic_mode`, e.g. `F#_minor`. Supported modes are Major (Ionian), Minor (Aeolian), Dorian, Phrygian, Lydian, Mixolydian, Locrian, Harmonic minor, and Melodic minor.
- `@bpm`: The song tempo in beats per minute. This sets the duration of a sixteenth note.
- `@loop`: The number of times to repeat the entire song.

#### Track Configuration

- `@instrument`: The name of the instrument to use. Supported instruments are sine, square, sawtooth, triangle, and noise. Sine is used by default.
- `@volume`: The volume modifier, between -infinity and zero.
- `@pan`: The stereo panning of the track, between -1 (left) and 1 (right).
- `@octave`: An octave offset to apply to all notes and chords.
- `@loop`: The number of times to repeat the track.
- `@offset`: The number of sixteenths to delay the track start.

The following options are flags that don't require a value.

- `@chords`: Play triad chords instead of notes.
- `@staccato`: Play notes for half their duration.
- `@mute`: Mute the track.
- `@solo`: Only play this and other soloed tracks.

## The Interpreter

### Installation

The interpreter and audio engine are written in Python. Make sure Python is installed, then run:

```bash
pip install git+https://github.com/aazuspan/arpeggio
```

Arpeggio uses [simpleaudio](https://simpleaudio.readthedocs.io/en/latest/index.html) for playback, which may require additional dependencies to install. See their [installation guide](https://simpleaudio.readthedocs.io/en/latest/installation.html) for specifics.

### Usage

Run `arpeggio --help` for a list of available commands. The interpreter can play a song from an `arp` file with:

```bash
arpeggio play song.arp
```

Compile a song to WAV with:

```bash
arpeggio compile song.arp song.wav
```

Enable watch mode with `-w` to automatically reload the song file when it changes:

```bash
arpeggio play song.arp -w
```