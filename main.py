import time
import cv2
import HandTrackingModule as htm
import cvzone.SerialModule as srl

# Initialize OpenCV and MediaPipe Hands
cap = cv2.VideoCapture(0)

detector = htm.HandDetector(detectionCon=0.7)
serial = srl.SerialObject("COM6", 9600, 1)

square_size = 225
square_x = 100
square_y = 100
square_color = (0, 0, 255)
square_thickness = 2
text_color = (0, 0, 0)
text_font = cv2.FONT_HERSHEY_SIMPLEX
text_size = 1
text_thickness = 1

timer_duration = 15

def draw_hollow_square(image, x, y, size, color, thickness):
    cv2.rectangle(image, (x, y), (x + size, y + size), color, thickness)

def run_camera():
    start_time = time.time()
    while time.time() - start_time < timer_duration:
        success, image = cap.read()

        Hands, image = detector.findHands(image, draw=False)
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        draw_hollow_square(image, square_x, square_y, square_size, square_color, square_thickness)
        draw_hollow_square(image, square_x * 4, square_y, square_size, square_color, square_thickness)

        cv2.putText(image, "Right hand", (square_x, square_y + 220), text_font, text_size, text_color, text_thickness)
        cv2.putText(image, "Left hand", (square_x * 4, square_y + 220), text_font, text_size, text_color, text_thickness)

        for hand in Hands:
            lmList = hand["lmList"]
            if square_x <= lmList[8][0] <= square_x + square_size and square_y <= lmList[8][1] <= square_y + square_size:
                Hands, image = detector.findHands(image)
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

                    serial.sendData(fingerList)

        cv2.imshow("Output", image)
        cv2.waitKey(1)


# TODO: implement somthing to read the arduino data so
#  that we can run run_camera() once we press a button.
if __name__ == '__main__':
    run_camera()

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
