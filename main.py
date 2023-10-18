import cvzone.HandTrackingModule as htm
import cvzone.SerialModule as srl
import mediapipe as mp
import serial as ser
import cv2
import time

pTime = 0
cTime = 0
# Initialize OpenCV and MediaPipe Hands
cap = cv2.VideoCapture(0)

detector = htm.HandDetector(detectionCon=0.7)
serial = srl.SerialObject("COM6",9600,1)
arduino = ser.Serial("", 9600)


square_size = 225
square_x = 100
square_y = 100
square_color = (0, 0, 255)
square_thickness = 2
text_color = (0, 0, 0)
text_font = cv2.FONT_HERSHEY_SIMPLEX
text_size = 1
text_thickness = 1

timer_durantion = 30


def draw_hollow_square(image, x, y, size, color, thickness):
    cv2.rectangle(image, (x, y), (x + size, y + size), color, thickness)

def runCamera():
    start_time = time.time()
    while start_time <= timer_durantion:
        success, image = cap.read()
        Hands, image = detector.findHands(image, draw=False)


        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        draw_hollow_square(image, square_x, square_y, square_size, square_color, square_thickness)
        draw_hollow_square(image, square_x * 4, square_y, square_size, square_color, square_thickness)
        cv2.putText(image, "Right hand", (square_x, square_y + 220), text_font, text_size, text_color, text_thickness)
        cv2.putText(image, "Left hand", (square_x * 4, square_y + 220), text_font, text_size, text_color, text_thickness)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(image, str(int(fps)), (18, 78), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # Loop through detected hands
        for hand in Hands:
            lmList = hand["lmList"]
            if square_x <= lmList[8][0] <= square_x + square_size and square_y <= lmList[8][1] <= square_y + square_size:
                # Draw landmarks or process the hand here
                Hands, image = detector.findHands(image)

                #finger Data sent to arduino
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

                    # serial.sendData(reversed(fingerList));
                    serial.sendData(fingerList)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow("Output", image)
        cv2.waitKey(1)



if __name__ == '__main__':
    while True:
        # Read data from the Arduino
        serial.getData()
        if data == "ButtonPressed":
            runCamera()