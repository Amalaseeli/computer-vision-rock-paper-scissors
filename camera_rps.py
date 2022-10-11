import cv2
import random
from keras.models import load_model
import numpy as np
import time

model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def get_user_choice():

    duration=5
    start_time=time.time()
    time_passed=0

    while True: 
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        user_guess=np.argmax(prediction)
        cv2.imshow('frame', frame)
        
        list=['rock','paper','scissors','nothing']
        # Press q to close the window
        #print(prediction)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        if time.time()-start_time >=time_passed:
            time_passed+=1
            print(time.time()-start_time)
            print(time_passed)
        if time_passed==duration:
            break

        return list[user_guess]    
    cap.release()
# Destroy all the windows
    cv2.destroyAllWindows()

def get_computer_choice():
    guess={}
    with open('labels.txt') as f:
        for content in f:
            key,value=content.split()
            guess[key]=value
        f.close()
    computer_choice=random.choice(list(guess.values())).lower()
    return computer_choice




def get_prediction():
    while True:
        computer_choice=get_computer_choice()
        user_choice=get_user_choice()
        print("Computer_choice:",computer_choice)
        print("User_choice:",user_choice)
        if (computer_choice=="rock" and user_choice=="scissors") or (computer_choice=="paper" and user_choice=="rock") or (computer_choice=="scissors" and user_choice=="paper"):
            print("Computer wins")
            
             
        elif (computer_choice=="rock" and user_choice=="paper") or (computer_choice=="paper" and user_choice=="scissors") or (computer_choice=="scissors" and user_choice=="rock"):
            print("User wins")
            
            
        else:
            print("Draw game")
        print(time.time())
    
get_prediction()


