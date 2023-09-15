import cvzone.HandTrackingModule
import cvzone.SerialModule
import cv2
import time

pTime = 0
cTime = 0
cap = cv2.VideoCapture(2)
detector = cvzone.HandTrackingModule.HandDetector(maxHands=1,detectionCon=0.7)
serial = cvzone.SerialModule.SerialObject("COM6",9600,1);

while True:
    success, img = cap.read()
    Hands, img = detector.findHands(img)

    if Hands:
        myHand = Hands[0]
        fingerList = detector.fingersUp(myHand)
        lmList = myHand["lmList"]

        thumbTip = lmList[4]
        center = lmList[0]
        if thumbTip[0] > center[0]:
            fingerList.append(1)
        else:
            fingerList.append(0)

#eddy 
        #serial.sendData(reversed(fingerList));
        serial.sendData(fingerList);



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime


    cv2.putText(img, str(int(fps)), (18, 78), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break


cap.release()
cv2.closeAllWindows
