from unittest import TestCase


class TestTune(TestCase):
    def test__unscramble_chord_string(self):
        from pyRealParser.pyRealParser import Tune

        scrambled = '[T44A BLZC DLZE FLZG, ALZA BLZC DLZE FLZG ALZA B | '
        unscrambled = '[T44A BLZC DLZE FLZG, ALZA BLZC DLZE FLZG ALZA B | '
        assert unscrambled == Tune._unscramble_chord_string(scrambled)

        scrambled = '| B A BLZCZLF EZLD CZLB ZALA ,GZLF EZLD G ALZA44T[C '
        unscrambled = '[T44A BLZC DLZE FLZG, ALZA BLZC DLZE FLZG ALZA B |C '
        assert unscrambled == Tune._unscramble_chord_string(scrambled)

        scrambled = 'ZLB A BLZCZLF EZLD CZLB ZALA ,GZLF EZLD G ALZA44T[C- DLZE ' + \
                    'FLZG A,LZA BLZC DLZE FLZG ALZA BLZC- D |E '
        unscrambled = '[T44A BLZC DLZE FLZG, ALZA BLZC DLZE FLZG ALZA BLZC- DLZE ' + \
                      'FLZG A,LZA BLZC DLZE FLZG ALZA BLZC- D |E '
        assert unscrambled == Tune._unscramble_chord_string(scrambled)

        scrambled = 'ZLB A BLZCZLF EZLD CZLB ZALA ,GZLF EZLD G ALZA44T[ EZLDZE FLB ' + \
                    'AZLA GZLF EZDL CZLB AZL,A GZLZC- LD -CF '
        unscrambled = '[T44A BLZC DLZE FLZG, ALZA BLZC DLZE FLZG ALZA BLZC- DLZE FLZG ' + \
                      'A,LZA BLZC DLZE FLZG ALZA BLZC- DLZE F '
        assert unscrambled == Tune._unscramble_chord_string(scrambled)

    def test__cleanup_chord_string(self):
        from pyRealParser.pyRealParser import Tune
        test_string = 'T34N1A-7 |x XyQ|lC7, |cl *  *[N2F7 ][D7s *A|r |r } N4 F7sus YYY|B-7 |  E7b9'
        expected_result = 'T34N1A-7 |x |lC7 |x [N2F7 ][D7s *A|r |r } N4 F7sus |B-7 |E7b9'
        assert expected_result == Tune._cleanup_chord_string(test_string)

    def test__remove_annotations(self):
        from pyRealParser.pyRealParser import Tune
        test_string = 'T34N1A-7 |x |lC7 |x [N2F7(D7) ][fD7s *A|r |r } N4 F7sus  <blah >YYY|B-7 |  E7b9'
        expected_result = 'N1A-7 |x |C7 |x |N2F7 |D7 |r |r } N4 F7sus |B-7 |E7b9'
        assert expected_result == Tune._cleanup_chord_string(Tune._remove_annotations(test_string))

        test_string = 'Db9(Bb-7)(Eb7)B9(Ab-7)(Db7)| Ab-7(F#-7)(B7)F-7Bb7|'
        expected_result = 'Db9B9| Ab-7F-7Bb7|'
        assert expected_result == Tune._remove_annotations(test_string)

    def test__remove_markers(self):
        from pyRealParser.pyRealParser import Tune
        test_string = 'N1A-7 |x |C7 |x |N2F7 |D7 |r |r } N4 F7 |B-7 |E7b9'
        expected_result = 'A-7 |x |C7 |x |F7 |D7 |r |r }  F7 |B-7 |E7b9'
        assert Tune._remove_markers(test_string) == expected_result

    def test__fill_long_repeats(self):
        from pyRealParser.pyRealParser import Tune
        test_string = '{A-7 |B-7 |N1C7 |C7 } |N2F7 |x ][D7 |G7 |C7 |F7 ] |N3B-7 |E7b9'
        expected_result = '|A-7 |B-7 |C7 |C7 |A-7 |B-7 |F7 |x |D7 |G7 |C7 |F7 |A-7 |B-7 |B-7 |E7b9'
        result = Tune._fill_long_repeats(test_string)
        result = Tune._remove_annotations(Tune._cleanup_chord_string(result))
        assert expected_result == result

        test_string = '{A-7 |B-7Q |N1C7 |C7 } |N2F7 |x'
        expected_result = '|A-7 |B-7Q |C7 |C7 |A-7 |B-7 |F7 |x'
        result = Tune._fill_long_repeats(test_string)
        result = Tune._remove_annotations(Tune._cleanup_chord_string(result))
        assert expected_result == result

        test_string = '|A-7 |C7 |QD7 |G7 {QC7 |E7b9}'
        expected_result = '|A-7 |C7 |QD7 |G7 |QC7 |E7b9 |C7 |E7b9|'
        result = Tune._fill_long_repeats(test_string)
        result = Tune._remove_annotations(Tune._cleanup_chord_string(result))
        assert expected_result == result

    def test__fill_codas(self):
        from pyRealParser.pyRealParser import Tune
        test_string = 'A7 |A7S |B7 |B7Q |C7 |C7Q |D7 |D7'
        expected_result = 'A7 |A7 |B7 |B7 |C7 |C7 |B7 |B7 |D7 |D7'
        result = Tune._fill_codas(test_string)
        result = Tune._cleanup_chord_string(result)
        assert expected_result == result

    def test__fill_single_double_repeats(self):
        from pyRealParser.pyRealParser import Tune
        test_string = 'A-7 |x |C7 |x |N1F7 |D7 |r |r |F7 |B-7 |E7b9'
        expected_result = Tune._get_measures('A-7 |A-7 |C7 |C7 |N1F7 |D7 |F7 |D7 |F7 |B-7 |E7b9')
        assert expected_result == Tune._fill_single_double_repeats(Tune._get_measures(test_string))

    def test__fill_slashes(self):
        from pyRealParser.pyRealParser import Tune
        test_measures = ['A-7', 'C7', 'ppF7', 'D7']
        expected_result = ['A-7', 'C7', 'C7C7F7', 'D7']
        assert expected_result == Tune._fill_slashes(test_measures)

        test_measures = ['A-7', 'Bb6C7/Ab', 'ppF7', 'D7']
        expected_result = ['A-7', 'Bb6C7/Ab', 'C7/AbC7/AbF7', 'D7']
        assert expected_result == Tune._fill_slashes(test_measures)

        test_measures = ['A-7', 'Bb6', 'F7/A#ppC', 'D7']
        expected_result = ['A-7', 'Bb6', 'F7/A#F7/A#F7/A#C', 'D7']
        assert expected_result == Tune._fill_slashes(test_measures)

    def test__get_measures(self):
        from pyRealParser.pyRealParser import Tune
        test_string = 'A-7 |x |C7 |x |N1F7 |D7 |r |r ][F7 ||B-7 |E7b9'
        expected_result = ['A-7', 'A-7', 'C7', 'C7', 'N1F7', 'D7', 'F7', 'D7', 'F7', 'B-7', 'E7b9']
        assert expected_result == Tune._get_measures(test_string)

    def test__get_time_signature(self):
        from pyRealParser.pyRealParser import Tune
        test_string = '*A[T43Eb^7XyQKcl LZDh7XyQ|G7b9XyQ|C-7XyQKcl LZBb-7XyQ|Eb7XyQ]'
        assert (4, 3) == Tune._get_time_signature(test_string)

    def test_parse_ireal_url(self):
        from pyRealParser.pyRealParser import Tune
        test_string = 'irealb://Test=McTest%20Testy==Up%20Tempo%20Swing=Eb==1r34LbKcu7X7bB%7C4Eb%5E7FZL5%237C%209bB' + \
                      '%7CQy1X1-F%7CQyX7-C%7CQyX-7XyQ4TA%2A%7Bb7C%7CQ7%20B7L7-G%7CQyX7oA%7CQyX%5E7bAZL5b7A%207-bBZ%' + \
                      '2FBbXy-C%7CQy%20QyXQY%7CF-77bB%207-FZL7bG%207G-1N%7CQyX%2C7bB%7CQyX%2C%20%7DXy%7CQyX9EZL6-b6' + \
                      'XyQ%7Cr%20ZL%20%7Cr%20ZL%2C7bZEL7-bBB%2A%5B%5D%20%20lcK%20LZBbE2NZL%20dr3%20b%5E7LZ%2ED<%2C7' + \
                      'FZLxZLxZL%5E7bAl%7C%2C7bE%2C7-bBsC%2E%20alAZL7bEnd%2E>LZBb7sus%2CLZBb7%20%5DXyQXyQ%20%20Y%7C' + \
                      'N3Eb6XyQ%7CBb7XyQZ%20==0=0==='
        str(Tune.parse_ireal_url(test_string))
