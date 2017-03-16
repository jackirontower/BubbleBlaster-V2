#!/usr/bin/python3
raw_input('Ready to play? ')
# Importing modules
from math import sqrt
import sys
from Tkinter import *
from time import sleep, time
from random import randint, choice

# Window and screen setup
HEIGHT = 800
WIDTH = 1600
window = Tk()
window.title('Bubble Blaster')
can = \
Canvas(window, width = WIDTH, height = WIDTH, bg='darkblue')

# Image setup
bg_img = PhotoImage(file = "bg_bubble.gif")
img = PhotoImage(file = "bubsub2.gif")
#play_img = PhotoImage(file = "play_btn.gif" )
small_img = PhotoImage.subsample(img, x = 1, y = 1)

# Creating the ship and background
bgpic = can.create_image((800, 400), image = bg_img)
ship_id = can.create_image((50, 50), image = small_img)
can.pack()
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
# Placing the ship in the middle of the screen
can.move(ship_id, MID_X, MID_Y)

# Ship settings
ship_spd = 20
SHIP_R = 20

# Moving the ship by defining an event function
def move_ship(event):
    if event.keysym == 'Up':
        can.move(ship_id, 0, -ship_spd)
        
    elif event.keysym == 'Down':
        can.move(ship_id, 0, ship_spd)
        
    elif event.keysym == 'Right':
        can.move(ship_id, ship_spd, 0)
        
    elif event.keysym == 'Left':
        can.move(ship_id, -ship_spd, 0)
        
    if event.keysym == 'q':
        try:
            can.create_text(MID_X, MID_Y, text="Quiting Already?", fill="#FFAC00", \
                font=("femkeklaver", 55))
            window.update()
            sleep(3)
            window.destroy()
        except tkinter.TclError:
            sys.exit(2)
    
    if event.keysym == 'p':
        while event.keysym != 'P':
            pass

can.bind_all('<Key>', move_ship)

# Setting up the bubbles and 
# minimizing/maximizing bubble
# speed and size
bub_id = []
bub_r = []
bub_speed = []
MIN_BUB_R = 10
MAX_BUB_R = 35
MAX_BUB_SPD = 15
GAP = 100
colors = ["#639DD6"]

# A function for creating bubbles
def create_bubble():
    x = WIDTH + GAP
    y = randint(175, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    id1 = can.create_oval(x - r, y - r, x + r, y + r, outline='white', fill=choice(colors))
    # Adding the bubble to the id, radius, and speed lists
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPD))

# A function for moving the bubbles horizontily across the screen
def move_bubbles():
    for i in range(len(bub_id)):
        can.move(bub_id[i], -bub_speed[i], 0)
        
# Determining the coordinates of the bubbles
def get_coords(id_num):
    pos = can.coords(id_num)
    x = (pos[0] + pos[1])/2
    y = (pos[1] - pos[0])/2
    return x, y
    
# Deleting the bubble using a function
def del_bubble(i):
    del bub_r[i]
    del bub_speed[i]
    can.delete(bub_id[i])
    del bub_id[i]

# Deleting bubbles if they go off-screen
def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x, y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)

# Finding the distance between id1 and id2
# by calling the get_coords() function
def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 -y1)**2)
    
# Detecting collisions between the sub and bubbles
def collision():
    points = 0
    for bub in range(len(bub_id)-1, -1, -1):
        # By using the distance function, we find out wether
        # or not the bubbles are touching the sub
        if distance(ship_id, bub_id[bub]) < (SHIP_R + bub_r[bub]):
            points += (bub_r[bub] + bub_speed[bub])
            del_bubble(bub)
    return points

    
# Creating the time and score text
can.create_rectangle(1350, 0, 1550, 150, fill="grey")
can.create_text(1450, 30, text='TIME', fill='#FFAC00', font=("Monospace bold", 20) )
can.create_text(1450, 100, text='SCORE', fill='#FFAC00', font=("Monospace bold", 20) )
time_text = can.create_text(1450, 60, fill='#FFAC00', font=("Monospace bold", 16) )
score_text = can.create_text(1450, 140, fill='#FFAC00', font=("Monospace bold", 16) )

# A function that displays the score and modifies it
def show_score(score):
    can.itemconfig(score_text, text=str(score))
    
# A function that displays the time and modifies it
def show_time(time_left):
    can.itemconfig(time_text, text=str(time_left))  

# Setup for the high score
target = open('high_score')
r = target.readline()
# Creating the high score text
can.create_rectangle(650, 0, 950, 150, fill="grey")
can.create_text(800, 70, text="HIGH SCORE", fill='#FFAC00', font=('Monospace bold', 23))
high_score_text = can.create_text(800, 100, text=r, fill='#FFAC00', font=("Monospace bold", 23))

# A function that displays the new high score
def show_new_high():
    new_high = score
    can.itemconfig(high_score_text, text=str(new_high))

# Saving the high score by writing it
# to the file 'high_score'
def save():
    target = open('high_score', 'w')
    target.write(str(score))

# Setup for the main loop    
BUB_CHANCE = 6
TIME_LIMIT = 25
BONUS_SCORE = 1000
score = 0
bonus = 0
end = time() + TIME_LIMIT

#MAIN GAME LOOP
while time() < end:
    if randint (1, BUB_CHANCE) == 1:
        create_bubble()
    
    # Managing the bubbles    
    move_bubbles()
    clean_up_bubs()
    score += collision()
    
    # Detecting high scores
    if (int(score / BONUS_SCORE)) > bonus:
        bonus += 1
        end += TIME_LIMIT
        BUB_CHANCE += 1
        
    # Displaying score    
    show_score(score)
    if score > int(r):
        show_new_high()
        save()
        
    # Managing time    
    show_time(int(end - time()))
    window.update()
    sleep(0.001)

# Creating the gameover text
can.create_rectangle(490, 190, 1110, 610, fill="black")
can.create_rectangle(500, 200, 1100, 600, fill="#6D6161", outline="black")
can.create_text(MID_X, MID_Y - 20, \
              text='GAME OVER', fill='#FF0000', font=('femkeklaver', 75))
can.create_text(MID_X, MID_Y + 40, \
              text='Score: '+ str(score), fill='#FFAC00', font=("Monospace bold", 20))
can.create_text(MID_X, MID_Y + 70, \
              text='Bonus Time: '+ str(bonus*TIME_LIMIT), fill='#FFAC00', font=("Monospace bold", 20))
window.update()
sleep(4)

# THE END
