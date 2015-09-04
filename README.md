Analyzer of German nouns gender.
==================

###Non-Technical details:
This is a simple python script counts the frequency of last character in every German noun, based on the noun gender to find the percentage of this frequency, so you can guess if you don't know what's gender of the noun :D

The German language has 3 genders for nouns: Masculine, Feminine, Neutral. Unlike English which has one article "The", German has many articles change based on the grammatical case.
Nominativ, Akkusativ, Dativ, Genitiv! ... It's a long story :D

You can read more about German nouns at:<br>
https://en.wikipedia.org/wiki/German_nouns
 
Anyway, in German, this is not the best way to determine the noun gender, there are another rules make it easy to guess, but I just had a curiosity to know :D

###Technical details:
I tested this script with two data sets "**dict.cc**", and "**Wiktionary**".

<br>

#####Dict.cc version (About 334,000 words):
I downloaded data set from dict.cc, but due to its license I can't share the data itself,
you can find more information about this data set on following URL:<br>
  http://www1.dict.cc/translation_file_request.php

I extracted single nouns only from dictionary using Regex and "grep" command (this one-liner):
```
  grep -P ".*?noun" dict.cc_full_dictionary.txt | \
  grep -P -o "[A-ZÄÜÖß][a-zA-ZÄÜÖäüöß-]+[a-zäüöß] \{(m|f|n)\}" | \
  sort | uniq > dict.cc_nouns_with_gender.txt
```
**Final result example:**
> Apfel {m}

<br>

#####Wiktionary.org version (About 50,000 words):
I donwloaded this data set from the following URL:<br>
http://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-meta-current.xml.bz2

Then extracted single nouns only using next combination (this one-liner):
```
  xbuffer=$(awk "END {print NR}" dewiktionary-latest-pages-meta-current.xml); \
  pcregrep --buffer-size ${xbuffer} -M '.*?\<text xml\:space\=\"preserve\"\>\=\= .*? \(\{\{Sprache\|Deutsch\}\}\) \=\=.*?\n.*?\=\=\= \{\{Wortart\|Substantiv\|Deutsch\}\}\, \{\{.\}\} \=\=\=.*?' dewiktionary-latest-pages-meta-current.xml | \
  awk '{noun=$3; getline; gender=gensub(/.*?\{(\{.\})\}.*?/,"\\1",$3); print noun, gender}' | \
  sort | uniq > wiktionary_nouns_with_gender.txt
```
**Final result example:**
> Apfel {m}

<br>

###How to use:
  > python german-nouns-gender-analyzer.py nouns_with_gender.txt

<br>

###Output example:
This example of "**dict.cc**" data set.

```
Total number of words: (334399) words.
 - Feminine: 145711 (43.57%)
 - Neutral: 69784 (20.87%)
 - Masculine: 118905 (35.56%)

Characters statistics:
#:  Masculine        Feminine          Neutral
------------------------------------------------------
A:  581 (14.3%)      2331 (57.2%)      1162 (28.5%)
B:  1393 (83.1%)     14 (0.8%)         270 (16.1%)
C:  33 (42.3%)       15 (19.2%)        30 (38.5%)
D:  3791 (44.6%)     535 (6.3%)        4183 (49.2%)
E:  3249 (4.7%)      63684 (91.9%)     2354 (3.4%)
F:  3947 (89.9%)     27 (0.6%)         417 (9.5%)
G:  7164 (18.4%)     29996 (77.2%)     1690 (4.4%)
H:  5963 (68.8%)     304 (3.5%)        2398 (27.7%)
I:  1556 (46.1%)     1321 (39.1%)      499 (14.8%)
J:  2 (66.7%)        0 (0.0%)          1 (33.3%)
K:  3161 (38.2%)     3304 (39.9%)      1815 (21.9%)
L:  9733 (47.9%)     3733 (18.4%)      6854 (33.7%)
M:  3245 (29.2%)     618 (5.6%)        7257 (65.3%)
N:  10320 (25.9%)    13290 (33.3%)     16310 (40.9%)
O:  915 (37.0%)      184 (7.4%)        1376 (55.6%)
P:  684 (49.2%)      46 (3.3%)         660 (47.5%)
Q:  2 (40.0%)        0 (0.0%)          3 (60.0%)
R:  32620 (73.9%)    5672 (12.9%)      5821 (13.2%)
S:  8146 (59.2%)     2375 (17.3%)      3244 (23.6%)
T:  16521 (38.6%)    15601 (36.5%)     10630 (24.9%)
U:  909 (53.5%)      317 (18.7%)       473 (27.8%)
V:  137 (37.5%)      3 (0.8%)          225 (61.6%)
W:  50 (32.5%)       46 (29.9%)        58 (37.7%)
X:  611 (64.2%)      278 (29.2%)       63 (6.6%)
Y:  221 (35.6%)      173 (27.9%)       226 (36.5%)
Z:  3299 (50.5%)     1791 (27.4%)      1441 (22.1%)
ß:  650 (68.9%)      23 (2.4%)         270 (28.6%)
Ä:  0 (0.0%)         2 (40.0%)         3 (60.0%)
Ö:  1 (3.6%)         26 (92.9%)        1 (3.6%)
Ü:  1 (1.9%)         2 (3.8%)          50 (94.3%)
```

<br>

Now you can guess! :D
