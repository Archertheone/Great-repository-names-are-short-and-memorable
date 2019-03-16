import requests
import re
import os
import json
from bs4 import BeautifulSoup


# get html content
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        html = response.content
        return html
    except:
        print('request error')
        pass


# get music id by musician
def get_music_ids_by_musician_id(musician_id):
    singer_url = 'http://music.163.com/artist?id=' + str(musician_id)
    r = get_html(singer_url)
    soupObj = BeautifulSoup(r, 'lxml')
    song_ids = soupObj.find('textarea').text
    j = json.loads(song_ids)
    ids = {}
    # print(len(j))
    for item in j:
        print(item['id'])
        # ids[item['name']] = item['id']
    return ids


# get one music lyric
def get_lyric_by_id(music_id):
    lyric_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(music_id) + '&lv=1&kv=1&tv=-1'
    r = requests.get(lyric_url)
    jobj = r.text
    j = json.loads(jobj)
    try:
        lrc = j['lrc']['lyric']
        pattern_lrc = re.compile(r'\[.*\]')
        lrc = re.sub(pattern_lrc, "", lrc)
        lrc = lrc.strip()
        return lrc
    except:
        pass

# download lyrics
def download_lyrics(musician_id, music_ids):
    #start a directory
    os.mkdir(str(musician_id))
    os.chdir(str(musician_id))

    #download lyric for each music
    for id in music_ids:
        text = get_lyric_by_id(music_ids[id])
        file = open(id + '.txt', 'a')
        file.write(id + '\n')
        file.write(str(text).replace(u'\xa0', u' '))#solve decode problem
        file.close()



# get lyrics by musician id
def get_lyrics(musician_id):
    #get music ids
    music_ids = get_music_ids_by_musician_id(musician_id)

    #download music lyrics
    download_lyrics(musician_id, music_ids)


def main():
    #eminem id : 32665
    #Jay Chou id : 6452
    get_lyrics(32665)
    return

if __name__ == '__main__':
    main()
