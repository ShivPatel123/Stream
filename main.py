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
import bs4 as bs
from rich import print


#TODO:
#add in weighted random feature to have a higher chance of picking better ranked episodes

#FEATURES:
#-pick a random "channel" and play random episode of a show from that category (e.g. picks 'cartoon' channel and plays spongebob episode 123 from x streaming website)
#-Option to play specific episode of that show
#-Option to play different show and episode in that category 
#-On randomized episodes cross check with highest ranking episodes on alternate website
#-Flip through channels of categories or refresh category
#-Input 'mood' questionaire to establish a score and pick a category based off that (e.g. score of 6 based on the questionaire = happy and childish mood so will play cartoons or comedy channel)

#Channels

Cartoons = [
    ['Tom and Jerry Movie: The Great Chases|110', 'Tom and Jerry Movie: The Fast and The Furry (2005)|110'], 
    ['Iron Man: Armored Adventures|022'], 
    ['Young Justice Season 01 (Dub)|023', 'Young Justice Season 02 (Dub)|023', 'Young Justice Season 03 (Dub)|023', 'Young Justice Season 04 (Dub)|023'],
    ['Danny Phantom|022'],
    ['Teen Titans|022', 'Teen Titans: Trouble in Tokyo (Dub)|115'],
    ['Avatar: The Last Airbender: Book 1 - Water|022', 'Avatar: The Last Airbender: Book 2 - Earth|022', 'Avatar: The Last Airbender: Book 3 - Fire|022', 'The Legend of Korra Season 1|021'],
    ['Ben 10 (2005) Season 01 (Dub)|022', 'Ben 10 (2005) Season 02 (Dub)|022', 'Ben 10 (2005) Season 03 (Dub)|022', 'Ben 10 (2005) Season 04 (Dub)|022', 'Ben 10: Alien Force Season 01 (Dub)|022', 'Ben 10: Alien Force Season 03 (Dub)|022', 'Ben 10: Alien Force Season 02 (Dub)|022', 'Ben 10: Ultimate Alien Season 01 (Dub)|022', 'Ben 10: Ultimate Alien Season 02 (Dub)|022', 'Ben 10: Ultimate Alien Season 03 (Dub)|022', 'Ben 10: Omniverse (Dub)|022', 'Ben 10: Secret of the Omnitrix (Dub)|110']    
    ]
Comedy = [
    ['One Punch Man (Dub)|022', 'One Punch Man 2nd Season (Dub)|022', 'One Punch Man Specials (Dub)|011', 'One Punch Man 2nd Season Specials (Dub)|011'],
    ['Dr. Stone (Dub)|022', 'Dr. Stone: Stone Wars (Dub)|022']
]
Movies = [
    ['Pokemon 3: The Movie - Spell of the Unown (Dub)|110', 'Pokemon: Mewtwo Returns (Dub)|100', 'Pokemon 4Ever (Dub)|118', 'Pokemon: The Movie 2000 (Dub)|140', 'Pokemon Movie 23: Koko (Dub)|138', 'Pokemon: Jirachi Wish Maker (Dub)|120', 'Pokemon: The Rise Of Darkrai (Dub)|128', 'Pokemon Heroes: Latias and Latios (Dub)|110', 'Pokemon XY: Ring no Choumajin Hoopa (Dub)|105', 'Pokemon: Senritsu no Mirage Pokemon (Dub)|042', 'Pokemon Movie 21: Minna no Monogatari (Dub)|135'],
    ['Dragon Ball Z Movie 12: Fusion Reborn (Dub)|050', 'Dragon Ball Z Movie 14: Battle of Gods (Dub)|145', 'Dragon Ball Z Movie 05: Cooler (Dub)|046', 'Dragon Ball Z Movie 07: Super Android 13 (Dub)|045', 'Dragon Ball Z Movie 07: Super Android 13 (Dub)|045', 'Dragon Ball Z Movie 08: Broly - The Legendary Super Saiyan (Dub)|110'],
    ['Spirited Away (Dub)|202', 'Moving Castle (Dub)|158', 'Laputa: Castle in the Sky (Dub)|200', 'Mononoke Hime (Dub)|210'],
    ['Koe no Katachi (Dub)|210', 'Kimi no Na wa. (Dub)|145', 'SHIGATSU WA KIMI NO USO (DUB)|021']
]
Action = [
    ['Dragon Ball Kai (Dub)|021', 'Dragon Ball Kai 2014 (Dub)|021', 'Dragon Ball (Dub)|023'],
    ['Enen no Shouboutai (Dub)|021', 'Enen no Shouboutai: Ni no Shou (Dub)|021'],
    ['Boku no Hero Academia (Dub)|021', 'Boku no Hero Academia 2nd Season (Dub)|021', 'Boku no Hero Academia 3rd Season (Dub)|021', 'Boku no Hero Academia 4th Season (Dub)|021', 'Boku no Hero Academia 5th Season (Dub)|021'],
    ['Kimetsu no Yaiba (Dub)|021', 'Kimetsu no Yaiba: Yuukaku-hen (Dub)|021'],
    ['Naruto (Dub)|021']
]
Adventure = [
    ['Hunter x Hunter 2011 (Dub)|022'],
    ['Fullmetal Alchemist: Brotherhood (Dub)|021'],
    ['Naruto (Dub)|021']
]
#add more here

Channels = ['Cartoons', 'Comedy', 'Movies', 'Action', 'Adventure']
Channel_Arrays = [Cartoons, Comedy, Movies, Action, Adventure]
Queue = []
Queue_Names = Queue
for channel in Channel_Arrays:
    Random_Title_Index = random.choice(channel)
    Random_Title_Name = random.choice(Random_Title_Index)
    Queue.append(Random_Title_Name)
random.shuffle(Queue)

Queue_Names = Queue
count = 0
timer = 0


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
x,y = pyautogui.size()
x,y=int(str(x))/2,int(str(y))/2

#Methods
def randomizeQueue():
    n = 0
    for channel in Channel_Arrays:
        Random_Title_Index = random.choice(channel)
        Random_Title_Name = random.choice(Random_Title_Index)
        Queue[n] = Random_Title_Name
        n += 1
    random.shuffle(Queue)

def Play(anime_name):
    soup = BeautifulSoup(requests.get('https://gogoanime.fi//search.html?keyword=' + anime_name).text, 'html.parser')
    all_url = []
    titles = []
    for k, i in enumerate(soup.find_all('a')):
        if str(i.get('href')).startswith('/category') and k % 2 == 0:
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
    for i in div_list:
        html_url = i.find("div", class_="play-video")
        temp = str(html_url).partition('src="')[2]
        url = 'https:' + (temp.partition('">')[0])
        
    print('Now Playing: '+ anime_name + ' | Episode: ' + str(episode_number))          

    c.open_new(url)
    #print(url)
    time.sleep(10)
    pyautogui.moveTo(x, y, duration=.1)
    pyautogui.leftClick()
    time.sleep(2)
    pyautogui.keyDown('F')
    time.sleep(.4)
    pyautogui.keyUp('F')
    
def Search():
    # #Choose Title
    # questions = [
    #     {
    #         'type': 'input',
    #         'name': 'Title',
    #         'message': 'What would you like to watch'
    #     }
    # ]
    
    # answers = prompt(questions)
    # Show_Title = answers.get('Title')
    # #Get Anime Link
    # anime_name = Show_Title.replace(' ', '%20')
    # soup = BeautifulSoup(requests.get('https://gogoanime.fi//search.html?keyword=' + anime_name).text, 'html.parser')
    # count = 0
    # episode_number = 1
    # all_url = []
    # titles = []
    # for k, i in enumerate(soup.find_all('a')):
    #     if str(i.get('href')).startswith('/category') and k % 2 == 0:#it returns duplicate so using this to remove it
    #         count += 1
    #         #print('[' + str(count) + ']', str(i.get('href'))[10:].replace('-', ' '))
    #         titles.append(str(i.get('href'))[10:].replace('-', ' '))
    #         all_url.append('https://gogoanime.fi//' + str(i.get('href')))

    # questions = [
    #     {
    #         'type': 'list',
    #         'name': 'Title',
    #         'message': 'Which One?',
    #         'choices': titles
    #     }
    # ]
    # answers = prompt(questions)
    # index = titles.index(answers.get('Title'))

    # get_episodes_range(f'https://gogoanime.fi//{all_url[index][31:]}-episode-1')

    # Episode_Ranges = []

    # for n in total_rng:
    #     t = n.partition('-')[2]
    #     Episode_Ranges.append(int(t))

    # if(Episode_Ranges[len(Episode_Ranges)-1] != 1):
    #     questions = [
    #         {
    #             'type': 'input',
    #             'name': 'Episode_Number',
    #             'message': 'Which episode would you like to watch? ' + ','.join(total_rng)
    #         } 
    #     ]
    #     answers = prompt(questions)
    #     episode_number=answers.get('Episode_Number')
        
    # page = requests.get(f'https://gogoanime.fi//{all_url[index][31:]}-episode-{episode_number}')
    # Soup_Link = BeautifulSoup(page.content, 'html.parser')
    
    # results = Soup_Link.find(id="load_anime")
    # div_list = results.find_all("div", class_="anime_video_body_watch_items load")
    # count = 1
    # for i in div_list:
    #     html_url = i.find("div", class_="play-video")
    #     #print(html_url)
    #     temp = str(html_url).partition('src="')[2]
    #     url = 'https:' + (temp.partition('">')[0])
    # c.open_new(url)
    # time.sleep(5)
    # pyautogui.moveTo(-1920/2, 1080/2, duration=.1)
    # pyautogui.leftClick()
    # time.sleep(4)
    # pyautogui.keyDown('F')
    # time.sleep(.4)
    # pyautogui.keyUp('F')
    return 0

def getTime():
    timer = int((int(Queue[count].partition('|')[2])/100)) * 3600
    timer += (int(Queue[count].partition('|')[2])%100) * 60
    return timer

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

print('-'*150)
print("The Mix:")
for id in Queue:
    if((id.partition('|')[0])[-6:] == ' (Dub)'):
        print((id.partition('|')[0])[:-6], end=" | ")
    else:
        print(id.partition('|')[0], end=" | ")
print()
print('='*150)

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
    Cartoon_Queue = []
    for channel in Channel_Arrays: Cartoon_Queue.append(random.choice(random.choice(Cartoons)))
    Comedy_Queue = []
    for channel in Channel_Arrays: Comedy_Queue.append(random.choice(random.choice(Comedy)))
    Movies_Queue = []
    for channel in Channel_Arrays: Movies_Queue.append(random.choice(random.choice(Movies)))
    Action_Queue = []
    for channel in Channel_Arrays: Action_Queue.append(random.choice(random.choice(Action)))
    Adventure_Queue = []
    for channel in Channel_Arrays: Adventure_Queue.append(random.choice(random.choice(Adventure)))
    ChannelQueues = [Cartoon_Queue, Comedy_Queue, Movies_Queue, Action_Queue, Adventure_Queue]
    ChannelsList = ['The Mix', 'Cartoons', 'Comedy', 'Movies', 'Action', 'Adventure']
    print('-'*150)
    n=0
    for channel_queue in ChannelQueues:
        print(Channels[n] + ":")
        for id in channel_queue:
            if((id.partition('|')[0])[-6:] == ' (Dub)'):
                print((id.partition('|')[0])[:-6], end=" | ")
            else:
                print(id.partition('|')[0], end=" | ")
        print()
        print('-'*150)
        n+=1
        
    questions = [
        {
            'type': 'list',
            'name': 'Title',
            'message': 'Which One?',
            'choices': ChannelsList
        }
    ]
    answers = prompt(questions)
    
    if answers.get("Title")==('Cartoons'): Queue = Cartoon_Queue
    elif answers.get("Title")==('Comedy'): Queue = Comedy_Queue
    elif answers.get("Title")==('Movies'): Queue = Movies_Queue
    elif answers.get("Title")==('Action'): Queue = Action_Queue
    elif answers.get("Title")==('Adventure'): Queue = Adventure_Queue
    
    print('-'*150)
    print("Up Next:")
    print('-'*150)
    for id in Queue:
        if((id.partition('|')[0])[-6:] == ' (Dub)'):
            print((id.partition('|')[0])[:-6], end=" | ")
        else:
            print(id.partition('|')[0], end=" | ")
    print()
    print('='*150)

elif (answers.get('Main')==('Play')):
    
    Play(Queue[count].partition('|')[0])
    time.sleep(getTime())
    pyautogui.moveTo(x, y, duration=.1)
    pyautogui.leftClick()
    pyautogui.hotkey('command', 'W')
    count += 1
    
    
while True:
    if(count < 5):
        Play(Queue[count].partition('|')[0])
        time.sleep(getTime())
        pyautogui.moveTo(x, y, duration=.1)
        pyautogui.leftClick()
        pyautogui.hotkey('command', 'W')
        count += 1
    else:
        randomizeQueue()
        count = 0
        print('-'*150)
        print("Up Next:")
        print('-'*150)
        for id in Queue:
            if((id.partition('|')[0])[-6:] == ' (Dub)'):
                print((id.partition('|')[0])[:-6], end=" | ")
            else:
                print(id.partition('|')[0], end=" | ")
        print()
        print('-'*150)
    
