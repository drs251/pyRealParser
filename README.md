# pyRealParser
A Python package to read [songs in the iRealPro format](https://www.irealb.com/forums/forumdisplay.php?3-Songs).

## Introduction & Usage
Here's an example of how to import an iReal link and print the information it contains:

```python
>from pyRealParser import Tune
>my_tune = Tune.parse_ireal_url('irealb://%44%65%61%72<link shortened>')[0]
>print(my_tune)

<pyRealParser.Tune object at 0x107305e80>
Title: Dear Old Stockholm
Composer: Traditional
Style: Medium Swing
Key: D-
Transpose: None
Comp style: 0
BPM: 0
Repeats: None
Time signature: 4/4

Chord string:
*A{T44D- |Eh7 A7b9|G-7 C7|F^7 |Eh7 A7b9|D- |Eh7 |A7b9 |D-7 |D-6 |D-7 |D-6 }*B[F^7 |G-7 C7|F^7 |Eh7 A7b9 ]*C[D- |Eh7 A7b9|G-7 C7|F^7 |Eh7 A7b9|D- |C7sus |x |C7sus |x |x |x |C7sus A7b9|D- <As played by Miles Davis>|x

Flattened measures:
| D-          | Eh7A7b9     | G-7C7       | F^7         |
| Eh7A7b9     | D-          | Eh7         | A7b9        |
| D-7         | D-6         | D-7         | D-6         |
| D-          | Eh7A7b9     | G-7C7       | F^7         |
| Eh7A7b9     | D-          | Eh7         | A7b9        |
| D-7         | D-6         | D-7         | D-6         |
| F^7         | G-7C7       | F^7         | Eh7A7b9     |
| D-          | Eh7A7b9     | G-7C7       | F^7         |
| Eh7A7b9     | D-          | C7sus       | C7sus       |
| C7sus       | C7sus       | C7sus       | C7sus       |
| C7susA7b9   | D-          | D-          |
```

`parse_ireal_url`returns a list of `Tune` objects, each representing a song contained in the input url. They contain a number of member variables, containing the chords as well as some meta information:

- `chord_string`: A single string that has all chords of the tune, with bar lines, repeat markers, endings, codas etc:

```python
>print(my_tune.chord_string)

*A{T44D- |Eh7 A7b9|G-7 C7|F^7 |Eh7 A7b9|D- |Eh7 |A7b9 |D-7 |D-6 |D-7 |D-6 }*B[F^7 |G-7 C7|F^7 |Eh7 A7b9 ]*C[D- |Eh7 A7b9|G-7 C7|F^7 |Eh7 A7b9|D- |C7sus |x |C7sus |x |x |x |C7sus A7b9|D- <As played by Miles Davis>|x
```

- `measures_as_strings`: A list, for which every element corresponds to a single bar, containing the chords in string form. Repeats, codas etc. have been flattened.

```python
>print(my_tune.measures_as_strings)

*['D-', 'Eh7A7b9', 'G-7C7', 'F^7', 'Eh7A7b9', 'D-', 'Eh7', 'A7b9', 'D-7', 'D-6', 'D-7', 'D-6', 'D-', 'Eh7A7b9', 'G-7C7', 'F^7', 'Eh7A7b9', 'D-', 'Eh7', 'A7b9', 'D-7', 'D-6', 'D-7', 'D-6', 'F^7', 'G-7C7', 'F^7', 'Eh7A7b9', 'D-', 'Eh7A7b9', 'G-7C7', 'F^7', 'Eh7A7b9', 'D-', 'C7sus', 'C7sus', 'C7sus', 'C7sus', 'C7sus', 'C7sus', 'C7susA7b9', 'D-', 'D-']
```

- `title`: The title
- `composer`: The composer
- `style`: The style (e.g. 'Swing', 'Bossa', 'Blues' etc.)
- `key`: The key (e.g. 'A', 'F#' etc)
- `transpose`: How many semitones to transpose
- `comp_style`: Accompaniment style (usually empty)
- `bpm`: Tempo in BPM (usually empty)
- `repeats`: How many repeats (usually empty)
- `time_signature`: Time signature as a tuple (e.g. (3,4), (4, 4), (5, 8) etc.)

Notice, that some of these meta-data fields might be empty, depending on the input url.

`Tune` objects are designed to have a nice textual representation in Jupyter notebooks, but can be used outside of a notebook perfectly well.

For more documentation, please read the code.

Contributions are welcome, please submit a PR.

## Installation

```
pip install pyRealParser
```

## Acknowledgements
Kudos to [@pianosnake](https://github.com/pianosnake/ireal-reader) and [@ironss](https://github.com/ironss/accompaniser) for figuring out the iReal url format!
