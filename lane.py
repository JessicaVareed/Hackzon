import matplotlib.pylab as plt
import cv2
import numpy as np
import tkinter
import PIL.Image
import PIL.ImageTk


def region_mask(img, vert):
    mask=np.zeros_like(img)
    match_colour=255
    
    cv2.fillPoly(mask, vert, match_colour)
    maskedImage= cv2.bitwise_and(img,mask)
    return maskedImage


def drawLines(img, lines):
    cpimg=np.copy(img)
    blankImage= np.zeros((cpimg.shape[0], img.shape[1], 3), dtype= np.uint8)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1,y1), (x2,y2), (0,255,0), thickness=3)

    img=cv2.addWeighted(img, 0.8, blankImage, 1, 0.0)
    return img



def process(image):
    height= image.shape[0]
    width= image.shape[1]
    
    region_vertice=[(0,height),
            (width/2,height/2),
            (width,height)]
    
    
    grayImage=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    cannyImage= cv2.Canny(grayImage, 100, 120)
    
    cropImage= region_mask(cannyImage, np.array([region_vertice],np.int32))
    
    line= cv2.HoughLinesP(cropImage, rho=2, theta=np.pi/60, threshold=50,
                           lines=np.array([]),
                           minLineLength=40, maxLineGap=25)
    
    imageLines=drawLines(image, line)
    return imageLines


def video():
    cap= cv2.VideoCapture(v1)

    frame_width =  int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    out=cv2.VideoWriter('output_video3.mp4',fourcc, 20,
                          (frame_width,frame_height))

    while(cap.isOpened()):
        ret, frame= cap.read()
        if ret == True: 
            frame= process(frame)      
        
            out.write(frame)
        
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()



class App:
    def __init__(self, window, video_source1, video_source2):
        self.window = window
        self.window.title("Raod Lane Tracking System")
        self.window.configure(bg="Thistle")
        #self.window.l1=tkinter.Label()
        #L1 = tkinter.Label(self.window, text="Input")
        #L1.pack()
        #L1.place(x=20, y=0, anchor='w')
        self.video_source1 = video_source1
        self.video_source2 = video_source2
        self.photo1 = ""
        self.photo2 = ""

        # open video source
        self.vid1 = MyVideoCapture(self.video_source1, self.video_source2)

        # Create a canvas that can fit the above video source size
        self.canvas1 = tkinter.Canvas(window, width=500, height=500)
        self.canvas2 = tkinter.Canvas(window, width=500, height=500)
        self.canvas1.pack(padx=5, pady=10, side="left")
        self.canvas2.pack(padx=5, pady=60, side="left")

        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret1, frame1, ret2, frame2 = self.vid1.get_frame

        if ret1 and ret2:
                self.photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
                self.photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
                self.canvas1.create_image(0, 0, image=self.photo1, anchor=tkinter.NW)
                self.canvas2.create_image(0, 0, image=self.photo2, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)



class MyVideoCapture:
    def __init__(self, video_source1, video_source2):
        # Open the video source
        self.vid1 = cv2.VideoCapture(video_source1)
        self.vid2 = cv2.VideoCapture(video_source2)

        if not self.vid1.isOpened():
            raise ValueError("Unable to open video source", video_source1)

    @property
    def get_frame(self):
        ret1 = ""
        ret2 = ""
        if self.vid1.isOpened() and self.vid2.isOpened():
            ret1, frame1 = self.vid1.read()
            ret2, frame2 = self.vid2.read()
            frame1 = cv2.resize(frame1, (500, 500))
            frame2 = cv2.resize(frame2, (500, 500))
            if ret1 and ret2:
                # Return a boolean success flag and the current frame converted to BGR
                return ret1, cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB),ret2, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            else:
                return ret1, None, ret2, None
        else:
            return ret1, None, ret2, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid1.isOpened():
            self.vid1.release()
        if self.vid2.isOpened():
            self.vid2.release()


def callback():
    global v1,v2
    v1=E1.get()
    video()
    v2='output_video3.mp4'
    if v1 == "" or v2 == "":
        L3.pack()
        L3.place(x=425,y=330,anchor='center')
        return
    root.destroy()
      

v1 = ""
v2 = ""

root = tkinter.Tk()
root.geometry('850x500')
root.configure(bg="Thistle")
root.title("Road Lane Tracking")
lb=tkinter.Label(root, text="ROAD LANE TRACKING FOR SELF DRIVING CARS", 
                 font=("Arial", 25),
                 justify=tkinter.CENTER)
lb.pack()
lb.place(x=425,y=100,anchor='center')
L1 = tkinter.Label(root, text="Video name")
L1.pack()
L1.place(x=425,y=225, anchor='center')
E1 = tkinter.Entry(root, bd =5)
E1.pack()
E1.place(x=425, y=260, anchor='center')
B = tkinter.Button(root, text ="Next",
                   bg="SlateBlue", 
                   command = callback)
B.pack()
B.place(x=425,y=300, anchor='center')
L3 = tkinter.Label(root, text="Enter the name of the video")

root.mainloop()


App(tkinter.Tk(),v1,v2)

    
