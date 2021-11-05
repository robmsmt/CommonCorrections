import os
import re
from io import BytesIO, IOBase
from pathlib import Path
from typing import Union, Optional, List
import pprint

import inflect  # type: ignore
import pandas as pd  # type: ignore
import requests


def default_csv_path() -> str:
    """
    return the full path to the local csv file included in the package
    """
    return str(os.path.join(Path(__file__).parent, "corrections.csv"))


class DatatypeNotRecognized(Exception):
    pass


class CommonCorrections(object):

    def __init__(self, corrections_csv: str = default_csv_path(),
                 private_corrections_url: Optional[str] = None,
                 additional_corrections_dict: Optional[dict] = None,
                 error_duplicates: bool = True,
                 df_correction_suffix: str = "_corrected"):

        self.error_duplicates = error_duplicates
        self.df_correction_suffix = df_correction_suffix
        self.p = inflect.engine()
        self.time_regex = re.compile("^(?:[01]*\d|2[0123]):(?:[012345]\d)(?::[012345]\d)*(am|pm)?", re.IGNORECASE)
        self.decimal = re.compile("^\d+\.\d+")
        self.digits = re.compile('\d')

        if corrections_csv:
            self.df = pd.read_csv(corrections_csv, header=None, comment="#", skipinitialspace=True, na_filter=False)
        else:
            self.df = pd.DataFrame(data={0: [], 1: []})

        if private_corrections_url:
            resp = requests.get(private_corrections_url)
            assert resp.status_code == 200
            csv_bytes = BytesIO(resp.content)
            self.add_more_corrections(csv_bytes)

        if additional_corrections_dict:
            self.add_more_corrections(additional_corrections_dict)

        if self.error_duplicates:
            assert len(self.df) == len(self.df[0].unique())  # todo print which are duplicates

        self.corrections = dict(zip(self.df[0], self.df[1]))
        self.escaped_corrections = dict((re.escape(k), v) for k, v in self.corrections.items())
        self.pattern = re.compile("|".join(self.escaped_corrections.keys()))  # todo consider order and substring check on the corrections

    def __str__(self):
        return repr(pprint.pprint(self.corrections, indent=2))

    def __repr__(self):
        return repr(pprint.pprint(self.corrections, indent=2))

    def contains_digits(self, w: str) -> bool:
        return bool(self.digits.search(w))

    def contains_decimal(self, w: str) -> bool:
        return bool(self.decimal.search(w))

    def contains_time(self, w: str) -> bool:
        return bool(self.time_regex.search(w))

    def add_more_corrections(self, csv_bytes_or_dict: Union[str, IOBase, dict]) -> None:
        if type(csv_bytes_or_dict) is str or type(csv_bytes_or_dict) is BytesIO:
            new_df = pd.read_csv(csv_bytes_or_dict, header=None, comment="#", skipinitialspace=True, na_filter=False)
        elif type(csv_bytes_or_dict) == dict:
            f = [k for k in csv_bytes_or_dict]
            r = [csv_bytes_or_dict[k] for k in csv_bytes_or_dict]
            new_df = pd.DataFrame.from_dict({0:f, 1:r})
        else:
            raise DatatypeNotRecognized
        self.df = self.df.append(new_df, ignore_index=True)

    # digit and text
    def _fix_numbered_word(self, num_word: str) -> str:
        if all(char.isdigit() for char in num_word):
            return self.p.number_to_words(num_word).replace(",", "")
        elif self.contains_digits(num_word):
            #word is mixture of digit+character
            if self.contains_time(num_word):
                # TIME DETECTED
                return ' '.join([self.p.number_to_words(subword, group=3) if subword.isdigit() else subword for subword in num_word.split(":")])
            elif self.contains_decimal(num_word):
                # DECIMAL DETECTED
                replaced_num_word = num_word.replace(".", " point ")
                return ' '.join([self.p.number_to_words(subword, group=3) if subword.isdigit() else subword for subword in replaced_num_word.split()])
            else:
                return ' '.join([self.p.number_to_words(char, group=3) if char.isdigit() else char for char in num_word])
        else:
            # no digits so returns itself
            return num_word

    def _swap_digits_for_spelt(self, sentence: str) -> str:

        if self.contains_digits(sentence):

            fixed = " ".join([self._fix_numbered_word(word) if self.contains_digits(word) else word for word in sentence.split()])  # todo only whole digits are going in here atm
            fixed = fixed.replace("-", " ")

            return fixed
        else:
            return sentence

    def _fix_str(self, sentence: str) -> str:

        # 1. handle numbers
        numberless_sentence = self._swap_digits_for_spelt(str(sentence))

        # 2. handle corrections
        return self.pattern.sub(lambda m: self.escaped_corrections[re.escape(m.group(0))], numberless_sentence)

    def correct_df(self, df: pd.DataFrame, column_list: Optional[List[str]] = None) -> pd.DataFrame:
        new_df = df.copy()
        if not column_list:
            # since no columns have been provided it will find and replace across entire DF
            itor = new_df.columns()
        else:
            itor = column_list

        for col in itor:
            new_df[col + self.df_correction_suffix] = new_df[col].apply(lambda sent: self._fix_str(sent))

            # todo time vs pandas.series replace and compare - https://stackoverflow.com/questions/42012339/using-replace-efficiently-in-pandas
            # df[col+self.df_correction_suffix] = df[col+self.df_correction_suffix].replace(self.corrections)
        return new_df

    def correct_str(self, input_str: str) -> str:
        return self._fix_str(input_str)

