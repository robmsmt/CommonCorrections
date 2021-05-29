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
Turn numbers into words
```python
>>> cc = CommonCorrections()
>>> print(cc.correct_str("123"))
one two three
```
Turn decimals into words
```python
>>> cc = CommonCorrections()
>>> print(cc.correct_str("23:59"))
twenty three fifty nine
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