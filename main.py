#Python based cable-like video streamer and randomizer

from __future__ import print_function, unicode_literals
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import requests
import random
from pprint import pprint
from PyInquirer import prompt, Separator
import time
import webbrowser
import pyautogui
import sys
import bs4 as bs


#TODO:
#add in weighted random feature to have a higher chance of picking better ranked episodes
#automatically play next episode
#fix channels to include more and dubbed content


#FEATURES:
#-pick a random "channel" and play random episode of a show from that category (e.g. picks 'cartoon' channel and plays spongebob episode 123 from x streaming website)
#-Option to play specific episode of that show
#-Option to play different show and episode in that category 
#-On randomized episodes cross check with highest ranking episodes on alternate website
#-Flip through channels of categories or refresh category
#-Input 'mood' questionaire to establish a score and pick a category based off that (e.g. score of 6 based on the questionaire = happy and childish mood so will play cartoons or comedy channel)

#Channels
Cartoons = ['Tom and Jerry', 'Iron Man', 'Young Justice', 'Tom and Jerry Movie: The Fast and The Furry (2005)', 'Batman Beyond', 'Danny Phantom', 'Teen Titans', 'Avatar The Last Airbender', 'Ben 10', 'Ben 10 (2005)', 'Ben 10: Alien Force', 'Ben 10: Ultimate Alien']
Comedy = ['One Punch Man', 'One Punch Man 2nd Season', 'Dr. Stone', 'Dr. Stone: Stone Wars', 'Black Clover', 'Spy x Family']
Movies = ['Pokemon 4Ever (Dub)', 'Pokemon Movie 23: Koko (Dub)', 'Pokemon Movie 21: Minna no Monogatari (Dub)', 'Dragon Ball Z Movie 12: Fusion Reborn (Dub)', 'Dragon Ball Super Movie: Broly (Dub)', 'Pokemon 3: The Movie - Spell of the Unown (Dub)']
Aesthetic = ['Shigatsu wa Kimi no Uso', 'akira', 'Koe no Katachi', 'Spirited Away', 'Howls Moving Castle', 'Princess Mononoke']
Action = ['Dragon Ball Kai 2014 (Dub)', 'Fire Force', 'My Hero Academia', 'Demon Slayer', 'Attack on Titan', 'Naruto', 'Pokemon XY']
Adventure = ['One Piece', 'Hunter x Hunter', 'Fullmetal Alchemist: Brotherhood', 'Naruto']

# Cartoons = ['Tom and Jerry|123']
# Comedy = ['One Punch Man|gogo']
# Movies = ['Pokemon (Dub)|gogo', 'Infinity War|123']
# Aesthetic = ['Akira (Dub)|gogo']
# Action = ['Boku no Hero Academia (Dub)|gogo']
# Adventure = ['Hunter x Hunter|gogo']
#add more here

Channels = ['Cartoons', 'Comedy', 'Movies', 'Aesthetic', 'Action', 'Adventure']
Channel_Arrays = [Cartoons, Comedy, Movies, Aesthetic, Action, Adventure]


#Variables
url = ''
c = webbrowser.get('firefox')
total_rng = []
Episode_Time = 0
req_headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Upgrade-Insecure-Requests": "1"
}

#Methods
def Randomize():
    Random_Channel = random.choice(Channel_Arrays)
    Random_Title_Index = random.choice(Random_Channel)
    # Random_Title = Random_Title_Index.partition('|')[0]
    Random_Title = Random_Title_Index
    # if (Random_Title_Index.partition('|')[2]=='gogo'):
        #Get Anime Link
    anime_name = Random_Title
    soup = BeautifulSoup(requests.get('https://gogoanime.fi//search.html?keyword=' + anime_name).text, 'html.parser')
    count = 0
    number = 1
    all_url = []
    titles = []
    for k, i in enumerate(soup.find_all('a')):
        if str(i.get('href')).startswith('/category') and k % 2 == 0:#it returns duplicate so using this to remove it
            count += 1
            #print('[' + str(count) + ']', str(i.get('href'))[10:].replace('-', ' '))
            titles.append(str(i.get('href'))[10:].replace('-', ' '))
            all_url.append('https://gogoanime.fi//' + str(i.get('href')))

    get_episodes_range(f'https://gogoanime.fi//{all_url[0][31:]}-episode-1')

    Episode_Ranges = [1]
    episode_number = 1
    
    for n in total_rng:
        t = n.partition('-')[2]
        Episode_Ranges.append(int(t))
    episode_number = random.randint(Episode_Ranges[0], Episode_Ranges[len(Episode_Ranges)-1])
    page = requests.get(f'https://gogoanime.fi//{all_url[0][31:]}-episode-{episode_number}')
    Soup_Link = BeautifulSoup(page.content, 'html.parser')
    
    results = Soup_Link.find(id="load_anime")
    div_list = results.find_all("div", class_="anime_video_body_watch_items load")
    count = 1
    for i in div_list:
        html_url = i.find("div", class_="play-video")
        #print(html_url)
        temp = str(html_url).partition('src="')[2]
        url = 'https:' + (temp.partition('">')[0])
        
    print('Now Playing: '+ Random_Title + '| Episode: ' + str(episode_number))          

    c.open_new(url)
    print(url)
    time.sleep(3)
    pyautogui.moveTo(-1920/2, 1080/2, duration=.1)
    pyautogui.leftClick()
    time.sleep(4)
    pyautogui.keyDown('F')
    time.sleep(.4)
    pyautogui.keyUp('F')
    # elif(Random_Title_Index.partition('|')[2]=='123'):
    #     print(Random_Title_Index.partition('|')[2])
    #     print(Random_Title)
    
def Tune():
    #Choose Title
    questions = [
        {
            'type': 'input',
            'name': 'Title',
            'message': 'What would you like to watch'
        }
    ]
    
    answers = prompt(questions)
    Show_Title = answers.get('Title')
    #Get Anime Link
    anime_name = Show_Title.replace(' ', '%20')
    soup = BeautifulSoup(requests.get('https://gogoanime.fi//search.html?keyword=' + anime_name).text, 'html.parser')
    count = 0
    episode_number = 1
    all_url = []
    titles = []
    for k, i in enumerate(soup.find_all('a')):
        if str(i.get('href')).startswith('/category') and k % 2 == 0:#it returns duplicate so using this to remove it
            count += 1
            #print('[' + str(count) + ']', str(i.get('href'))[10:].replace('-', ' '))
            titles.append(str(i.get('href'))[10:].replace('-', ' '))
            all_url.append('https://gogoanime.fi//' + str(i.get('href')))

    questions = [
        {
            'type': 'list',
            'name': 'Title',
            'message': 'Which One?',
            'choices': titles
        }
    ]
    answers = prompt(questions)
    index = titles.index(answers.get('Title'))

    get_episodes_range(f'https://gogoanime.fi//{all_url[index][31:]}-episode-1')

    Episode_Ranges = []

    for n in total_rng:
        t = n.partition('-')[2]
        Episode_Ranges.append(int(t))

    if(Episode_Ranges[len(Episode_Ranges)-1] != 1):
        questions = [
            {
                'type': 'input',
                'name': 'Episode_Number',
                'message': 'Which episode would you like to watch? ' + ','.join(total_rng)
            } 
        ]
        answers = prompt(questions)
        episode_number=answers.get('Episode_Number')
        
    page = requests.get(f'https://gogoanime.fi//{all_url[index][31:]}-episode-{episode_number}')
    Soup_Link = BeautifulSoup(page.content, 'html.parser')
    
    results = Soup_Link.find(id="load_anime")
    div_list = results.find_all("div", class_="anime_video_body_watch_items load")
    count = 1
    for i in div_list:
        html_url = i.find("div", class_="play-video")
        #print(html_url)
        temp = str(html_url).partition('src="')[2]
        url = 'https:' + (temp.partition('">')[0])
    c.open_new(url)
    time.sleep(5)
    pyautogui.moveTo(-1920/2, 1080/2, duration=.1)
    pyautogui.leftClick()
    time.sleep(4)
    pyautogui.keyDown('F')
    time.sleep(.4)
    pyautogui.keyUp('F')

def get_soup(url):
    r = requests.get(url, headers=req_headers)
    if r.status_code == 404:
        return None
    return BeautifulSoup(r.text, 'html.parser')

def get_episodes_range(anime_url):
    soup = get_soup(anime_url)
    if soup == None:
        return []
    rngs_obj = soup.find_all('a', ep_end=True, ep_start=True)
    
    for r in rngs_obj:
        rng = r.text
        rngs = rng.split('-')
        if rngs[0] == '0':
            rngs[0] = '1'
        total_rng.append('-'.join(rngs))
    return ''.join(total_rng)

#WELCOME
opener = [
    {
        'type': 'list',
        'name': 'Main',
        'message': 'Welcome!',
        'choices': ['Play', 'Tune']
    }
]
answers = prompt(opener)
if (answers.get('Main')==('Tune')):

    Tune()


elif (answers.get('Main')==('Play')):
    Randomize()
while True:
    controls = [
        {
            'type': 'list',
            'name': 'controller',
            'message': 'What would you like to do?',
            'choices': ['Play Next', 'Pick Next', 'Quit']
        }
    ]
    answers = prompt(controls)
    if(answers.get('controller')==('Play Next')):
        pyautogui.moveTo(-1920/2, 1080/2, duration=.1)
        time.sleep(2)
        pyautogui.leftClick()
        pyautogui.press('esc')
        pyautogui.hotkey('command', 'W')
        Randomize()
    elif(answers.get('controller')==('Pick Next')):
        pyautogui.moveTo(-1920/2, 1080/2, duration=.1)
        time.sleep(2)
        pyautogui.leftClick()
        pyautogui.press('esc')
        pyautogui.hotkey('command', 'W')
        pyautogui.hotkey('alt', 'tab')
        Tune()
    elif(answers.get('controller')==('Quit')):
        pyautogui.moveTo(-1920/2, 1080/2, duration=.1)
        time.sleep(2)
        pyautogui.leftClick()
        pyautogui.press('esc')
        pyautogui.hotkey('command', 'W')
        quit()
        
        
    
