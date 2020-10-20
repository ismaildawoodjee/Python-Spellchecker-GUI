# Spell-It-Right

Most Python spellcheckers require you to input your text on the command line interface
and run it to return misspelled words or suggest corrections to them. However,
we built a Python spellchecker that came with an integrated user-friendly GUI, where users 
can input their text, detect misspelled words and choose from a list of five candidate
correction words to correct them. Users can even add words to a pre-built dictionary.

An example of how this spellchecker works is shown in this [video](https://youtu.be/Xad0fN4jXpI) and the screenshot below:

![](images/gui_final_appearance.png)

## The Tasks
The team consists of four members, including myself. I was responsible for

- Data collection
- Data extraction
- Important contributions to data cleaning and preprocessing
- Implementing backend spellchecking code and suggesting correction words
- Meshing backend code with GUI frontend written by teammate
- Adding text highlighting and right-click functionality, 
  as well as dictionary scroll-box and user instructions

## Data Collection
The first challenge was to find an appropriate corpus. According to the instructor, the corpus must

1. Contain at least 100,000 words
2. Be from one scientific field only
3. Have no spelling errors

Open-source corpora on the Internet are made from a combination of papers in several scientific 
and non-scientifc disciplines, popular English eBooks and the Project Gutenberg repository. 
Or the word count ranges from several million to billion words, including misspelled ones.
A thoroughly-cleaned ready-to-use corpus that is limited to only one scientific discipline, with no spelling errors and a
word count higher than 100,000 words (but not so high, the user doesn't want to wait 15 seconds
to correct a single word) does not exist on the World Wide Web.

So I created my own corpus. A first-year [university economics textbook](https://sangu.ge/images/Economics1.pdf) in PDF format satisfies all the criteria. 
It contains 700 pages (excluding index and contents) and assuming 500 words per page, it should consist of
approximately 350,000 words (give or take 20,000). Being a textbook, I trusted it not to contain any spelling errors. 
Also, economics is a (social) science. 

## Data Extraction
The next challenge was to figure out how to extract text data from a PDF file.

PDFs are extremely messy objects. In addition to the main body of words, there are headers, footers, page numbers, chapter names and numbers, textboxes on the sides, images and diagrams, figure descriptions, and so on. 

## Data Preprocessing


## Final Appearance of the GUI

