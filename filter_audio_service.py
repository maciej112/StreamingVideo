#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 8 sty 2016

@author: Sobot
'''
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
        self.declare_output("audioOutput", OutputMessageConnector(self)) #deklaracja wyjścia "videoOutput" będącego interfejsem wyjściowym konektora msg_stream_connector
        
    def declare_inputs(self): #deklaracja wejść
        self.declare_input("audioInput", InputMessageConnector(self)) #deklaracja wejścia "videoInput" będącego interfejsem wyjściowym konektora msg_stream_connector

    def run(self):    #główna metoda usługi
        audio_input = self.get_input("audioInput")    #obiekt interfejsu wejściowego
        audio_output = self.get_output("audioOutput") #obiekt interfejsu wyjściowego
        
        while self.running():   #pętla główna usługi
            try:
                #################################################################
                # na razie leci video, ma leciec audio!!!
                #################################################################
                frame_obj = audio_input.read()  #odebranie danych z interfejsu wejściowego
            except Exception as e:
                audio_input.close()
                audio_output.close()
                break
            frame = np.loads(frame_obj)     #załadowanie ramki do obiektu NumPy
            with self.filters_lock:     #blokada wątku
                current_filters = self.get_parameter("filtersOn") #pobranie wartości parametru "filtersOn"
            
            ############################################################    
            # tu mają być filtry audio
            ############################################################
            audio_output.send(frame.dumps()) #przesłanie ramki za pomocą interfejsu wyjściowego

if __name__=="__main__":
    sc = ServiceController(FilterAudioService, "filter_audio_service.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi