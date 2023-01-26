# Hackzon 2023

## Lane Tracking for self driving cars

This application is used to track road lanes by passing input video of the road thus producing the desired output detecting the lanes of the road. Open CV open source library is used to process videos. Each of the image frames are analysed by Numpy library to get the image pixel values. The detection of lanes is done by frame masking and Hough Line Transform.

## Smaple Output

![image](https://user-images.githubusercontent.com/113986649/213741244-0c6d0cc5-aec8-4326-befa-afc9ed222e23.png)

The home page allows to enter the video name that has to be processed and the next button which helps to move to the next page. 

![image](https://user-images.githubusercontent.com/113986649/213743137-f0345abf-7469-4b4c-a41c-5383c02b187b.png)

In the text field if there is no input then an error message is displayed and we can type the input again.  

![image](https://user-images.githubusercontent.com/113986649/213741617-9496a7c4-94e7-42ec-8a59-b0c558219080.png)

In this application, the output video as well as the input video will be displayed side by side. The output video of the road lanes will have the lanes detected in a different highlighted colour. 
