import time
import cv2
import HandTrackingModule as htm
import cvzone.SerialModule as srl

# Initialize OpenCV and MediaPipe Hands
cap = cv2.VideoCapture(0)

detector = htm.HandDetector(detectionCon=0.7)
serial = srl.SerialObject("COM3", 9600, 1)

square_size = 225
square_x = 100
square_y = 100
square_color = (0, 0, 255)
square_thickness = 2
text_color = (0, 0, 0)
text_font = cv2.FONT_HERSHEY_SIMPLEX
text_size = 1
text_thickness = 1

timer_duration = 30


def draw_hollow_square(image, x, y, size, color, thickness):
    cv2.rectangle(image, (x, y), (x + size, y + size), color, thickness)


def run_camera():
    draw_hands = False

    start_time = time.time()
    while time.time() - start_time < timer_duration:
        success, image = cap.read()


        hands, image = detector.findHands(image, draw_hands)  # finding hands without drawing them on screen

        # Drawing the limit boxes in the image
        draw_hollow_square(image, square_x, square_y, square_size, square_color, square_thickness)
        draw_hollow_square(image, square_x * 4, square_y, square_size, square_color, square_thickness)

        # Drawing indicating text for hands boxes
        cv2.putText(image, "Right hand", (square_x, square_y + 220), text_font, text_size, text_color, text_thickness)
        cv2.putText(image, "Left hand", (square_x * 4, square_y + 220), text_font, text_size, text_color,
                    text_thickness)

        if len(hands) == 2:  # if both hands are detected

            if hands[0]["type"] == "Right":  # is first hand detected RIGHT hand
                right_hand = hands[0]
                left_hand = hands[1]
            else:  # if not make first hand detected Left
                left_hand = hands[0]
                right_hand = hands[1]

            # initializing right and left hands landmarks
            right_hand_lmList = right_hand["lmList"]
            left_hand_lmList = left_hand["lmList"]

            # if hands are inside drawn limit boxes
            if (square_x <= right_hand_lmList[9][0] <= square_x + square_size
                    and square_y <= right_hand_lmList[9][1] <= square_y + square_size
                    and square_x * 4 <= left_hand_lmList[9][0] <= square_x * 4 + square_size
                    and square_y <= left_hand_lmList[9][1] <= square_y + square_size):

                draw_hands = True  # Draw hands

                if hands:
                    myHand = hands[0]
                    fingerList = detector.fingersUp(myHand)
                    lmList = myHand["lmList"]

                    thumbTip = lmList[4]
                    center = lmList[0]
                    if thumbTip[0] > center[0]:
                        fingerList.append(1)
                    else:
                        fingerList.append(0)

                    serial.sendData(fingerList)  # send finger data to arduino

            else:
                draw_hands = False

        cv2.imshow("Output", image)
        cv2.waitKey(1)


# TODO: implement somthing to read the arduino data so
#  that we can run run_camera() once we press a button.
if __name__ == '__main__':
    run_camera()
    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
