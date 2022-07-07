# CC - CommonCorrections

A simple repo that is used to correct common ASR outputs. 
The aim is not on mistakes but different ways of transcribing the same thing with a focus on how something may sound as opposed to the shortened form. 
The primary use case is to align the ground-truth and output from ASRs just before the WER is calculated. 

### Static Examples
```text
there's -> there is
google.com -> google dot com
```

### Dynamic Examples
```text
1 2 3 -> one two three
53.4 -> fifty three point four
23:59 -> twenty three fifty nine
```

## Features
 1. Designed to be used and fast (ish) with Pandas dataframes
 2. Lots of built in corrections for free
 3. Ability to easily extend with private corrections


## Getting Started
 1. Install with: `pip install commoncorrections`
 2. Import with: `from commoncorrections import CommonCorrections`

## Usage Examples
Turn numbers into words:
```python
>>> cc = CommonCorrections()
>>> print(cc.correct_str("1 2 3"))
one two three
```
Turn times into words:
```python
>>> cc = CommonCorrections()
>>> print(cc.correct_str("23:59"))
twenty three fifty nine
```
Correct a pandas dataframe:
```python
df = pd.DataFrame(data={"transcript": ['5 4 3', "123 the time is 1:23"],
                             "asr_1": ["five four three", "one two three the time is one twenty three"],
                             "filename": ["./my_local_file.wav", "file2.wav"]})
cc = CommonCorrections()

# to correct only specific columns 
new_df = cc.correct_df(df, column_list=['transcript', 'asr_1'])
# to apply to whole dataframe
new_whole_df = cc.correct_df(df)
```

## mypy Type Checks
I tested installing mypy to check that types are compatible
```bash
(py) rob@rob-T480s:~/projects/CommonCorrections/commoncorrections (master)$ mypy commoncorrections.py
Success: no issues found in 1 source file
```

## Change Log
 - v1.0.0 - First release 
 - v1.0.1 - Fixed packaging issue 
 - v1.0.3 - Fixed pip packaging issue 
 - v1.0.4 - Fixed pip packaging issue 
 - v1.0.5 - Fixed issue single digits
 - v1.0.6 - Fixed case where dataframe contains a non-str type (e.g. int)
 - v1.0.7 - Fixed adding additional dict works and added print(cc) object
 - v1.0.8 - Fixed print bug with repl
 - v1.0.9 - Added some words with space in default corrections csv
 - v1.0.10 - Typo in some corrections
 - v1.0.11 - Added test case and fixed mistake
 - v1.0.12 - Fixed pinning requirements
