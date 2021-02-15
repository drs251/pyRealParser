import re
import urllib.parse
import itertools

__license__ = 'MIT'
__docformat__ = 'reStructuredText'


class Tune(object):
    """Represents the chords in a song, with functionality to import the iReal format.

    :ivar chord_string: A single string that has all chords of the tune, with bar lines, repeat markers, endings,
       codas etc.
    :ivar measures_as_strings: A list, for which every element corresponds to a single bar, containing the chords in
       string form. Repeats, codas etc. have been flattened.
    :ivar title: The title
    :ivar composer: The composer
    :ivar style: The style (e.g. 'Swing', 'Bossa', 'Blues' etc.)
    :ivar key: The key (e.g. 'A', 'F#' etc)
    :ivar transpose: How many semitones to transpose
    :ivar comp_style: Accompaniment style (usually empty)
    :ivar bpm: Tempo in BPM (usually empty)
    :ivar repeats: How many repeats (usually empty)
    :ivar time_signature: Time signature as a tuple (e.g. (3,4), (4, 4), (5, 8) etc.)


    Notice, that some of these meta-data fields might
    be empty, depending on the input url.
    """

    _chords_prefix = """1r34LbKcu7"""

    chord_regex = re.compile(r'(?<!/)([A-GNn][^A-GN/]*(?:/[A-GN][#b]?)?)')

    @classmethod
    def _obfusc50(cls, block):
        """Unscrambles blocks of 50 by character substitution

        :param block: A string of 50 characters
        :return: An unscrambled string
        """
        result = list(block)
        # switch first 5 characters with last 5
        for i in range(5):
            result[i] = block[49 - i]
            result[49 - i] = block[i]
        # switch characters 10-24 like before:
        for i in range(10, 24):
            result[i] = block[49 - i]
            result[49 - i] = block[i]
        return ''.join(result)

    @classmethod
    def _unscramble_chord_string(cls, scrambled_string):
        """Unscrambles a single song in iReal's crazy format (Kudos to ironss and pianosnake for
        figuring this out!)
        :param scrambled_string: A scrambled chord string, corresponding to one tune
        :return: An unscrambled chord string.
        """
        unscrambled = ""
        while len(scrambled_string) > 50:
            temp = scrambled_string[:50]
            scrambled_string = scrambled_string[50:]
            if len(scrambled_string) < 2:
                unscrambled += temp
            else:
                unscrambled += cls._obfusc50(temp)
        unscrambled += scrambled_string
        return unscrambled

    @classmethod
    def _cleanup_chord_string(cls, chord_string):
        """Removes excessive whitespace, unnecessary stuff, empty measures etc. and return a nice,
        readable string
        :param chord_string: unscrambled chords in string form
        :return: cleaned up chord string
        """
        # unify symbol for new measure to |
        chord_string = re.sub(r'LZ|K', '|', chord_string)
        # unify symbol for no chord to n
        # chord_string = re.sub(r'[np]', 'n', chord_string)
        # unify symbol for one-bar repeat to x
        chord_string = re.sub(r'cl', 'x', chord_string)
        # remove stars with empty space in between
        chord_string = re.sub(r'\*\s*\*', '', chord_string)
        # remove vertical spacers
        chord_string = re.sub(r'Y+', '', chord_string)
        # remove empty space
        chord_string = re.sub(r'XyQ|,', ' ', chord_string)
        # remove empty measures
        chord_string = re.sub(r'\|\s*\|', '|', chord_string)
        # remove end markers
        chord_string = re.sub(r'Z', '', chord_string)
        # remove spaces behing bar lines
        chord_string = re.sub(r'\|\s+', '|', chord_string)
        # remove multiple white-spaces
        chord_string = re.sub(r'\s+', ' ', chord_string)
        # remove trailing white-space
        chord_string = chord_string.rstrip()
        return chord_string

    @classmethod
    def _remove_annotations(cls, chord_string):
        """Removes comments, section markers, alternative chords, time signatures etc.
        :param chord_string: A chord string
        :return: A cleaned up chord string
        """
        # unify symbol for new measure to |
        chord_string = re.sub(r'[\[\]]', '|', chord_string)
        # remove empty measures
        chord_string = re.sub(r'\|\s*\|', '|', chord_string)
        # remove comments
        chord_string = re.sub(r'<.*?>', '', chord_string)
        # remove alternative chords
        chord_string = re.sub(r'\([^)]*\)', '', chord_string)
        # remove unneeded single f (fermata)
        chord_string = re.sub(r'f', '', chord_string)
        # remove l unless it's part of an alt chord
        chord_string = re.sub(r'(?<!a)l(?!t)', '', chord_string)
        # remove s (for 'small), unless it's part of a sus chord
        chord_string = re.sub(r'(?<!su)s(?!us)', '', chord_string)
        # remove section markers
        chord_string = re.sub(r'\*\w', '', chord_string)
        # remove time signatures
        chord_string = re.sub(r'T\d+', '', chord_string)
        # remove the star that's sometimes after augmented chords
        chord_string = re.sub(r'\+\*', '+', chord_string)
        return chord_string

    @classmethod
    def _remove_markers(cls, chord_string):
        # remove part markers, segnos, codas etc
        return re.sub(r'U|S|Q|N\d', '', chord_string)

    @classmethod
    def _fill_long_repeats(cls, chord_string):
        """Replaces long repeats with multiple endings with the appropriate chords
        :param chord_string: A chord string
        :return: A chord string with filled repeats
        """
        repeat_match = re.search(r'{(.+?)}', chord_string)
        if repeat_match is None:
            return chord_string
        # is there a first ending in the repeat?
        number_match = re.search(r'N(\d)', repeat_match.group(1))
        if number_match is not None:
            first_repeat = repeat_match.group(1)
            # first, get rid of the first repeat number and the curly braces
            first_repeat = re.sub(r'N\d', '', first_repeat)
            # add bar line after curly brace if required:
            if re.match(r'\}\s*\|.*', chord_string[repeat_match.end()-1:]):
                bar_line = ''
            else:
                bar_line = '|'
            new_chord_string = chord_string[:repeat_match.start()] + '|' + first_repeat + bar_line + \
                               chord_string[repeat_match.end():]

            # remove the first repeat ending as well as segnos and codas from the saved repeat
            repeat = cls._remove_markers(re.search(r'([^N]+)N\d', repeat_match.group(1)).group(1))
            # find the next repeat ending markers and insert the repeated chords before them
            while True:
                if re.search(r'[|}]\s*N(\d)', new_chord_string) is None:
                    break
                new_chord_string = re.sub(r'\|\s*N(\d)', '|' + repeat, new_chord_string)
            return new_chord_string
        else:
            # it's only a simple repeat: easy!
            new_chord_string = chord_string[:repeat_match.start()] + '|' + repeat_match.group(1) + \
                               ' |' + cls._remove_markers(repeat_match.group(1)) + chord_string[
                                                                                   repeat_match.end():] + '|'
            # there could be another repeat somewhere, so:
            new_chord_string = cls._fill_long_repeats(new_chord_string)
            return new_chord_string

    @classmethod
    def _fill_codas(cls, chord_string):
        """Flatten D.C. al Coda and D.S. al Coda
        :param chord_string: A chord string
        :return: A chord string with filled D.C. or D.S.
        """

        qs = chord_string.count('Q')
        if qs > 2:
            raise RuntimeError('Could not parse codas: number of Qs expected to be 0, 1 or 2, not {}!'.format(qs))

        # coda is used to indicate an outro: just get rid of it!
        if qs == 1:
            chord_string = chord_string.replace('Q', '')

        # this implies a repeat from the head or a segno to the first 'Q' and then a jump to the second 'Q'
        if qs == 2:
            q1, q2 = [pos for pos, char in enumerate(chord_string) if char == 'Q']
            segno = chord_string.find('S')
            if segno == -1:
                segno = 0
            coda = chord_string[q2 + 1:]
            repeat = chord_string[segno + 1:q1]
            new_chord_string = chord_string[:q2] + repeat + ' |' + coda
            new_chord_string = re.sub(r'[QS]', '', new_chord_string)
            return new_chord_string
        return chord_string

    @classmethod
    def _fill_single_double_repeats(cls, measures):
        """Replaces one- and two-measure repeat symbols with the appropriate chords
        :param measures: A list of measures (as strings)
        :return: A list of measures with filled repeats
        """
        # single repeats:
        for i in range(1, len(measures)):
            if measures[i] == 'x':
                measures[i] = cls._remove_markers(measures[i - 1])
        # double repeats:
        i = 2
        while i < len(measures):
            if measures[i] == 'r':
                first = cls._remove_markers(measures[i-2])
                second = cls._remove_markers(measures[i-1])
                measures = measures[:i] + [first, second] + measures[i+1:]
                i += 1
            i += 1
        return measures

    @classmethod
    def _fill_slashes(cls, measures):
        """Replace slash symbols (encoded as 'p') with the previous chord
        :param measures: List of measures (as strings)
        :return: A list of measures with filled slashes
        """
        for i in range(1, len(measures)):
            while measures[i].find('p') != -1:
                slash = measures[i].find('p')
                if slash == 0:
                    prev_chord = cls.chord_regex.findall(measures[i - 1])[-1]
                    measures[i] = prev_chord + measures[i][1:]
                    measures[i] = re.sub(r'^(p+)', prev_chord, measures[i])
                else:
                    prev_chord = cls.chord_regex.findall(measures[i][:slash])[-1]
                    measures[i] = measures[i][:slash] + prev_chord + measures[i][slash + 1:]
        return measures

    @classmethod
    def _add_space_between_chords(cls, measures):
        """
        Add a space between chords in the same measure
        :param measures: List of measures as strings
        :return: List of measures with added spaces
        """
        for i in range(len(measures)):
            chords = cls.chord_regex.findall(measures[i])
            measures[i] = ' '.join(chords)
        return measures

    @classmethod
    def _replace_no_chords(cls, measures):
        """
        Replace n and nn with N.C.
        :param measures: List of measures as strings
        :return: List of measures
        """
        for i in range(len(measures)):
            measures[i] = measures[i].replace('nn', 'N.C.').replace('n', 'N.C.')
        return measures

    @classmethod
    def _get_measures(cls, chord_string):
        """Splits a chord string into a list of measures, where empty measures are discarded.
        Cleans up the chord string, removes annotations, and handles repeats & codas as well.
        :param chord_string: A chord string
        :return: A list of measures, with the contents of every measure as a string
        """
        chord_string = cls._cleanup_chord_string(chord_string)
        chord_string = cls._remove_annotations(chord_string)
        chord_string = cls._fill_long_repeats(chord_string)
        chord_string = cls._fill_codas(chord_string)
        measures = re.split(r'\||LZ|K|Z|{|}|\[|\]', chord_string)
        measures = [measure.replace(' ', '') for measure in measures if measure.strip() != '']
        measures = cls._fill_single_double_repeats(measures)
        measures = cls._fill_slashes(measures)
        measures = cls._add_space_between_chords(measures)
        measures = cls._replace_no_chords(measures)

        return measures

    @classmethod
    def _get_time_signature(cls, chord_string):
        """Get the time signature form a chord string
        :param chord_string: A chord string containing a time signature
        :return: Time signature as a tuple, e.g. (3, 4)
        """
        match = re.search(r'T(\d)(\d)', chord_string)
        if match is not None:
            a = int(match.group(1))
            b = int(match.group(2))
            return a, b
        else:
            return 4, 4

    def __init__(self, tune_string):
        """Make a new Tune object from a scrambled string extracted from a url, corresponding to a
        single tune. Note: This function will *not* accept a full iReal url, e.g. a string starting with *ireal://* -
        use ``parse_ireal_url`` for this.
        :param tune_string: Scrambled string for a single tune
        """
        parts = re.split(r"=+", tune_string)
        self.title = parts[0]
        self.composer = parts[1]
        self.style = parts[2]
        self.key = parts[3]
        offset = 0
        self.transpose = None
        if parts[4].index(self._chords_prefix) != 0:
            offset = 1
            self.transpose = int(parts[4])
        chords_scrambled = parts[4 + offset].split(self._chords_prefix)[1]
        self.comp_style = len(parts) > 5 + offset and parts[5 + offset] or None
        self.bpm = len(parts) > 6 + offset and parts[6 + offset] or None
        self.repeats = len(parts) > 7 + offset and parts[7 + offset] or None

        self.raw_chord_string = self._unscramble_chord_string(chords_scrambled)
        self.chord_string = self._cleanup_chord_string(self.raw_chord_string)
        self.time_signature = self._get_time_signature(self.chord_string)
        self.measures_as_strings = self._get_measures(self.chord_string)

    def __repr__(self):
        """A nice representation containing the meta-data and the chords
        :return: String representation
        """
        result = super().__repr__() + '\n'
        result += 'Title: ' + self.title + '\n'
        result += 'Composer: ' + self.composer + '\n'
        result += 'Style: ' + self.style + '\n'
        result += 'Key: ' + self.key + '\n'
        result += 'Transpose: ' + str(self.transpose) + '\n'
        result += 'Comp style: ' + str(self.comp_style) + '\n'
        result += 'BPM: ' + str(self.bpm) + '\n'
        result += 'Repeats: ' + str(self.repeats) + '\n'
        result += 'Time signature: {}/{}'.format(*self.time_signature) + '\n\n'
        result += 'Chord string:\n' + self.chord_string + '\n\n'
        result += 'Flattened measures:\n'
        args = [iter(self.measures_as_strings)] * 4
        for chords in ([e for e in t if e is not None] for t in itertools.zip_longest(*args)):
            for chord in chords:
                result += '| {:12}'.format(chord)
            result += '|\n'
        return result

    @staticmethod
    def parse_ireal_url(url):
        """Parses iReal urls into human- and machine-readable formats

        :param url: A url containing one or more tunes
        :return: A list of Tune objects

        Example:

        ``list_of_tunes = Tune.parse_ireal_url('irealb://Example%20Song=Composer...)```
        """
        url = urllib.parse.unquote(url)
        match = re.match(r'irealb://([^"]+)', url)
        if match is None:
            raise RuntimeError('Provided string is not a valid iReal url!')
        # split url into individual songs along ===
        songs = re.split("===", match.group(1))
        tunes = []
        for song in songs:
            if song != '':
                try:
                    tune = Tune(song)
                    tunes.append(tune)
                    print('Parsed {}'.format(tune.title))
                except Exception as err:
                    print('Could not import song', song)
                    print(str(err))
        return tunes
