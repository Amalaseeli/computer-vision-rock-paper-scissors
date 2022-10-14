'''Let's play a Rock, Paper, Scissors Game
'''
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
        end_time=time.time()+0.5
        while end_time>time.time(): 
            ret, frame = cap.read()
            font = cv2.FONT_HERSHEY_SIMPLEX
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            data[0] = normalized_image
            prediction = model.predict(data)
            
            user_guess=np.argmax(prediction)
            #Puttext() method for inserting text on video
            cv2.putText(frame,f"User Choice {self.choices[user_guess]} ",(50, 50),font,1,(0, 255, 255),2,cv2.LINE_4)
            cv2.imshow('frame', frame)
            # Press q to close the window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        return self.choices[user_guess].lower() 
              
        cap.release()
    # Destroy all the windows
        cv2.destroyAllWindows()
         
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

    def get_prediction(self):
         
        computer_choice=self.get_computer_choice()
        user_choice=self.get_user_choice()
        
        print("Computer_choice:",computer_choice)
        print("User_choice:",user_choice)
        if (computer_choice=="rock" and user_choice=="scissors") or (computer_choice=="paper" and user_choice=="rock") or (computer_choice=="scissors" and user_choice=="paper"):
            self.computer_wins+=1
        elif (computer_choice=="rock" and user_choice=="paper") or (computer_choice=="paper" and user_choice=="scissors") or (computer_choice=="scissors" and user_choice=="rock"):
            self.user_wins+=1
        else:
            print("Tie")
        self.get_winner()

        
    def get_winner(self):
        if self.user_wins<=3 and self.computer_wins<=3:
            start_time=time.time()
            print(f"Computer_wins {self.computer_wins} times")
            print(f"User_wins {self.user_wins} times")
            self.get_prediction()
        elif self.user_wins>3:
            print("Oops! the computer lost the game. You win the game")
        else:
            print("Oops! the user lost the game. The computer win the game")

play=Rps()
play.get_winner()


