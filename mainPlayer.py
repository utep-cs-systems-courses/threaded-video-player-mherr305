#!/usr/bin/env python3
import numpy as np
import cv2
import threading
import queue
import os
import time

def put(queue,item):
    if queue==q1:
        emptyq.acquire()
        mutexq.acquire()
        queue.put(item)
        mutexq.release()
        fullq.release()

    else:
        emptyq2.acquire()
        mutexq2.acquire()
        queue.put(item)
        mutexq2.release()
        fullq2.release()

def get(queue):
    if queue==q1:
        fullq.acquire()
        mutexq.acquire()
        image= queue.get()
        mutexq.release()
        emptyq.release()

    else:
        fullq2.acquire()
        mutexq2.acquire()
        image = queue.get()
        mutexq2.release()
        emptyq2.release()

    return image

mutexq = threading.Lock()
mutexq2 = threading.Lock()

emptyq = threading.BoundedSemaphore(24)
fullq = threading.Semaphore(0)
emptyq2 = threading.BoundedSemaphore(24)
fullq2 = threading.Semaphore(0)

def extract(fileName, queue1, maxFrames=9999):
    counter=0
    vidcap = cv2.VideoCapture(fileName)
    success, image = vidcap.read()

    print(f'Reading frame {counter} {success}')

    while success and counter < maxFrames:
        
        success, jpgImage = cv2.imencode('.jpg', image)

        put(queue1,image)
        success, image = vidcap.read()
        print(f' Frame {counter} {success}')
        counter +=1
        
    print("Extraction of frames done!")

def convert(queue1, queue2, maxFrames=9999):
    counter=0
    while queue1 is not None and counter < 72:
        
        print(f'Executing converting to grayscale frame {counter}')
        grayScale =  cv2.cvtColor(get(queue1), cv2.COLOR_BGR2GRAY)
        counter += 1

        put(queue2,grayScale)
    
    print("Conversion to grayscale done!")

def display(queue2):
    counter= 0
    while not queue2.empty():
        
        nextFrame = queue2.get()
        print(f'Displaying frame {count}')

        cv2.imshow('Video', nextFrame)

        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        
        counter += 1
    print('Finished displaying all frames')
    cv2.destroyAllWindows()
    print("Execution done!")

clipName = 'clip.mp4'
frames = 400

q1 = queue.Queue()
q2 = queue.Queue()

firstThread = threading.Thread(target = extract , args=(clipName, q1, 72))
secondThread = threading.Thread(target = convert , args=(q1, q2, 72))
thirdThread = threading.Thread(target = display, args=(q2,))

firstThread.start()
secondThread.start()
thirdThread.start()
