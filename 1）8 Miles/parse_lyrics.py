import os
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import cv2
import nltk

# read all the lyrics
def read_all_lyrics(file_path):
    all_lyrics = ''
    for lyric_file in os.listdir(file_path):
        with open(file_path + "/" + lyric_file) as f:
            letters = str(f.read())
            all_lyrics += letters

    return all_lyrics

# parse lyrics
def parse_lyrics(lyrics):
    words = Counter(lyrics.split(" "))# a dict { 'word':count }

    #filter
    filter_manual = ['a', 'like', 'get', 'can', 'at', 'till', 'are']
    nouns = {x.name().split('.', 1)[0] for x in nltk.corpus.wordnet.all_synsets('n')}
    for word in list(words.keys()):
        if word.lower() not in nouns or word.lower() in filter_manual:
            del words[word]

    print(words)
    return words

# draw words
def draw_words(words):
    cloud = WordCloud(
        font_path='C:\Windows\Fonts\STHUPO.TTF',#necessary if you want to draw Chinese
        width=600,
        height=480,
        background_color='snow',
        max_words=350,
        max_font_size=150)
    world_cloud = cloud.fit_words(words)
    world_cloud.to_file('Eminem.jpg')
    plt.imshow(world_cloud)



def main():
    #read Eminem's lyrics
    lyric_path = "./32665"
    all_lyrics = read_all_lyrics(lyric_path)

    #parse lyrics
    words = parse_lyrics(all_lyrics)

    #draw them!
    draw_words(words)

if __name__ == '__main__':
    main()
