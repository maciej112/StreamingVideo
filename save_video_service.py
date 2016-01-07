#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 7 sty 2016

@author: Sobot
'''
from ComssServiceDevelopment.connectors.tcp.msg_stream_connector import InputMessageConnector, OutputMessageConnector #import modułów konektora msg_stream_connector

from ComssServiceDevelopment.service import Service, ServiceController #import modułów klasy bazowej Service oraz kontrolera usługi
import cv2 #import modułu biblioteki OpenCV
import numpy as np #import modułu biblioteki Numpy

class SaveVideoService(Service): #klasa usługi musi dziedziczyć po ComssServiceDevelopment.service.Service
    def __init__(self):            #"nie"konstruktor, inicjalizator obiektu usługi
        super(SaveVideoService, self).__init__() #wywołanie metody inicjalizatora klasy nadrzędnej
    
    def declare_outputs(self): #deklaracja wyjść
        pass

    def declare_inputs(self): #deklaracja wejść
        self.declare_input("videoInput", InputMessageConnector(self)) #deklaracja wejścia "videoInput" będącego interfejsem wyjściowym konektora msg_stream_connector

    def run(self):    #główna metoda usługi
        video_input = self.get_input("videoInput")    #obiekt interfejsu wejściowego
        input_start = True

        while self.running():   #pętla główna usługi
            try:
                frame_obj = video_input.read()  #odebranie danych z interfejsu wejściowego
                if input_start:
                    video_format = self.get_parameter("videoFormat")
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    out = cv2.VideoWriter('output.avi',fourcc, video_format.get(0), (video_format.get(1),video_format.get(2)))
                    input_start = False
            except Exception as e:
                video_input.close()
                out.release()
                break
            frame = np.loads(frame_obj)     #załadowanie ramki do obiektu NumPy
            out.write(frame)


if __name__=="__main__":
    sc = ServiceController(SaveVideoService, "save_video_service.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi