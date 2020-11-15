
# Ensure that you have both beautifulsoup and requests installed:
#   pip install beautifulsoup4
#   pip install requests

import requests
from bs4 import BeautifulSoup
from random import randint
import nltk
from nltk.tokenize import WhitespaceTokenizer 
import collections
import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg

# Scrape this webpage:
result = requests.get("https://thoughtcatalog.com/michael-koh/2013/07/40-freaking-creepy-ass-two-sentence-stories/")

# Check if URL is valid
# print(result.status_code)
# print(result.headers)

src = result.content
soup = BeautifulSoup(src, 'lxml')

# Inspect each post and load them into a list
stories = soup.find_all("blockquote")
stories_clean = []

# Count how many stories there are
print("There are ",str(len(stories))," stories")

# Clean the stories for HTML markup
for story in stories:
    if story.find('image') == True:
        print('This was an image.')
    else:
        new_story = story
        story_stripped = str(new_story).strip('<blockquote><p>').strip('</p><blockquote>').replace('\xa0',' ').replace('<em>',' ').replace('</em>',' ').replace('</p>\n<p>',' ').replace('href="https://wwwredditcom/r/AskReddit/comments/2i8hj7/what_is_the_creepiest_2_sentence_poem_you_guys/','').replace('target="_blank">—<span','').replace('class="author">','').replace('[deleted]','').replace('</span>','').replace('</a','').replace('<a href="https://www.reddit.com/r/AskReddit/comments/2i8hj7/what_is_the_creepiest_2_sentence_poem_you_guys/','').replace('" target="_blank">','').replace('<span','')
        stories_clean.append(story_stripped)

selection = stories_clean[randint(0,len(stories_clean)-1)]

# Remove punctuation because whitespace tokens would absorb the punctuation when replacing words  
unpunctuate = selection.replace('.','').replace(',','').replace('!','').replace('…','').replace('”','').replace('‘','').replace('“','')#.lower()

# Run the below to do a word count by individual word analysis
wordcount = {}
for word in unpunctuate.lower().split():
    word = word.replace(".","")
    word = word.replace(",","")
    word = word.replace(":","")
    word = word.replace("\"","")
    word = word.replace("!","")
    word = word.replace("â€œ","")
    word = word.replace("â€˜","")
    word = word.replace("*","")
    # if word not in stopwords:
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1

# Print most common word
# n_print = 3
# word_counter = collections.Counter(wordcount)
# for word, count in word_counter.most_common(n_print):
#     print(word, ": ", count)

# lst = word_counter.most_common(n_print)
# df = pd.DataFrame(lst, columns = ['Word', 'Count'])
# df.plot.bar(x='Word',y='Count')

# Breaks the sentence down by whitespaces, to avoid contractions being split
tk = WhitespaceTokenizer() 
tokens = tk.tokenize(unpunctuate)
# print(tokens)
tagged = nltk.pos_tag(tokens)
# print(tagged)

def connection(pairs, item):
    return [p[1-p.index(item)] for p in pairs if item in p]

# print(connection(tagged, 'NN'))
nouns = connection(tagged, 'NN')
noun_count = len(connection(tagged, 'NN')) - 1
print('\n')

line_1 = str('Number of nouns to enter: '+str(noun_count))
count_down = noun_count
print(line_1)

sg.theme('TanBlue')
layout = [  [sg.Text(line_1)],
            [sg.Text('Please enter a noun:'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

window = sg.Window('CreepyPasta MadLibs', layout)

n = 0
user_nouns = []

# Event Loop to process "events" and get the "values" of the inputs
while n < count_down:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    print('You entered ', values[0])
    user_nouns.append(values[0])
    n += 1

window.close()
# print(user_nouns)
# print(nouns)
# plt.show()

output = selection
if noun_count < 1:
    print('Re-run for new story.')
else:
    print('Time to make a story!')
    i = 0 
    for i in range(0,noun_count):
        # Terminal input:
        # print(nouns[i])
        # new_noun = input("Please enter a noun: ")

        # GUI input:
        new_noun = user_nouns[i]
        output = output.replace(nouns[i],new_noun)

print('\n')

you_lib = str('MadPasta: '+output)
print(you_lib)
mad_lib = str('OriginalPasta: '+selection)
print(mad_lib)

layout_2 = [  [sg.Text(you_lib)],
            [sg.Text(mad_lib)] ,
            [sg.Button('So Spoopy!')] ]

window_2 = sg.Window('CreepyPasta MadLibs', layout_2)
while True:
    event, values = window_2.read()
    if event == sg.WIN_CLOSED or event == 'So Spoopy!':	# if user closes window or clicks cancel
        break
window_2.close()