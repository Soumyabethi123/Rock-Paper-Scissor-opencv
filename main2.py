import random

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)

cap.set(3,640) #Width = 640
cap.set(4,480)  #Height = 480

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0 , 0]  #[ AI , Player ]

while True:

    imgBg = cv2.imread("BG.png")

    success , img = cap.read()

    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)

    imgScaled = imgScaled[:,80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)

    playermove = None
    randomnumber = None

    if startGame:


        if stateResult is False:

            timer = time.time() - initialTime
            cv2.putText(imgBg,str(int(timer)),(605,435),cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4)

            if timer > 3:
                stateResult = True

                timer =0

                if hands:

                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers==[0,0,0,0,0]:
                        playermove=1

                    elif fingers==[1,1,1,1,1]:
                        playermove=2

                    elif fingers==[0,1,1,0,0]:
                        playermove=3

                    print(playermove)

                    randomnumber = random.randint(1,3)

                    imgAI = cv2.imread(f'{randomnumber}.png',cv2.IMREAD_UNCHANGED)
                    imgBg = cvzone.overlayPNG(imgBg,imgAI,(149,310))

                    flag = 0

                    if (randomnumber == 1 and playermove == 3):
                        flag = 1
                        scores[0] = scores[0] + 1

                    if (randomnumber == 2 and playermove == 1):
                        flag = 1
                        scores[0] = scores[0] + 1

                    if (randomnumber == 3 and playermove == 2):
                        flag = 1
                        scores[0] = scores[0] + 1

                    if (flag == 0):

                        if (randomnumber != playermove):
                            scores[1] = scores[1] + 1

    imgBg[234:654,795:1195] = imgScaled

    if stateResult:
        imgBg = cvzone.overlayPNG(imgBg, imgAI, (149, 310))


    cv2.putText(imgBg, str(scores[0]), (410,215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBg, str(scores[1]), (1112,215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG Image",imgBg)


    key = cv2.waitKey(1)

    if(key==ord('s')):

        startGame=True
        initialTime = time.time()
        stateResult=False