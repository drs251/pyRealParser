# recommended test runner: py.test


def test__unscramble_chord_string():
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


def test__cleanup_chord_string():
    from pyRealParser.pyRealParser import Tune
    test_string = 'T34N1A-7 |x XyQ|lC7, |cl *  *[N2F7 ][D7s *A|r |r } N4 F7sus YYY|B-7 |  E7b9'
    expected_result = 'T34N1A-7 |x |lC7 |x [N2F7 ][D7s *A|r |r } N4 F7sus |B-7 |E7b9'
    assert expected_result == Tune._cleanup_chord_string(test_string)


def test__remove_annotations():
    from pyRealParser.pyRealParser import Tune
    test_string = 'T34N1A-7 |x |lC7 |x [N2F7(D7) ][fD7s *A|r |r } N4 F7sus  <blah >YYY|B-7 |  E7b9'
    expected_result = 'N1A-7 |x |C7 |x |N2F7 |D7 |r |r } N4 F7sus |B-7 |E7b9'
    assert Tune._cleanup_chord_string(Tune._remove_annotations(test_string)) == expected_result

    test_string = 'Db9(Bb-7)(Eb7)B9(Ab-7)(Db7)| E7alt| Ab-7(F#-7)(B7)F-7Bb7|'
    expected_result = 'Db9B9| E7alt| Ab-7F-7Bb7|'
    assert expected_result == Tune._remove_annotations(test_string)


def test__remove_markers():
    from pyRealParser.pyRealParser import Tune
    test_string = 'N1A-7 |x |C7 |x |N2F7 |D7 |r |r } N4 F7 |B-7 |E7b9'
    expected_result = 'A-7 |x |C7 |x |F7 |D7 |r |r }  F7 |B-7 |E7b9'
    assert Tune._remove_markers(test_string) == expected_result


def test__fill_long_repeats():
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

    test_string = '{A-7 |B-7Q |N1C7 |C7 } N2F7 |x'
    expected_result = '|A-7 |B-7Q |C7 |C7 |A-7 |B-7 |F7 |x'
    result = Tune._fill_long_repeats(test_string)
    result = Tune._remove_annotations(Tune._cleanup_chord_string(result))
    assert result == expected_result

    test_string = '|A-7 |C7 |QD7 |G7 {QC7 |E7b9}'
    expected_result = '|A-7 |C7 |QD7 |G7 |QC7 |E7b9 |C7 |E7b9|'
    result = Tune._fill_long_repeats(test_string)
    result = Tune._remove_annotations(Tune._cleanup_chord_string(result))
    assert expected_result == result


def test__fill_codas():
    from pyRealParser.pyRealParser import Tune
    test_string = 'A7 |A7S |B7 |B7Q |C7 |C7Q |D7 |D7'
    expected_result = 'A7 |A7 |B7 |B7 |C7 |C7 |B7 |B7 |D7 |D7'
    result = Tune._fill_codas(test_string)
    result = Tune._cleanup_chord_string(result)
    assert expected_result == result


def test__fill_single_double_repeats():
    from pyRealParser.pyRealParser import Tune
    test_string = 'A-7 |x |C7 |x |N1F7 |D7 |r |r |F7 |B-7 |E7b9'
    expected_result = Tune._get_measures('A-7 |A-7 |C7 |C7 |N1F7 |D7 |F7 |D7 |F7 |B-7 |E7b9')
    assert expected_result == Tune._fill_single_double_repeats(Tune._get_measures(test_string))


def test__fill_slashes():
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


def test__add_space_between_chords():
    from pyRealParser.pyRealParser import Tune
    test_measures = ['A-7', 'Bb6C7/Ab', 'C7/AbC7/AbF7', 'D7']
    expected = ['A-7', 'Bb6 C7/Ab', 'C7/Ab C7/Ab F7', 'D7']
    assert Tune._add_space_between_chords(test_measures) == expected

    test_measures = ['A-7', 'Bb6', 'F7/A#F7/A#F7/A#C', 'D7']
    expected = ['A-7', 'Bb6', 'F7/A# F7/A# F7/A# C', 'D7']
    assert Tune._add_space_between_chords(test_measures) == expected


def test__get_measures():
    from pyRealParser.pyRealParser import Tune
    test_string = 'A-7 |x |C7 |x |N1F7 |D7 |r |r ][F7 ||B-7 |E7b9'
    expected_result = ['A-7', 'A-7', 'C7', 'C7', 'N1 F7', 'D7', 'F7', 'D7', 'F7', 'B-7', 'E7b9']
    assert expected_result == Tune._get_measures(test_string)


def test__get_time_signature():
    from pyRealParser.pyRealParser import Tune
    test_string = '*A[T43Eb^7XyQKcl LZDh7XyQ|G7b9XyQ|C-7XyQKcl LZBb-7XyQ|Eb7XyQ]'
    assert (4, 3) == Tune._get_time_signature(test_string)


def test_parse_ireal_url():
    from pyRealParser.pyRealParser import Tune
    test_string = 'irealb://Test=McTest%20Testy==Up%20Tempo%20Swing=Eb==1r34LbKcu7X7bB%7C4Eb%5E7FZL5%237C%209bB' + \
                  '%7CQy1X1-F%7CQyX7-C%7CQyX-7XyQ4TA%2A%7Bb7C%7CQ7%20B7L7-G%7CQyX7oA%7CQyX%5E7bAZL5b7A%207-bBZ%' + \
                  '2FBbXy-C%7CQy%20QyXQY%7CF-77bB%207-FZL7bG%207G-1N%7CQyX%2C7bB%7CQyX%2C%20%7DXy%7CQyX9EZL6-b6' + \
                  'XyQ%7Cr%20ZL%20%7Cr%20ZL%2C7bZEL7-bBB%2A%5B%5D%20%20lcK%20LZBbE2NZL%20dr3%20b%5E7LZ%2ED<%2C7' + \
                  'FZLxZLxZL%5E7bAl%7C%2C7bE%2C7-bBsC%2E%20alAZL7bEnd%2E>LZBb7sus%2CLZBb7%20%5DXyQXyQ%20%20Y%7C' + \
                  'N3Eb6XyQ%7CBb7XyQZ%20==0=0==='
    tune = Tune.parse_ireal_url(test_string)
    measures = tune[0].measures_as_strings
    str(Tune.parse_ireal_url(test_string))


def test_parse_ireal_url_as_long():
    from pyRealParser.pyRealParser import Tune
    url = 'irealb://%41%73%20%4C%6F%6E%67%20%41%73%20%49%20%4C%69%76%65=%41%72%6C%65%6E%20%48%61%72%6F%6C%64==%4D%6' \
          '5%64%69%75%6D%20%53%77%69%6E%67=%46==%31%72%33%34%4C%62%4B%63%75%37%20%37%2D%47%7C%34%46%5E%37%58%6C%5' \
          'A%4C%37%44%20%37%2D%41%7C%51%79%58%37%5A%44%4C%2C%39%62%37%41%20%37%68%45%6C%7C%51%79%47%37%58%79%51%3' \
          '4%54%41%2A%5B%5B%5D%51%79%58%31%46%5E%37%20%62%42%20%37%5E%46%32%4E%5A%4C%20%51%79%58%79%51%58%7D%20%3' \
          '7%43%20%37%2D%47%5A%4C%37%2D%44%37%4C%5A%46%36%4E%5A%4C%37%43%37%47%7C%51%79%20%46%37%4C%5A%7C%2C%37%4' \
          '1%2C%68%45%73%20%37%5E%46%5A%4C%62%37%45%20%37%2D%62%42%7C%51%79%58%37%5E%62%42%6C%44%2D%37%58%37%2D%4' \
          '3%42%2A%44%20%37%2D%41%2D%37%58%79%51%44%5A%4C%2C%39%62%37%41%20%37%68%45%6C%7C%79%51%58%37%5E%46%41%2' \
          'A%5B%5D%51%79%58%37%43%7C%37%58%79%51%7C%47%7C%51%79%58%37%4C%5A%6C%47%37%58%79%51%7C%47%2D%37%20%43%3' \
          '7%4C%5A%46%5E%37%20%42%62%37%4C%5A%46%36%58%79%51%5A%20==%30=%30==='
    tune = Tune.parse_ireal_url(url)[0]
    raw = tune.raw_chord_string
    flat = tune.measures_as_strings
    pass


def test_parse_ireal_url_it_might():
    from pyRealParser.pyRealParser import Tune
    url = 'irealb://%49%74%20%4D%69%67%68%74%20%41%73%20%57%65%6C%6C%20%42%65%20%53%70%72%69%6E%67=%52%6F%64%67%65%72%73%20%52%69%63%68%61%72%64==%4D%65%64%69%75%6D%20%53%77%69%6E%67=%47==%31%72%33%34%4C%62%4B%63%75%37%2D%44%5A%4C%20%34%47%5E%37%58%58%37%5E%47%5A%4C%37%44%20%37%2D%41%5A%4C%45%37%20%37%2D%42%7C%51%79%58%37%2D%41%7C%51%79%79%51%4B%63%6C%34%54%5B%41%2A%7C%51%79%58%37%47%37%58%79%51%58%37%45%7C%51%79%58%37%2D%42%5A%4C%39%62%23%37%46%20%37%68%23%43%7C%51%79%58%37%5E%43%7C%79%51%7C%41%2D%7C%51%79%58%37%20%37%47%20%37%7C%4E%31%42%2D%58%37%5E%47%32%4E%5A%4C%20%51%79%58%51%79%7D%58%20%37%44%20%37%2D%41%5A%4C%37%2D%45%20%37%79%51%7C%44%2D%51%79%58%37%44%4C%37%2D%41%7C%5E%37%4C%5A%41%68%42%73%5A%4C%37%5E%43%5A%4C%37%47%5A%4C%2D%37%44%5A%4C%37%47%5A%4C%37%2D%44%5A%4C%37%2D%2C%45%37%2C%6C%43%5B%42%2A%5D%41%5A%4C%37%41%47%4C%5A%46%23%6E%65%20%64%72%33%20%6C%61%20%2E%43%2E%44%5A%3C%4C%37%2D%45%5A%4C%39%62%37%42%5A%4C%37%68%64%69%6E%67%3E%2F%37%2D%41%5A%23%46%2F%37%5E%37%20%5D%7C%4E%7C%51%79%58%37%46%7C%51%79%58%37%2D%43%5A%78%4C%5A%4C%37%41%5A%4C%37%45%5A%4C%37%2D%42%33%47%5E%37%20%47%44%5A%4C%37%2D%4C%37%5E%47%5A%20%45%2D%37%2F%37%2D%41%5A%4C%37%45%5A%4C%37%2D%42%7C%51%58%79%36%2D%43%7C%51%79%58%37%68%23%43%5A%4C%44%4C%5A%44%37%4C%37%2D%45%5A%4C%5A%78%4C%5A%41%2D%37%4C%5A%44%37%20%5A==%30=%30==='
    tune = Tune.parse_ireal_url(url)[0]
    raw = tune.raw_chord_string
    flat = tune.measures_as_strings
    pass


def test_parse_ireal_url_nightingale():
    from pyRealParser.pyRealParser import Tune
    url = 'irealb://%41%20%4E%69%67%68%74%69%6E%67%61%6C%65%20%53%61%6E%67%20%49%6E%20%42%65%72%6B%65%6C%65%79%20%53%71%75%61%72%65=%53%68%65%72%77%69%6E%20%4D%61%6E%6E%69%6E%67==%42%61%6C%6C%61%64=%45%62==%31%72%33%34%4C%62%4B%63%75%37%41%20%2D%43%6C%34%45%62%5E%37%68%44%73%20%37%5E%62%41%6C%7C%2C%37%62%45%37%2C%2D%62%42%73%20%37%2D%47%5A%4C%37%2D%43%20%2C%47%37%2C%7C%34%54%41%2A%7B%37%2D%46%5A%4C%45%62%5E%37%2F%5E%62%45%6C%7C%2C%37%62%44%2C%37%2D%62%41%20%73%47%2F%37%5E%62%45%5A%4C%37%2D%46%20%62%42%37%20%43%2D%37%5A%4C%36%2D%62%42%2A%5B%5D%20%5A%59%7C%4E%31%41%7C%51%79%58%37%5E%62%45%32%4E%7D%20%37%42%62%20%37%2D%46%5A%4C%37%2D%43%20%37%5E%62%45%68%37%20%44%37%4C%37%62%42%20%37%44%20%37%2D%2D%37%4C%5A%41%45%20%37%5E%47%5A%4C%37%44%20%37%2D%41%5A%37%4C%6F%62%42%20%37%2D%42%5A%4C%37%44%20%37%2D%2D%37%4C%5A%41%45%20%37%5E%47%41%6C%7C%2C%37%20%45%2D%37%4C%62%42%73%20%37%2D%47%5A%4C%37%2D%43%20%37%62%5E%45%41%2A%5B%5D%20%37%62%42%20%37%2D%46%5A%2D%37%2C%45%62%37%2D%42%5A%4C%62%44%2C%37%2D%44%68%2C%47%37%2F%37%5E%62%45%5A%4C%37%2D%46%20%62%42%2F%5E%37%62%45%5A%4C%36%2D%62%41%20%2D%43%6C%7C%2C%47%20%73%41%62%73%20%37%5E%62%37%2C%7C%6C%45%62%5E%37%20%43%2D%37%4C%5A%46%2D%37%20%42%62%37%4C%5A%45%62%5E%37%20%43%2D%37%4C%5A%46%2D%37%20%42%62%37%20%5A%20==%30=%30==='
    tune = Tune.parse_ireal_url(url)[0]
    raw = tune.raw_chord_string
    flat = tune.measures_as_strings
    pass


def test_parse_ireal_url_airmail():
    from pyRealParser.pyRealParser import Tune
    url = 'irealb://%41%69%72%6D%61%69%6C%20%53%70%65%63%69%61%6C=%43%68%72%69%73%74%69%61%6E%20%43%68%61%72%6C%69%65==%4D%65%64%69%75%6D%20%55%70%20%53%77%69%6E%67=%43==%31%72%33%34%4C%62%4B%63%75%37%51%79%58%5A%4C%34%3C%2A%36%35%51%79%58%5A%4C%51%79%58%7C%72%51%79%58%5A%20%4C%6C%63%4B%51%79%58%36%43%3E%64%61%65%48%20%72%7C%58%79%51%34%54%69%2A%5B%37%62%41%7C%51%20%5D%5B%43%6F%42%5A%4C%37%6F%42%20%37%6F%43%5A%4C%51%79%7C%58%72%51%79%58%5A%4C%20%6C%63%4B%51%79%58%37%62%6F%37%58%79%51%79%58%7C%72%6C%6F%53%3C%53%37%58%79%51%5D%79%58%51%79%58%51%79%58%51%79%58%51%79%58%41%3E%42%41%41%20%3A%6D%72%6F%46%20%38%31%2A%3C%51%20%7B%2A%41%47%7C%51%79%58%20%43%7C%51%79%43%2F%45%4C%5A%4C%37%6F%23%46%20%46%5A%4C%37%43%20%43%5A%47%4C%20%46%5A%4C%45%2F%43%20%43%5A%4C%47%20%46%5A%43%2F%47%58%20%43%3E%73%6F%51%79%58%37%6F%3E%20%20%7D%5B%6F%42%20%37%6F%43%5A%4C%51%79%58%7C%72%51%58%79%5A%4C%20%6C%63%4B%51%79%58%37%6F%43%42%2A%37%4C%5A%42%62%65%6E%69%46%3C%7C%41%62%37%58%79%51%7C%3C%44%2E%53%2E%20%61%6C%20%46%69%6E%65%3E%47%37%58%79%51%5A%20==%30=%30==='
    tune = Tune.parse_ireal_url(url)[0]
    raw = tune.raw_chord_string
    flat = tune.measures_as_strings
    pass


def test_parse_ireal_url_blood():
    from pyRealParser.pyRealParser import Tune
    url = 'irealb://%42%6C%6F%6F%64%20%43%6F%75%6E%74=%53%74%72%61%79%68%6F%72%6E%20%42%69%6C%6C%79==%53%6C%6F%77%20%53%77%69%6E%67=%44==%31%72%33%34%4C%62%4B%63%75%37%44%7C%51%79%58%34%46%39%23%31%62%45%20%37%2D%62%42%7C%51%79%58%33%31%62%7C%45%51%79%58%31%31%23%33%31%45%7C%51%79%58%31%39%4C%5A%44%2D%34%54%41%2A%5B%7C%51%79%58%31%62%2F%44%29%58%7C%51%79%58%31%31%23%39%46%41%2A%5B%5D%20%44%39%20%37%2D%41%7C%51%79%58%36%2D%44%7C%51%79%45%31%33%23%31%42%28%36%62%2D%2A%5B%5D%20%39%79%51%7C%42%62%7C%51%79%58%36%44%7C%51%79%58%35%23%37%5E%7C%44%51%79%58%37%5E%44%5A%4C%39%62%45%20%37%2D%41%2D%37%20%44%58%33%31%62%45%51%79%58%74%6C%58%79%51%7C%47%79%58%37%68%42%7C%51%79%58%31%31%23%39%62%7C%42%51%79%58%36%2D%47%7C%51%79%58%73%75%73%37%51%7C%45%37%61%33%31%5E%47%42%7C%51%79%58%33%42%62%31%33%4C%79%58%31%31%23%33%31%45%7C%51%79%58%31%31%39%23%46%41%2A%5B%5D%20%33%31%43%20%33%31%42%5A%51%7C%45%62%31%20%33%31%41%7C%7C%51%79%58%39%45%62%39%4C%5A%5D%20%39%44%20%37%2D%41%7C%51%79%58%36%44%51%7C%79%58%35%23%37%5E%44%7C%51%79%58%37%5E%44%5B%2A%43%47%5E%20%37%2D%62%42%62%45%20%37%2D%51%7C%46%23%2D%20%37%2D%23%46%5A%4C%39%62%37%23%43%20%37%23%68%47%6C%7C%2C%41%2F%57%2C%37%2D%42%73%20%37%46%39%4C%5A%45%79%58%36%2D%47%62%41%2C%44%2F%23%39%20%46%39%62%45%20%37%2D%45%5A%4C%39%46%20%37%2D%23%51%46%5B%5A%20%51%2C%39%62%45%20%37%2D%45%5A%4C%39%4C%5A%73%47%37%44%5A%4C%39%2F%44%2C%42%2F%44%2C%43%2F%44%2C%7C%6C%43%23%2F%44%20%66%55%42%62%2F%44%20%5A%20==%30=%30==='
    tune = Tune.parse_ireal_url(url)[0]
    raw = tune.raw_chord_string
    flat = tune.measures_as_strings
    pass
