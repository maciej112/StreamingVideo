#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from ComssServiceDevelopment.connectors.tcp.msg_stream_connector import InputMessageConnector, OutputMessageConnector #import modułów konektora msg_stream_connector

from ComssServiceDevelopment.service import Service, ServiceController #import modułów klasy bazowej Service oraz kontrolera usługi
import cv2 #import modułu biblioteki OpenCV
import numpy as np #import modułu biblioteki Numpy

class FilterAudioService(Service): #klasa usługi musi dziedziczyć po ComssServiceDevelopment.service.Service
    def __init__(self):            #"nie"konstruktor, inicjalizator obiektu usługi
        super(FilterAudioService, self).__init__() #wywołanie metody inicjalizatora klasy nadrzędnej
        
        self.filters_lock = threading.RLock() #obiekt pozwalający na blokadę wątku

    def declare_outputs(self):    #deklaracja wyjść
        self.declare_output("videoOutput", OutputMessageConnector(self)) #deklaracja wyjścia "videoOutput" będącego interfejsem wyjściowym konektora msg_stream_connector
        
    def declare_inputs(self): #deklaracja wejść
        self.declare_input("videoInput", InputMessageConnector(self)) #deklaracja wejścia "videoInput" będącego interfejsem wyjściowym konektora msg_stream_connector

    def run(self):    #główna metoda usługi
        video_input = self.get_input("videoInput")    #obiekt interfejsu wejściowego
        video_output = self.get_output("videoOutput") #obiekt interfejsu wyjściowego
        
        while self.running():   #pętla główna usługi
            try:
                frame_obj = video_input.read()  #odebranie danych z interfejsu wejściowego
            except Exception as e:
                video_input.close()
                video_output.close()
                break
            frame = np.loads(frame_obj)     #załadowanie ramki do obiektu NumPy
            with self.filters_lock:     #blokada wątku
                current_filters = self.get_parameter("filtersOn") #pobranie wartości parametru "filtersOn"

            if 1 in current_filters:    #sprawdzenie czy parametr "filtersOn" ma wartość 1, czyli czy ma być stosowany filtr
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #zastosowanie filtru COLOR_BGR2GRAY z biblioteki OpenCV na ramce wideo
            
            if 2 in current_filters:
                frame = cv2.blur(frame,(5,5))
                
            if 3 in current_filters:
                frame = cv2.GaussianBlur(frame,(5,5),0)
                
            if 4 in current_filters:
                frame = cv2.medianBlur(frame,5)
                
            video_output.send(frame.dumps()) #przesłanie ramki za pomocą interfejsu wyjściowego

if __name__=="__main__":
    sc = ServiceController(FilterAudioService, "filter_video_service.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi

