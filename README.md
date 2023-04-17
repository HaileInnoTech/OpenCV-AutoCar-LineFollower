# OpenCV-AutoCar-LineFollower
This is a group project using Raspberry 4 + Camera Pi and OpenCV module to detect a line, and control the car to follow the line.

Attributor:
      1. Hai Le
      
      2. Quoc Bao
      
      3. Nhat Huy

The aim of our project is to create a mini smart car that will be able to detect obstacles, track and automatically follow a line through a mounted camera. A full-fledged IoT communication will be established between the IoT node (the car) and the edge device through an MQTT broker. A cloud computing platform is also utilized through use of an AWS (Amazon Web Service) EC2 server. 

Hardware requirement:
      Raspberry Pi 4B 
      Camera Raspberry Pi V1 
      HC-SR04 Ultrasonic sensor 
      L293D Motor driver 
      Car chassis (4 wheels + motors) 
      Power bank 5V (two 18650 batteries) 
      Charger 
      Jumper wires 
      USB Type-C cable 
      32GB MicroSD card Breadboard 
      GPIO Breakout extension board 
      
Sofware requirement:
      Raspbian OS Buster VMWare 
      PuTTY SSH session 
      OpenCV 3.0 
      Cloud server (Amazon Web Service EC2) 
      Visual Studio Code 
      Python 2.7 
      Cloud ware 
      MySQL server 
      Mosquito MQTT broker 
      Android OS 
      
      
CONCEPTUAL DESIGN
  For a car to be considered smart, it needs to employ various IoT technologies such as sensors, processors, actuators, and other communication devices. Smart cars should be able to drive itself automatically while avoiding obstacles on the road as well as being able to connect to other IoT devices within the network. We implemented an ultrasonic sensor on the front to detect obstacles and a camera to implement self-driving. The Raspberry Pi will be the brain of the IoT node, receiving information from the sensors and sending signals to the motor drivers to move the car. 
  
Block diagram:

![image](https://user-images.githubusercontent.com/114500456/232432662-511ad98a-f364-494f-ad5f-6dacc2774ea0.png)

IMPLEMENTATION
1. Sensing System 
This system utilizes two main sensing system: an ultrasonic sensor (model HC-SR04) used to detect objects and a camera (Camera V1) coded to automatically follow a road made up of two lines. 
First, the ultrasonic sensor is a type of sensor that sends out ultrasonic waves through a transmitter that bounces off objects and reflects back to the sensor’s receiver. The interval between sending and receiving waves can be used to measure the distance between the object and the sensor itself. In this context, the sensor is mounted on the front to detect obstacles on the road, and then relaying that information to the Raspberry for it to process and take appropriate actions. 
An ultrasonic sensor has 4 pins: VCC, Trig, Echo and GND. The VCC pin is responsible for powering up the sensor itself, thus it is connected to the 5V pin from the GPIO Extension board. The GND pin provides ground connection and is subsequently connected to the GND pin on the Extension board. Trig is the input pin that sends out ultrasonic waves while Echo is the output pin that receives the bounced echo signal and sends that information back to the Raspberry Pi for processing. 

![image](https://user-images.githubusercontent.com/114500456/232433021-729a2fe4-aeeb-4880-bf77-af10c971ddc1.png)

![image](https://user-images.githubusercontent.com/114500456/232433091-b082280e-52ce-4e83-8099-ae2d804262c9.png)
  
Secondly, a custom camera is set up to capture and process images in real-time. The camera is coded to analyze the image captured and draw relevant lines for the car to track. By implementing a computer vision algorithm known as color thresholding, the car can detect and maintain its center position along the lines drawn.  
Color thresholding is an image processing method that changes all pixels within a specified color range to white and anything outside of it to black. First, we greyscale the captured image for easier processing, then convert it to a binary image using thresholding by setting all pixels to white when above a certain color threshold and anything below it to black. The result is a binary image where the points of interest are painted white while other background items are black. We then identify the connected areas in the binary image to form contours and apply a centroid calculation on them to be able to detect the center of the shapes, or in this case lines, for the car to follow. We also included extra steps to clean up the binary image using erosion and dilation, formally called morphological operations, for more accurate processing. 

![image](https://user-images.githubusercontent.com/114500456/232433155-ec785ced-e067-4ccf-b4f5-e82c1262f234.png)

2. Cloud Computing 
This car features a cloud computing platform in form of an EC2 (Elastic Compute Cloud) server hosted on AWS (Amazon Web Service). EC2 is a web service that allows you to host your own virtual servers (called Instances) where you can run your custom applications. The instances themselves are quite configurable in terms of operating systems and software configurations, while being highly scalable to suit the user’s needs.  

![image](https://user-images.githubusercontent.com/114500456/232433387-82d7bbac-bc2d-4ec8-ac53-c311e586127f.png)

On the cloud, we also implemented a MySQL server to store the car’s instructions into a database for processing, among other relevant information. 

![image](https://user-images.githubusercontent.com/114500456/232433432-079ba39b-af12-4879-be10-7492e72eeacd.png)  
 	 
An SQL table called MOVEMENT is created with several columns: 
+) No: Item number in the list. 
+) Time: Date and time when the data is recorded. 
+) CarMovement: Status message of the car.  
When the car runs, the table is populated with data. 

![image](https://user-images.githubusercontent.com/114500456/232433506-5cfeed75-e68c-4ff6-b08a-32c628577c65.png)

![image](https://user-images.githubusercontent.com/114500456/232433517-f7250c37-6fed-40ea-9ea6-1ab05f82df38.png)

3. Communication Protocol 
For our IoT communication protocol, we have set up a Mosquito MQTT broker to serve as a central point for communication between the car and the edge device. The car publishes messages in a “topic” to the broker, which is then forwarded to the edge device that is subscribed to said “topic”. The broker itself has administrator role which allows it to access and publish/subscribe data through the internet. 

![image](https://user-images.githubusercontent.com/114500456/232433684-18e60ade-2374-4234-beb8-ffe7ff9d73b7.png)

4. Edge Server 
In IoT, an edge server is a server on the edge of a network that provides localized processing and data storage which reduces the need to constantly transport data to and from data centers, resulting in improved performance. For this project, we are hosting a virtual Raspbian OS edge server using VMWare. The edge server receives data collected from the car through the MQTT broker and upload it to the database. 

![image](https://user-images.githubusercontent.com/114500456/232433745-56705d0c-b998-4bed-8db6-bfbda92d151e.png)

![image](https://user-images.githubusercontent.com/114500456/232433788-d7226b2c-8150-4b24-b338-e3fa5bc343cb.png)

5. Mobile Application (User Interface/Control) 
We also included a mobile application to allow control over the car anywhere at any time. By using the online website MIT App Inventor, we have designed a simple app that enables the user to turn the car on and off at will. The app will connect and send instructions to the MQTT broker, which then forwards it to the car to take appropriate actions. 
![image](https://user-images.githubusercontent.com/114500456/232433845-7aafd270-10f7-41d3-b2f4-d727f3ffd5b9.png)
![image](https://user-images.githubusercontent.com/114500456/232433855-a511af4d-7872-4006-ac87-ea8f1a4a9d6d.png)






  
   




  
 
 



