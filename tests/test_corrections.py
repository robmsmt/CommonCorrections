import unittest

import pandas as pd

from commoncorrections.commoncorrections import CommonCorrections


class TestString(unittest.TestCase):

    # 0.
    def test_string_empty(self):
        cc = CommonCorrections()
        x = cc.correct_str("")
        self.assertEqual(x, "")

    def test_dont_ruin_string(self):
        cc = CommonCorrections()
        x = cc.correct_str("the cat sat on the mat")
        self.assertEqual(x, x)

    # 0.
    def test_common(self):
        cc = CommonCorrections()
        x = cc.correct_str("there's")
        self.assertEqual(x, "there is")
        x = cc.correct_str("we're")
        self.assertEqual(x, "we are")
        x = cc.correct_str("it's")
        self.assertEqual(x, "it is")
        x = cc.correct_str("google.com")
        self.assertEqual(x, "google dot com")

        # todo capitalizations of first letter
        # x = cc.correct_str("It's")
        # self.assertEqual(x, "It is")

    def test_time(self):
        cc = CommonCorrections()

        x = cc.correct_str("1:15")
        print(x)
        self.assertEqual(x, "one fifteen")

        x = cc.correct_str("23:59")
        print(x)
        self.assertEqual(x, "twenty three fifty nine")

        x = cc.correct_str("8:29 pm")
        print(x)
        self.assertEqual(x, "eight twenty nine pm")

        # todo this does not work atm - need to handle this case
        # x = cc.correct_str("8:29am")
        # print(x)
        # self.assertEqual(x, "eight twenty nine am")

    def test_number(self):
        cc = CommonCorrections()
        x = cc.correct_str("123")
        print(x)
        self.assertEqual(x, "one hundred and twenty three")

        x = cc.correct_str("50102")
        print(x)
        self.assertEqual(x, "fifty thousand one hundred and two")

    def test_timer(self):
        cc = CommonCorrections()
        x = cc.correct_str("set timer for 10 mins")
        print(x)
        self.assertEqual(x, "set timer for ten mins")

    def test_decimal(self):
        cc = CommonCorrections()
        x = cc.correct_str("12.5")
        self.assertEqual(x, "twelve point five")
        x = cc.correct_str("53.4")
        self.assertEqual(x, "fifty three point four")

    def test_additonal_corrections(self):
        # this should strip out any commas

        d = {
            ',': '',
            '!': '',
            'TESTFIND': 'TESTREPLACE'
        }

        cc = CommonCorrections(additional_corrections_dict=d)
        self.assertEqual(cc.correct_str("hello, friend"), "hello friend")
        self.assertEqual(cc.correct_str("hello, friend!"), "hello friend")
        self.assertEqual(cc.correct_str("hello TESTFIND"), "hello TESTREPLACE")
        self.assertEqual(cc.correct_str("hello TESTREPLACE"), "hello TESTREPLACE")
        self.assertEqual(cc.correct_str("hello, TESTFIND!"), "hello TESTREPLACE")


class TestDataframe(unittest.TestCase):

    def test_df(self):
        df = pd.DataFrame(data={"transcript": ['5 4 3', "123 the time is 1:23"],
                                "asr_1": ["five four three", "one two three the time is one twenty three"],
                                "filename": ["./my_local_file.wav", "file2.wav"]})
        cc = CommonCorrections()

        col_list = ['transcript', 'asr_1']
        new_df = cc.correct_df(df, column_list=['transcript', 'asr_1'])

        # some columns should be identical
        self.assertEqual(df.transcript.tolist(), new_df.transcript.tolist())
        self.assertEqual(df.asr_1.tolist(), new_df.asr_1.tolist())
        self.assertEqual(df.filename.tolist(), new_df.filename.tolist())

        # new_df should have len(col_list) extra columns
        self.assertEqual(len(df.columns) + len(col_list), len(new_df.columns))

        # transcript
        for i in range(len(df)):
            self.assertEqual(new_df.transcript_corrected[i], cc.correct_str(df.transcript[i]))

        # asr_1
        for i in range(len(df)):
            self.assertEqual(new_df.asr_1_corrected[i], cc.correct_str(df.asr_1[i]))

    def test_nonstr(self):
        df = pd.DataFrame(data={"transcript": ['5 4 3', "123 the time is 1:23"],
                                "asr_1": [123, 123.23],
                                "filename": ["./my_local_file.wav", "file2.wav"]})
        cc = CommonCorrections()

        col_list = ['transcript', 'asr_1']
        new_df = cc.correct_df(df, column_list=['transcript', 'asr_1'])

        # some columns should be identical
        self.assertEqual(df.transcript.tolist(), new_df.transcript.tolist())
        self.assertEqual(df.asr_1.tolist(), new_df.asr_1.tolist())
        self.assertEqual(df.filename.tolist(), new_df.filename.tolist())

        # new_df should have len(col_list) extra columns
        self.assertEqual(len(df.columns) + len(col_list), len(new_df.columns))

        # transcript
        for i in range(len(df)):
            self.assertEqual(new_df.transcript_corrected[i], cc.correct_str(df.transcript[i]))

        # asr_1
        for i in range(len(df)):
            self.assertEqual(new_df.asr_1_corrected[i], cc.correct_str(df.asr_1[i]))

# class CustomURL(unittest.TestCase):
#
#
#     def test_url(self):
#         cc = CommonCorrections(private_corrections_url="https://<insert>")
#         x = cc.correct_str("12.5")
#         self.assertEqual(x, "twelve point five")

# running the tests - use: PYTHONPATH=$(pwd) python3 -m unittest discover .
