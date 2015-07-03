#-*- coding=utf-8 -*-

import os
import SocketServer
import threading

import cv2.cv as cv
import cv2
import time
import pyaudio
import numpy as np
import scipy.ndimage
from numpy.ma.core import exp
from scipy.constants.constants import pi


import get_SSIM
import get_WAV_Freq
import record_WAV_File


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
SOCKET_RECV_DATA = ""
SOCKET_SEND_DATA = ""


#-------------------------------------------------------------------------------
'''
Picture operature
'''             
class HDMI_OCR_VIDEO:
    def __init__(self):
        pass

    def run(self):
        #inint the videoCapture
        capture = cv2.VideoCapture(0)
        time.sleep(2)
        if not capture.isOpened():
            capture.open()
            
        # Port 0 means to select an arbitrary unused port
        HOST, PORT = '127.0.0.1', 12640

        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
		
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print ("OCR socket server running")
        
        while True:
            ret, self.frame = capture.read()
            
            #resize the image
            d = capture.get(cv.CV_CAP_PROP_FRAME_WIDTH)
            h = capture.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
            #cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
            #cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGH, 480)
            
            if self.frame is not None:
                dst = self.frame
                #cv2.namedWindow("HDMI_OCR", cv2.WINDOW_NORMAL)
                cv2.cv.ResizeWindow("HDMI_OCR", 721, 481)
                '''
                if d > 640 or h > 480 :
                    dst = cv2.resize(self.frame, (640, 480))
                '''
                cv2.imshow("HDMI_OCR", dst)
            else:
                continue

            c = cv.WaitKey(1) & 0xFF
            #print('The press key is: ', c)
            #Press 'ESC', destroy the windows()
            if c == 27:                
                cv.DestroyAllWindows()       
                break
            #Press 'c' or 'C', capture the current picture
            elif (c == ord('c') or c == ord('C')):                
                try:
                    self.capture_Image()
                except:
                    print("cv2.imwrite error")

            '''
            if recv the client socket data, judge the data and do the different operater
            '''
            global SOCKET_RECV_DATA
            global SOCKET_SEND_DATA
            if len(SOCKET_RECV_DATA) > 1:
                print(SOCKET_RECV_DATA)
            if "cap" in SOCKET_RECV_DATA.lower():
                SOCKET_RECV_DATA = ""
                try:
                    self.capture_Image()
                except:
                    print("capture_Image error")
                finally:
                    pass              
            else:
                #print('please check the command \'%s\' is right' % SOCKET_RECV_DATA)
                SOCKET_RECV_DATA = ""
                time.sleep(0.05)
        
        server.shutdown()
        server.server_close()


        
#-------------------------------------------------------------------------------
    def capture_Image(self):
        filename = SCRIPT_PATH + "\cap.bmp"
        cv2.imwrite(filename, self.frame)


#compare the two images's SSIM rate        
#-------------------------------------------------------------------------------
    def compare_Image(self, filename):
        sir = "-999"
        #capture current picture
        try:
            self.capture_Image()        

            #get the SSIM rate both the test image and the SPEC image
            img1 = cv2.imread(SCRIPT_PATH + r"\cap.bmp")
            img2 = cv2.imread(SCRIPT_PATH + "\\" + filename)
           
            sir = get_SSIM.compute_ssim(img1, img2)
            print("The two image's SSIM rate is : %s" % sir)
        except:
            print("get_SSIM error")
        finally:
            return sir
    
#-------------------------------------------------------------------------------
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        global SOCKET_RECV_DATA
        SOCKET_RECV_DATA = self.request.recv(1024)
        #print(SOCKET_RECV_DATA)

        #loop read the send buffer isChanged, if changed send the data back to the socket
        while True:            
            global SOCKET_SEND_DATA
            if len(SOCKET_SEND_DATA) :
                print(SOCKET_SEND_DATA)
                self.request.send(SOCKET_SEND_DATA)
                SOCKET_SEND_DATA = ""
            else:
                time.sleep(0.2)
    
#-------------------------------------------------------------------------------
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

	