'''Let's play a Rock, Paper, Scissors Game
'''
from tkinter import N
import cv2
import random
from keras.models import load_model
import numpy as np
import time

model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

class Rps:
    def __init__(self):
        self.user_wins=0
        self.computer_wins=0
        self.choices=["Rock","Paper","Scissors","Nothing"]

    def get_user_choice(self):
        end_time=time.time()+1

        while end_time>time.time():
            ret, frame = cap.read()
            font = cv2.FONT_HERSHEY_SIMPLEX
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            data[0] = normalized_image
            prediction = model.predict(data)
            user_guess=np.argmax(prediction[0])
            #Puttext() method for inserting text on video
            cv2.putText(frame,f"User Choice {self.choices[user_guess]} ",(50, 50),font,1,(0, 255, 255),2,cv2.LINE_4)
            cv2.imshow('frame', frame)
            user_choice = self.choices[user_guess].lower()
            # Press q to close the window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        return user_choice
         
    #Get Computer Choice
    @staticmethod
    def get_computer_choice():
        guess={}
        with open('labels.txt') as f:
            for content in f:
                key,value=content.split()
                guess[key]=value
            f.close()
        computer_choice=random.choice(list(guess.values())).lower()
        return computer_choice

    @staticmethod
    def countdown(t):
        minutes,seconds=divmod(t,60)#Get minutes and seconds
        timer="{:02d}:{:02d}".format(minutes,seconds)
        print(timer, end="\r")#Force the cursor to go back to start of screen
        time.sleep(2)
        t-=1
        print("Rock Paper Scissors shoot...")

    def get_winner(self,computer_choice,user_choice):
        print("Computer_choice:",computer_choice)
        print("User_choice:",user_choice)
        if (computer_choice=="rock" and user_choice=="scissors") or (computer_choice=="paper" and user_choice=="rock") or (computer_choice=="scissors" and user_choice=="paper"):
                self.computer_wins+=1
                
        elif (computer_choice=="rock" and user_choice=="paper") or (computer_choice=="paper" and user_choice=="scissors") or (computer_choice=="scissors" and user_choice=="rock"):
                self.user_wins+=1
        else:
            print("Tie")
        return self.computer_wins,self.user_wins

def play_game():
    play=Rps()
    
    while play.user_wins < 3 or play.computer_wins < 3: 
        play.countdown(5)
        computer_choice=play.get_computer_choice()
        user_choice=play.get_user_choice()
        play.get_winner(computer_choice,user_choice)
        print(f"Computer_wins {play.computer_wins} times")
        print(f"User_wins {play.user_wins} times")
            
        if play.user_wins==3:
            print("Oops! the computer lost the game. You win the game")
            break
        elif play.computer_wins==3:
            print("Oops! the user lost the game. The computer win the game")
            break
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()   
       
play_game()


