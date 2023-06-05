import cvzone.HandTrackingModule
import cvzone.SerialModule
import cv2
import time;
cap = cv2.VideoCapture(1)
detector = cvzone.HandTrackingModule.HandDetector(maxHands=1, detectionCon=0.7)
mySerial = cvzone.SerialModule.SerialObject(portNo="COM9")
pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand1 = hands[0]
        fingers = detector.fingersUp(hand1)
        mySerial.sendData(reversed(fingers))
        #print(fingers)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()