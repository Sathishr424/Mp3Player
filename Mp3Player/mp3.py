import pygame,os,random,time
from pathlib import Path
from  functools import partial
import tkinter as tk
from tkinter import *
#from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfile
from mutagen.mp3 import MP3

pygame.init()

activeScreen = "playBack"


h_display = 520
v_display = 400
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((h_display, v_display))
white = (255, 255, 255)
black = (0,0,0)
gray = (128, 128, 128)
green = (0, 255, 128)
red = (255, 64, 64)
pygame.display.set_caption("mp3")
pygame.mixer.init()

currentPlaylist = "none"
songDurations = []

pList = False

def directoryFinder(text):
    l = len(text)-1
    for k in range(l, -1, -1):
        ##print(text[k])
        if text[k] == r"\"" or text[k - 1:k + 1] == r"\\" or  text[k] == r"//" or text[k] == r"/":
            return text[:k+1]

def songNameGeter(text):
    l = len(text) - 1
    ##print(text)
    for k in range(l, -1, -1):
        # #print(text[k])
        if text[k] == r"\"" or text[k - 1:k + 1] == r"\\" or  text[k] == r"//" or text[k] == r"/" or text[k] == "\\":
            return text[k+1:]

lastLocation = open("res\\lastLocation.ini", "r")
t = lastLocation.read()
lastLocation.close()
if (len(t) <= 1):
    root = tk.Tk()
    root.withdraw()    
    t = askdirectory()
else:
    root = tk.Tk()
    root.withdraw()
    
try:
    temp = os.listdir(t)
    directory = t + "//"
    songList = []
    for i in temp:
        if i[-4:] == ".mp3":
            songList.append(directory + i)
    if len(songList) <= 0:
        t = askdirectory()
        directory = t + "\\"
        temp = os.listdir(t)
        songList = []
        for i in temp:
            if i[-4:] == ".mp3":
                songList.append(directory + i)
    for j in songList:
        tmp = MP3(j)
        songDurations.append(tmp.info.length)
    ##print("Hello")

except:  
    t = askdirectory()
    directory = t + "\\"
    temp = os.listdir(t)
    songList = []
    for i in temp:
        if i[-4:] == ".mp3":
            songList.append(directory + i)
    for j in songList:
        tmp = MP3(j)
        songDurations.append(tmp.info.length)
            
closed = False

def displayText(text, place, s, f, bold, center=True):
    font = pygame.font.SysFont(f, s, bold) 
    text_ = font.render(text, True, white)
    rect = text_.get_rect()
    rect.center = place
    if not center:
        rect.left = place[0]
    gameDisplay.blit(text_, rect) 

class SongPlayer:
    def __init__(self):
        self.playing = False
        self.vol = 0.6
        self._next = False
        self.alterPos = 0
        self.songIndex = 0
        print(songList[self.songIndex])
        pygame.mixer.music.load(songList[self.songIndex])
        pygame.mixer.music.set_volume(self.vol)
        self.songPos = pygame.mixer.music.get_pos()
        self.songLength = 0
        self.paused = False
        self.needTOadd = 0
        self.startTime = time.time()
        ##print(self.startTime)
        self.endTime = 0
        self.seconds = 0
        self.totalSecond = 0
        self.minute = 0
        self.repeat = "none"
        self.shuffle = False
        self.fullDuration = ""

    def play(self):
        if not self.playing:
            pygame.mixer.music.play()
            music = MP3(songList[self.songIndex])
            self.songLength = music.info.length
            seek.start = 0
            seek.end = int(self.songLength)
            seek.dotPos = [seek.x+30, seek.y]
            self.playing = True
            self.paused = False
            self.seconds = 0
    
    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True
    
    def nextSong(self):
        if (self.songIndex < len(songList)-1 and not self.shuffle):
            self.songIndex+=1
            pygame.mixer.music.load(songList[self.songIndex])
            self.playing = False
            self.play()
        elif (self.songIndex >= len(songList)-1 and not self.shuffle):
            self.songIndex=0
            pygame.mixer.music.load(songList[self.songIndex])
            self.playing = False
            self.play()
        elif (self.shuffle):
            self.songIndex = random.randrange(len(songList))
            pygame.mixer.music.load(songList[self.songIndex])
            self.playing = False
            self.play()            
        self.alterPos = 0
        self.needTOadd = 0
        self.startTime = time.time()
        self.seconds = 0           
        self.totalSecond = 0
        self.minute = 0       
        self.songPos = 0             
        self.paused = False
        time.sleep(0.3)
    
    def previousSong(self):
        if (self.songIndex > 0):
            self.songIndex-=1
            pygame.mixer.music.load(songList[self.songIndex])
            self.playing = False
            self.play()
        else:
            self.songIndex=len(songList)-1
            pygame.mixer.music.load(songList[self.songIndex])
            self.playing = False
            self.play()
        self.alterPos = 0
        self.needTOadd = 0
        self.startTime = time.time()
        self.seconds = 0           
        self.totalSecond = 0
        self.minute = 0         
        self.songPos = 0           
        self.paused = False
        time.sleep(0.3)   
    
    def songLengthAdder(self, duration, p):
        p = p
        #if (self.totalSecond >= 59 or self.totalSecond <= -59):
            #self.minute+=1
        #self.totalSecond = int(p-(self.minute*60))
        ##print(str(self.minute) + ", " + str(self.totalSecond))
        self.minute = int(self.songPos/60)
        self.totalSecond = self.songPos - (self.minute*60)

        duration = duration
        ##print(duration)
        m = int(duration/60)
        s = duration - (m*60)

        s1 = abs(int(self.totalSecond))
        s2 = abs(int(s))
        m1 = abs(int(self.minute))
        m2 = abs(int(m))

        if (s1 < 10): 
            s1 = str(0) + str(s1)
        if (s2 < 10): 
            s2 = str(0) + str(s2)
        if (m1 < 10): 
            m1 = str(0) + str(m1)
        if (m2 < 10): 
            m2 = str(0) + str(m2)	
            
        self.fullDuration = str(m2) + ":" + str(s2)

        return str(m1) + ":" + str(s1)    
        
    def volUp(self):
        if self.vol <= 0.9:
            self.vol += 0.1
        pygame.mixer.music.set_volume(self.vol)
        
    def volDown(self):
        if self.vol >= 0.2:
            self.vol -= 0.1
        pygame.mixer.music.set_volume(self.vol)    
    
    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        self.endTime = time.time()
        ##print(self.endTime - self.startTime)        
        if (not self.paused):
            if (self.endTime - self.startTime >= 1):
                self.seconds += 1
                self.startTime = time.time()
        else:
            self.startTime = time.time()
                
        self.songPos = self.alterPos+self.seconds
        if ((self.songPos >= self.songLength or self._next) and not self.paused):   
            ##print("Complete")
            if (self.songIndex < len(songList)-1 and not self.shuffle and (self.repeat == "all" or self.repeat == "none")):
                self.songIndex+=1
                pygame.mixer.music.load(songList[self.songIndex])
                self.playing = False
                self.play()
            elif (self.songIndex >= len(songList)-1 and not self.shuffle and self.repeat == "all"):
                self.songIndex=0
                pygame.mixer.music.load(songList[self.songIndex])
                self.playing = False
                self.play() 
            elif (self.repeat == "one"):
                pygame.mixer.music.load(songList[self.songIndex])
                self.playing = False
                self.play()            
            elif (self.shuffle):
                ##print("suffleMode")
                self.songIndex = random.randrange(len(songList))
                pygame.mixer.music.load(songList[self.songIndex])
                self.playing = False
                self.play()
            elif (self.songIndex >= len(songList)-1 and self.repeat == "none"):
                self.songIndex=0
                pygame.mixer.music.load(songList[self.songIndex])
                self.playing = False
                self.play() 
                self.pause()
            #elif (self.)
            self.alterPos = 0
            self.needTOadd = 0
            self.startTime = time.time()
            self.seconds = 0           
            self.totalSecond = 0
            self.minute = 0       
            self.songPos = 0
            self._next = False
            ##print(songList[self.songIndex])
        if (click[0] == 1):
            if (mouse[0] >= seek.linePos[0] and mouse[0] <= seek.linePos[2] and mouse[1] >= seek.linePos[1]-(seek.thickness/2) and mouse[1] <= seek.linePos[1]+(seek.thickness/2) and mouse[0] <= seek.maxX and mouse[0] >= seek.linePos[0]):
                seek.dotPos[0] = mouse[0]
                ##print(int((seek.dotPos[0]-seek.linePos[0])/((seek.linePos[2]-seek.linePos[0])/(seek.end-seek.start)))+seek.start)
                self.needTOadd += pygame.mixer.music.get_pos()
                self.alterPos = ((((seek.dotPos[0]-seek.linePos[0])/((seek.linePos[2]-seek.linePos[0])/(seek.end-seek.start)))+seek.start))
                self.seconds = 0
                self.songPos = self.alterPos+self.seconds
                pygame.mixer.music.rewind()
                pygame.mixer.music.set_pos(self.alterPos)
                #self.miunte = int(self.songPos/60)
                time.sleep(0.2)
        seek.dotPos[0] = int(seek.linePos[0] + ((((seek.linePos[2]-seek.linePos[0])/(seek.end-seek.start))*(self.songPos))))
        n = songNameGeter(songList[self.songIndex])[:-4]
        if len(n) > 40:
            n = n[:40] + "...."
        global  activeScreen
        if activeScreen == "playBack":
            displayText(n, (250,270), 18, "Times", False)
        # #print(self.songPos)

     
class ImageButtonS:
    def __init__(self, pos, image1, image2):
        self.pos = pos
        self.image1 = pygame.image.load(image1)
        self.image2 = pygame.image.load(image2)
        self.rect = self.image1.get_rect()
        self.rect.center = self.pos
        self.currentImage = self.image1
        
    def draw(self):
        gameDisplay.blit(self.currentImage, self.rect)
        
    def update(self, add=False, n=0):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if add:
            if (mouse[0] >= self.rect.left and mouse[0] <= self.rect.right+n and mouse[1] >= self.rect.top and mouse[1] <= self.rect.bottom):
                self.currentImage = self.image2
            else:
                self.currentImage = self.image1

            if (click[0] == 1 and mouse[0] >= self.rect.left and mouse[0] <= self.rect.right+n and mouse[1] >= self.rect.top and mouse[1] <= self.rect.bottom):
                return True
        else:
            if (mouse[0] >= self.rect.left and mouse[0] <= self.rect.right and mouse[1] >= self.rect.top and mouse[1] <= self.rect.bottom):
                self.currentImage = self.image2
            else:
                self.currentImage = self.image1

            if (click[0] == 1 and mouse[0] >= self.rect.left and mouse[0] <= self.rect.right and mouse[1] >= self.rect.top and mouse[1] <= self.rect.bottom):
                return True
        

class ButtonS:
    def __init__(self, x, y, w, h, text, color):
        self.rect = [x,y,w,h]
        self.text = text
        self.color = color
    
    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, self.rect)
        displayText(self.text, (self.rect[0]+(self.rect[2]/2), self.rect[1]+(self.rect[3]/2)), 20, "Arial", False)
        
    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if (mouse[0] >= self.rect[0] and mouse[0] <= self.rect[0]+self.rect[2] and mouse[1] >= self.rect[1] and mouse[1] <= self.rect[1]+self.rect[3]):
            self.color = (192,192,192)
        else:
            self.color = (167,167,167)
        if (click[0] == 1 and mouse[0] >= self.rect[0] and mouse[0] <= self.rect[0]+self.rect[2] and mouse[1] >= self.rect[1] and mouse[1] <= self.rect[1]+self.rect[3]):
            time.sleep(0.5)
            return True

class ListBox:
    def __init__(self, pos, w, h):
        self.pos = pos
        self.height = h
        self.image = pygame.Surface((w+40,h))
        self.image.fill((128,128,128))
        self.rect = self.image.get_rect()
        self.rect.top = pos[1]
        self.rect.left = pos[0]-40
        self.startPos = 0
        self.width = w+40
        self.image2 = pygame.Surface((70,h))
        self.image2.fill((128, 128, 128))
        self.rect2 = self.image2.get_rect()
        self.rect2.left = self.rect.right + 5
        self.rect2.right = self.rect.right + 75
        self.rect2.top = self.rect.top
        self.rect2.bottom = self.rect.bottom

    def lenChecker(self, dur):
        duration = dur
        # #print(duration)
        m = int(duration / 60)
        s = duration - (m * 60)

        s2 = abs(int(s))
        m2 = abs(int(m))

        if (s2 < 10):
            s2 = str(0) + str(s2)
        if (m2 < 10):
            m2 = str(0) + str(m2)

        return  str(m2) + ":" + str(s2)

    def draw(self):
        global songDurations
        global songList
        self.rect.top = self.pos[1]
        self.rect2.top = self.rect.top
        count = 0
        for i in range(self.startPos, len(songList)):
            #miniPlay.rect.bottom = self.rect.top + 30
            #miniPlay.rect.right = miniPlay.rect.left + 30
            miniPlay.currentImage = pygame.transform.scale(miniPlay.currentImage, (30, 30))
            miniPlay.rect = miniPlay.currentImage.get_rect()
            miniPlay.rect.left = self.pos[0] - 30
            miniPlay.rect.top = self.rect.top
            if (count <= 11):
                if (songList[i] == songList[player.songIndex]):
                    if not player.paused:
                        self.image.fill((0,128,255))
                        self.image2.fill((0,128,255))
                        miniPlay.image1 = pygame.image.load("res\\play.png")
                        miniPlay.image2 = pygame.image.load("res\\play1.png")
                    else:
                        self.image.fill((0, 128, 255))
                        self.image2.fill((0, 128, 255))
                        miniPlay.image1 = pygame.image.load("res\\pause.png")
                        miniPlay.image2 = pygame.image.load("res\\pause1.png")
                else:
                    self.image.fill((128, 128, 128))
                    self.image2.fill((128, 128, 128))
                    mouse = pygame.mouse.get_pos()
                    click = pygame.mouse.get_pressed()

                    if mouse[0] >= self.rect.left and mouse[0] <= self.rect.right and mouse[
                        1] >= self.rect.top and mouse[1] <= self.rect.bottom:
                        self.image.fill((0, 84, 168))
                        self.image2.fill((0, 84, 168))
                    miniPlay.image1 = pygame.image.load("res\\pause.png")
                    miniPlay.image2 = pygame.image.load("res\\pause1.png")
                if miniPlay.update(add=True, n=self.width):
                    player.songIndex = i
                    pygame.mixer.music.load(songList[player.songIndex])
                    player.playing = False
                    player.play()
                    player.alterPos = 0
                    player.needTOadd = 0
                    player.startTime = time.time()
                    player.seconds = 0
                    player.totalSecond = 0
                    player.minute = 0
                    player.songPos = 0
                    player.paused = False
                    playB.image1 = pygame.image.load("res\\play.png")
                    playB.image2 = pygame.image.load("res\\play1.png")
                miniPlay.currentImage = pygame.transform.scale(miniPlay.currentImage, (30, 30))

                gameDisplay.blit(self.image, self.rect)
                gameDisplay.blit(self.image2, self.rect2)
                miniPlay.draw()
                n = songNameGeter(songList[i])[:-4]
                if len(n) > 40:
                    n = n[:40] + "...."
                displayText(n, (self.rect.left+45, self.rect.top+(self.height/2)), 12, "Times", False, False)
                if songList[i] == songList[player.songIndex]:
                    displayText(self.lenChecker(player.songPos), (
                    self.rect2.left + ((self.rect2.right - self.rect2.left) / 2), self.rect.top + (self.height / 2)),
                                12, "Times", False, True)
                else:
                    displayText(self.lenChecker(songDurations[i]), (self.rect2.left+((self.rect2.right - self.rect2.left)/2), self.rect.top+(self.height/2)), 12, "Times", False, True)
                self.rect.top += self.height+2
                self.rect2.top = self.rect.top
            else:
                break
            count+=1


class SeekBar:
    def __init__(self, x, y, w, lineColor, circleColor, start, end, thickness, radius, size):
        self.x = x
        self.y = y
        self.dotPos = [x+(size*2),y]
        self.linePos = [x+(size*2), y, x+w-(size*2), y]
        self.cC = circleColor
        self.lC = lineColor
        self.maxX = x+w-(size*2)
        self.start = start
        self.end = end
        self.startTextPos = (x,y)
        self.endTexPos = (x+w, y) 
        self.value = 0
        self.radius = radius
        self.thickness = thickness
        self.size = size
        
    def draw(self):
        displayText(str(player.songLengthAdder(player.songLength, player.songPos)), self.startTextPos, self.size, "Arial", False)
        displayText(str(player.fullDuration), self.endTexPos, self.size, "Arial", False)
        pygame.draw.line(gameDisplay, self.lC, [self.linePos[0], self.linePos[1]], [self.linePos[2], self.linePos[3]], self.thickness)
        pygame.draw.circle(gameDisplay, self.cC, self.dotPos, self.radius)
    
    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if (click[0] == 1 or click[1] == 1):
            if (mouse[0] >= self.linePos[0] and mouse[0] <= self.linePos[2] and mouse[1] >= self.linePos[1]-(self.thickness/2) and mouse[1] <= self.linePos[1]+(self.thickness/2) and mouse[0] <= self.maxX and mouse[0] >= self.linePos[0]):
                self.dotPos[0] = mouse[0]
                ##print("clicked")
        self.value = int((self.dotPos[0]-self.linePos[0])/((self.linePos[2]-self.linePos[0])/(self.end-self.start)))+self.start

class ScrollBar:
    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos
        self.clicked = False
        self.distanceBetweenStartToEnd = ((self.endPos[1]) - (self.startPos[1]))/(len(songList)-12)
        ##print(self.distanceBetweenStartToEnd)
        self.sizeY = ((self.endPos[1]) - (self.startPos[1])) / ((len(songList) / 12))
        self.rectImage = pygame.Surface((15, self.sizeY))
        self.rectImage.fill((237, 28, 36))
        self.rectRect = self.rectImage.get_rect()
        self.rectRect.center = [self.startPos[0], self.startPos[1] + 20]
        self.rectRect.top = self.startPos[1] - 0.25
        self.distanceBetweenStartToEnd = (((self.endPos[1]) - (self.startPos[1])) / (len(songList) - 10))
        self.rectRect.top = (self.startPos[1] - 0.2) + (
                    listB.startPos * (self.distanceBetweenStartToEnd - (self.sizeY / ((len(songList) - 10)))))
        self.perSongIncreaseCount = (self.distanceBetweenStartToEnd - (self.sizeY / ((len(songList) - 10))))
        self.oldSongList = songList
        self.clickedPos = 0
        self.oldStartPos = 0

    def draw(self):
        pygame.draw.line(gameDisplay, (228, 228, 228), [self.startPos[0], self.startPos[1]-2], self.endPos, 4)
        pygame.draw.rect(gameDisplay, (255,127,39), [self.startPos[0]-9.5, self.startPos[1]-7, 20,6])
        pygame.draw.rect(gameDisplay, (255,127,39), [self.endPos[0]-9.5, self.endPos[1]-1, 20,6])
        gameDisplay.blit(self.rectImage, self.rectRect)

    def update(self):
        if (self.oldSongList != songList):
            self.oldSongList = songList
            self.sizeY = ((self.endPos[1]) - (self.startPos[1]))/((len(songList)/12))
            self.rectImage = pygame.Surface((15, self.sizeY))
            self.rectImage.fill((237,28,36))
            self.rectRect = self.rectImage.get_rect()
            self.rectRect.center = [self.startPos[0], self.startPos[1] + 20]
            self.rectRect.top = self.startPos[1]-0.25
            self.distanceBetweenStartToEnd = (((self.endPos[1]) - (self.startPos[1])) / (len(songList)-10))
            self.rectRect.top = (self.startPos[1]-0.2) + (listB.startPos * (self.distanceBetweenStartToEnd-(self.sizeY/((len(songList)-10)))))
            self.perSongIncreaseCount = (self.distanceBetweenStartToEnd-(self.sizeY/((len(songList)-10))))
        ##print(self.perSongIncreaseCount)
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if (checkCollisionRectangle((self.startPos[0]-7.5, self.rectRect.top), 15, self.sizeY) and clicked[0] == 1) or (clicked[0] == 1 and self.clicked):
            ##print("Ok")
            if not self.clicked:
                self.clickedPos = mouse[1] - self.rectRect.top
            self.clicked = True
            tmp = int((((self.startPos[1] - 0.2)) + (mouse[1]-self.clickedPos))/self.perSongIncreaseCount)
            #print(tmp)
            if tmp >= 0 and tmp < len(songList)-9:
                listB.startPos = int((((self.startPos[1] - 0.2)) + (mouse[1]-self.clickedPos))/self.perSongIncreaseCount)
            self.rectRect.top = (((self.startPos[1] - 0.2))) + (
                    listB.startPos * (self.distanceBetweenStartToEnd - (self.sizeY / (len(songList) - 10))))
        else:
            self.clicked = False
            if self.oldStartPos != listB.startPos and not self.clicked:
                self.oldStartPos = listB.startPos
                self.rectRect.top = ((self.startPos[1] - 0.2))  + (
                        listB.startPos * (self.distanceBetweenStartToEnd - (self.sizeY / (len(songList) - 10))))


def checkCollisionRectangle(pos, w, h):
    mouse = pygame.mouse.get_pos()
    if (mouse[0] >= pos[0] and mouse[0] < pos[0]+w and mouse[1] >= pos[1] and mouse[1] <= pos[1]+h):
        return True

class HandleButtonSEvents:
    def __init__(self):
        #playB.image1.fill((0,0,0,255))
        pass
    
    def draw(self):
        global  activeScreen
        if activeScreen == "playBack":
            playB.draw()
            nextB.draw()
            previousB.draw()
            shuffle.draw()
            repeat.draw()
            seek.draw()
            enLargeB.draw()
        if activeScreen == "songList":
            listB.draw()
            backB.draw()
            if (len(songList) > 12):
                scrollB.draw()

    def update(self):
        global activeScreen
        seek.update()
        player.update()
        if activeScreen == "songList":
            if (len(songList) > 12):
                scrollB.update()
            if backB.update():
                activeScreen = "playBack"
                enLargeB.image1 = pygame.image.load("res\\enLarge.png")
                enLargeB.image2 = pygame.image.load("res\\enLarge1.png")
                enLargeB.rect.center = (500, 230)
        if activeScreen == "playBack":
            if enLargeB.update():
                if activeScreen == "playBack":
                    activeScreen = "songList"
        if (playB.update()):
            if (not player.paused):
                player.pause()
                playB.image1 = pygame.image.load("res\\pause.png")
                playB.image2 = pygame.image.load("res\\pause1.png")
            else:
                player.paused = False
                pygame.mixer.music.unpause()
                playB.image1 = pygame.image.load("res\\play.png")
                playB.image2 = pygame.image.load("res\\play1.png")
            time.sleep(0.3)
        if (nextB.update()):
            player.nextSong()           
        if (previousB.update()):
            player.previousSong()
        if (shuffle.update()):
            if (not player.shuffle):
                player.shuffle = True
                shuffle.image1 = pygame.image.load("res\\shuffleON.png")
                shuffle.image2 = pygame.image.load("res\\shuffleON1.png")
            else:
                player.shuffle = False
                shuffle.image1 = pygame.image.load("res\\shuffle.png")
                shuffle.image2 = pygame.image.load("res\\shuffle1.png")   
            time.sleep(0.2)
        if (repeat.update()):
            if (player.repeat == "none"):
                player.repeat = "all"
                repeat.image1 = pygame.image.load("res\\repeatAllOn.png")
                repeat.image2 = pygame.image.load("res\\repeatAllOn1.png") 
            elif (player.repeat == "all"):
                player.repeat = "one"
                repeat.image1 = pygame.image.load("res\\repeatOneOn.png")
                repeat.image2 = pygame.image.load("res\\repeatOneOn1.png") 
            else:
                player.repeat = "none"
                repeat.image1 = pygame.image.load("res\\repeat.png")
                repeat.image2 = pygame.image.load("res\\repeat1.png")
            time.sleep(0.3)


seek = SeekBar(40,300,400, (205,205,205), (255,83,83), 0, 100, 5, 9 , 15)
ButtonS = ButtonS(200,200,70,40,"ButtonS1",(205,205,205))
playB = ImageButtonS((250,350), "res\\play.png", "res\\play1.png")
nextB = ImageButtonS((310,350), "res\\next.png", "res\\next1.png")
previousB = ImageButtonS((190,350), "res\\previous.png", "res\\previous1.png")
repeat = ImageButtonS((370,350), "res\\repeat.png", "res\\repeat1.png")
shuffle = ImageButtonS((130,350), "res\\shuffle.png", "res\\shuffle1.png")
miniPlay = ImageButtonS((0,0), "res\\play.png", "res\\play1.png")
backB = ImageButtonS((30,30), "res\\back.png", "res\\back1.png")
enLargeB = ImageButtonS((500,230), "res\\enlarge.png", "res\\enlarge1.png")

listB = ListBox((100,10), 300, 30)
scrollB = ScrollBar([500,10], [500,390])

player = SongPlayer()
player.playing = False
player.play()

lastLocation = open("res\\lastLocation.ini", "w")
lastLocation.write(str(Path(directory)))
lastLocation.close()

handle = HandleButtonSEvents()
plus = 0
startChange = time.time()
endChange = 0
scrollEvent = False

while not closed:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4:
                if activeScreen == "songList":
                    plus = -1
                    scrollEvent = True
                if activeScreen == "playBack":
                    player.volUp()
            elif e.button == 5:
                if activeScreen == "songList":
                    plus = 1
                    scrollEvent = True
                if activeScreen == "playBack":
                    player.volDown()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DOWN:
                if activeScreen == "songList":
                    plus = 1
                if activeScreen == "playBack":
                    player.volDown()
            if e.key == pygame.K_UP:
                if activeScreen == "songList":
                    plus = -1
                if activeScreen == "playBack":
                    player.volUp()
            if e.key == pygame.K_KP_PLUS or e.key == pygame.K_EQUALS:
                player.volUp()
            if e.key == pygame.K_KP_MINUS or e.key == pygame.K_MINUS:
                player.volDown()
            if e.key == pygame.K_p:
                activeScreen = "songList"
                enLargeB.image1 = pygame.image.load("res\\enLargeOp.png")
                enLargeB.image2 = pygame.image.load("res\\enLargeOp1.png")
                enLargeB.rect.center = (30, 230)
            if e.key == pygame.K_BACKSPACE:
                activeScreen = "playBack"
                enLargeB.image1 = pygame.image.load("res\\enLarge.png")
                enLargeB.image2 = pygame.image.load("res\\enLarge1.png")
                enLargeB.rect.center = (540, 230)
            if e.key == pygame.K_o:
                root = tk.Tk()
                root.withdraw()
                player.pause()
                playB.image1 = pygame.image.load("res\\pause.png")
                playB.image2 = pygame.image.load("res\\pause1.png")
                dir_ = askdirectory()
                player.paused = False
                pygame.mixer.music.unpause()
                playB.image1 = pygame.image.load("res\\play.png")
                playB.image2 = pygame.image.load("res\\play1.png")
                if (len(dir_) > 1):
                    temp = os.listdir(dir_)
                    songList = []
                    directory = dir_ + "//"
                    for i in temp:
                        if i[-4:] == ".mp3":
                            songList.append(directory + i)
                            ##print(directory + i)
                    for j in songList:
                        tmp = MP3(j)
                        songDurations.append(tmp.info.length)
                    lastLocation = open("res\\lastLocation.ini", "w")
                    lastLocation.write(str(Path(dir_)))
                    lastLocation.close()
                    listB.startPos = 0
                    player.songIndex = len(songList)-1
                    player.nextSong()
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_DOWN or e.key == pygame.K_UP:
                if activeScreen == "songList":
                    plus = 0

    gameDisplay.fill( (45, 45, 45) )
    if plus == -1 and listB.startPos + plus >= 0:
        listB.startPos += plus
        if scrollEvent:
            scrollEvent = False
            plus = 0
    if plus == 1 and listB.startPos + plus <= len(songList)-1:
        if listB.startPos+10 < len(songList):
            listB.startPos += plus
            if scrollEvent:
                scrollEvent = False
                plus = 0
    handle.draw()
    handle.update()
    pygame.display.update()
    clock.tick(100)


