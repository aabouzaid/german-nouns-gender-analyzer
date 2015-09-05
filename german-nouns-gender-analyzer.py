#! /bin/python
# -*- coding: utf-8 -*-
#

import sys
import string
from collections import Counter

#---------------------------------------------------#
#Intro.
#---------------------------------------------------#
#Non-Technical details:
"""
This a simple script counts the frequency of last character in every German noun based on the noun gender,
to find the percentage of this frequency, so you can guess if you don't know what's noun gender :D

The German language has 3 genders for nouns: Masculine, Feminine, Neutral.
Unlike English which has one article ("The"), German has many articles change based on the grammatical case.
Nominativ, Akkusativ, Dativ, Genitiv! ... It's a long story :D

You can read more about German nouns at:
https://en.wikipedia.org/wiki/German_nouns
 
Anyway, in German, this is not the best way to determine the noun gender, there are another rules make it easy to guess,
but I just had a curiosity to know :D
"""

#Technical details:
'''
I tested this script with two data sets "dict.cc", and "Wiktionary".

#Dict.cc version (About 334,000 words):
I downloaded data set from dict.cc, but due to its license I can't share the data itself,
you can find more information about this data set on following URL:
  http://www1.dict.cc/translation_file_request.php

I extracted single nouns only from dictionary using Regex and "grep" command (this one-liner):
  grep -P ".*?noun" dict.cc_full_dictionary.txt | \
  grep -P -o "[A-ZÄÜÖß][a-zA-ZÄÜÖäüöß-]+[a-zäüöß] \{(m|f|n)\}" | \
  sort | uniq > dict.cc_nouns_with_gender.txt

Sample:
Apfel {m}

#Wiktionary.org version (About 50,000 words):
I donwloaded this data set from the following URL:
http://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-meta-current.xml.bz2

Then extracted single nouns only using next combination (this one-liner)::
  xbuffer=$(awk "END {print NR}" dewiktionary-latest-pages-meta-current.xml); \
  pcregrep --buffer-size ${xbuffer} -M '.*?\<text xml\:space\=\"preserve\"\>\=\= .*? \(\{\{Sprache\|Deutsch\}\}\) \=\=.*?\n.*?\=\=\= \{\{Wortart\|Substantiv\|Deutsch\}\}\, \{\{.\}\} \=\=\=.*?' dewiktionary-latest-pages-meta-current.xml | \
  awk '{noun=$3; getline; gender=gensub(/.*?\{(\{.\})\}.*?/,"\\1",$3); print noun, gender}' | \
  sort | uniq > wiktionary_nouns_with_gender.txt

Sample:
Apfel {m}
'''

#---------------------------------------------------#
#Variables.
#---------------------------------------------------#
words_file = open(sys.argv[1]).read().strip().decode("UTF8")
total_words = words_file.count("\n")
gender_counts = {
  "masculine": words_file.count("{m}"),
  "feminine": words_file.count("{f}"),
  "neutral": words_file.count("{n}")
}

#---------------------------------------------------#
#Initialize.
#---------------------------------------------------#
alphabet_repetition = {}
alphabet = list(string.ascii_lowercase.decode('UTF8')) + [u"ä",u"ü",u"ö",u"ß"]
for letter in alphabet:
  alphabet_repetition[letter] = [0,0,0]

#---------------------------------------------------#
#Functions.
#---------------------------------------------------#
#Increments character by 1.
def count_last_character(noun, gender):
  #Determine word gender.
  if gender == "m":
    noun_number = 0
  elif gender == "f":
    noun_number = 1
  elif gender == "n":
    noun_number = 2

  #Get last character of word.
  last_character = noun.split()[0][-1].lower()

  #Check if last character already in our dictionary, and increments it by 1. 
  #To avoid hassles if the data set has non German words. 
  if last_character in alphabet_repetition:
    alphabet_repetition[last_character][noun_number] += 1

#Print result for every character form the dictionary that has character counts for masculine, feminine, and neutral.
#From A to Z and other German characters like Ä, Ü, Ö and ß.
def statistics_result():
  for letter in sorted(alphabet_repetition):
    character = alphabet_repetition[letter]
    print "%s:\t%d (%.1f%%)\t%d (%.1f%%)\t%d (%.1f%%)" % (letter.upper(), character[0], percentage(character[0],sum(alphabet_repetition[letter])), character[1], percentage(character[1], sum(alphabet_repetition[letter])), character[2], percentage(character[2], sum(alphabet_repetition[letter])))

#Calculate percentage.
def percentage(count, total):
  if total == 0:
    return 0
  else:
    return count / float(total) * 100

#Print result for every gender (Masculine, Feminine, and Neutral).
def gender_statistics(gender_name):
  total_gender = gender_counts[gender_name.lower()]
  print " - %s: %d (%.2f%%)" % (gender_name.capitalize(), total_gender, percentage(total_gender, total_words))

#---------------------------------------------------#
#Count words.
#---------------------------------------------------#
#Count words based on last character by adding it to "alphabet_repetition" dictionary.
for noun in words_file.split("\n"):
  gender = noun[-2]
  count_last_character(noun, gender)

#---------------------------------------------------#
#Final result.
#---------------------------------------------------#
#Print final result: Total number of words, total number of every gender,
#and frequency of character for every gender.
print "Total number of words: (%d) words." % (total_words)
for gender in sorted(gender_counts.keys()):
  gender_statistics(gender)

print "\nCharacters statistics:\n#: \tMasculine \tFeminine \tNeutral"
print '-' * 54
statistics_result()
