import numpy as np
import cv2
import RPi.GPIO as GPIO
import picamera
import motor
import time
import ultrasonic
import paho.mqtt.client as mqtt
broker_address = "35.165.89.144"
topic = "linetracking"
topic2 = "Carcontrol"
port = 1883
activated = False
signal = None

US=ultrasonic
m1=motor
def process_image():
    with picamera.PiCamera() as camera:
        # Set capture resolution
        camera.resolution = (640, 480)
        # Set capture fps
        camera.framerate = 30
        # Define start_time and frame_count variables for fps calculation
        start_time = time.time()
        frame_count = 0
        while activated:
            frame = np.empty((480, 640, 3), dtype=np.uint8)

            # Capture video
            camera.capture(frame, 'bgr', use_video_port=True)

            # Flip capture
            frame = cv2.flip(frame, 0)

            # Crop frame in the capture
            size = 300
            x = (640 - size)//2
            y = (480 - 300) // 2
            crop_size = 300
            crop_frame = frame[y:y+300, x:x+crop_size]

            # Increase brightness
            gamma = 1.5
            crop_frame = cv2.pow(crop_frame / 255.0, gamma)
            crop_frame = cv2.normalize(
                crop_frame, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

            # Convert to GrayScale
            gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)

            # Apply GaussianBlur to the grayscale iamge
            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            ret, thresh1 = cv2.threshold(
                blur, 25, 255, cv2.THRESH_BINARY_INV)  # Thresh hold the image

            mask = cv2.erode(thresh1, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            _, contours, hierarchy = cv2.findContours(
                mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                if len(c) > 0:
                    M = cv2.moments(c)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    cv2.line(crop_frame, (cx, 0), (cx, 720),
                             (255, 0, 0), 1)  # draw cx
                    cv2.line(crop_frame, (0, cy),
                             (1280, cy), (255, 0, 0), 1)  # draw cy
                    cv2.drawContours(crop_frame,
                                     contours, -1, (0, 255, 0), 1)  # draw contours

                    # print cordidate cx and cy
                    print(cx, cy, end='')
                    print()
                    # Control the car base on cordidate cx
                    if cx >= 230:
                        m1.turn_right()
                    elif cx < 325 and cx > 75:
                        m1.forward()
                    elif cx <= 75:
                        m1.turn_left()
                else:
                    m1.backward()
                # Show the capture with contour
                cv2.imshow('Track Line', crop_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    camera.stop_preview()
                    cv2.destroyAllWindows()
                    m1.p1.stop()
                    m1.p2.stop()
                    GPIO.cleanup()
                    break
                
                # Calculate fps
                frame_count += 1
                if frame_count % 10 == 0:
                    elapsed_time = time.time() - start_time
                    fps = frame_count / elapsed_time
                    print(f'FPS: {fps:.2f}')
                    

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic2)


def on_message(client, userdata, msg):
    print(" " + str(msg.payload))
    signal = str(msg.payload)
    global activated
    if signal == "b'ACTIVATE'":
        activated = True
    elif signal == "b'DEACTIVATE'":
        activated = False

client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker_address, port, 60)
client.on_message = on_message

# Initialize Rasp Pi camera
while True:
    client.loop_start()
    if activated:
        process_image()
    else:
        m1.stop()
    client.loop_stop()
