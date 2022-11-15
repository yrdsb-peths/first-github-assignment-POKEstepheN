"""This program is a reaction game, where LEDs will light up at random and then
   turned off. The user will try to press the button that corresponds
   to the lit LED before the LED turns off.

   Program by: Stephen Liu"""

#import statements
from gpiozero import LED, Button
from time import sleep
import sys
import random

#variable initialisation
easyLevelButton=Button(11)      #GPIO pin 11
mediumLevelButton=Button(25)    #GPIO pin 25
hardLevelButton=Button(8)       #GPIO pin 8
hammerButton1=Button(7)         #GPIO pin 7
hole1=LED(5)                    #GPIO pin 5
hammerButton2=Button(6)         #GPIO pin 6
hole2=LED(13)                   #GPIO pin 13
hammerButton3=Button(19)        #GPIO pin 19
hole3=LED(26)                   #GPIO pin 26
hammerButton4=Button(20)        #GPIO pin 20 
hole4=LED(21)                   #GPIO pin 21
hammerButton5=Button(2)         #GPIO pin 2
hole5=LED(3)                    #GPIO pin 3
hammerButton6=Button(4)         #GPIO pin 4
hole6=LED(14)                   #GPIO pin 14
hammerButton7=Button(15)        #GPIO pin 15
hole7=LED(18)                   #GPIO pin 18
hammerButton8=Button(17)        #GPIO pin 17
hole8=LED(27)                   #GPIO pin 27
score1=LED(22)                  #GPIO pin 22
score2=LED(23)                  #GPIO pin 23 
score3=LED(24)                  #GPIO pin 24   
score4=LED(10)                  #GPIO pin 10 
controlButton=Button(9)         #GPIO pin 9
interval=3                      #How long the hole LEDs light up
inGame=False                    #If the program is in the main game sequence
count=0                         #The number of times the game loop ran
holeList=[hole1,hole2,hole3,hole4,hole5,hole6,hole7,hole8]   #List of hole LEDs
hammerList=[hammerButton1,hammerButton2,hammerButton3,
            hammerButton4,hammerButton5,hammerButton6,
            hammerButton7,hammerButton8]            #List of hammer buttons
scoreList=[score1,score2,score3,score4]             #List of score LEDs
hammerStatus=False              #The hammer buttons' operational status
successfulPress=False           #If the user hit the correct hammer button
hole=0                          #Determines at random which LED turns on

"""Runs the actual game sequence, where the user will be tested on their
   reaction"""
def run_game_sequence():

    #Make the variables usable everywhere
    global scoreList
    global hole
    global holeList
    global hammerStatus
    global hammerList
    global interval
    global successfulPress
    global inGame
    
    #Reset different parameters for the upcoming game sequence
    decScore=0   #The user's score in decimal
    binScore=""  #The user's score in binary

    #Turns off all score LEDs
    for scoreLed in scoreList:

        scoreLed.off()
    
    #There are 15 chances for the user to press the correct button in time
    for i in range(15):

        hole=random.randint(0,7)
        holeList[hole].on()
        hammerStatus=True
        hammerList[hole].when_pressed=press_successful
        sleep(interval)
        hammerStatus=False

        #The LED will flash and there is a +1 score if successfulPress is true
        if successfulPress:

            #The hold LED will flash 3 times
            for j in range(3):

                holeList[hole].off()
                sleep(0.3)
                holeList[hole].on()
                sleep(0.3)
            
            decScore+=1
            successfulPress=False

        holeList[hole].off()
        sleep(0.2)
        
    binScore=turn_dec_to_bin(decScore)  #The binary score of the user

    #Based on the binary score, the score LEDs will turn on (On is 1, Off is 0)
    for digit in range(4):

        #If the digit of the score is 1, the corresponding score LED turns on
        if binScore[digit]=="1":
            
            scoreList[digit].on()

    inGame=False

#The variable successfulPress changes to True if the button is pressed on time
def press_successful():

    #Make the variable usable everywhere
    global successfulPress
    global hammerStatus
    
    """The code runs if the hammer buttons are active and the correct
       button is pressed"""
    if hammerStatus and hammerList[hole].is_pressed:

        successfulPress=True
        hammerStatus=False

"""Turns the decimal score to binary so it could be displayed by LEDs
   decScore-The user's score in decimal"""
def turn_dec_to_bin(decScore):

    binScore=""
    exponent=3

    #This loop creates the binary number
    for i in range(4):

        #Determines using the subtraction method if a digit is 0 or 1
        if decScore-2**exponent>0:

            decScore-=2**exponent
            binScore+="1"

        elif decScore-2**exponent<0:

            binScore+="0"

        else:

            binScore+="1"

            #The rest of the digits will be 0
            for j in range(exponent):

                binScore+="0"

            break

        exponent-=1

    return binScore

#Set different intervals depending on the level chosen
def set_interval():

    #Make the variable usable everywhere
    global interval
    global inGame

    #Only if 
    if not inGame:

        #The LEDs will turn on for 3 seconds before turning off
        if easyLevelButton.is_pressed:
            
            interval=3
            
        #The LEDs will turn on for 2 seconds before turning off
        elif mediumLevelButton.is_pressed:
            
            interval=2

        #The LEDs will turn on for 1 second before turning off
        else:
            
            interval=1

        inGame=True

"""If the user pressed the control button, the main game sequence is not
   running, and the game ran at least once, the program will end"""
def end_program():

    if (not inGame) and (count>=1):

        sys.exit("The program has ended.")

"""All the LEDs are turned off and the user is asked to press the control
   button to start the game"""
hole1.off()
hole2.off()
hole3.off()
hole4.off()
hole5.off()
hole6.off()
hole7.off()
hole8.off()
score1.off()
score2.off()
score3.off()
score4.off()
print("Press the control button to start the program!")

#The program waits for the control button to be pressed then starts
controlButton.wait_for_press()

#The level the user chooses determines the interval the LEDs will light up
easyLevelButton.when_pressed=set_interval
mediumLevelButton.when_pressed=set_interval
hardLevelButton.when_pressed=set_interval

"""If the user pressed the control button after the program started, the
   program will end"""
controlButton.when_pressed=end_program

#The loop will keep on checking if the inGame is set to True
while True:

    if inGame:

        run_game_sequence()
        count+=1
