#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 8 sty 2016

@author: Sobot
'''
from ComssServiceDevelopment.connectors.tcp.msg_stream_connector import InputMessageConnector #import modułów konektora msg_stream_connector

from ComssServiceDevelopment.service import Service, ServiceController #import modułów klasy bazowej Service oraz kontrolera usługi

class SaveVideoService(Service): #klasa usługi musi dziedziczyć po ComssServiceDevelopment.service.Service
    def __init__(self):            #"nie"konstruktor, inicjalizator obiektu usługi
        super(SaveVideoService, self).__init__() #wywołanie metody inicjalizatora klasy nadrzędnej
    
    def declare_outputs(self): #deklaracja wyjść
        pass

    def declare_inputs(self): #deklaracja wejść
        self.declare_input("audioInput", InputMessageConnector(self)) #deklaracja wejścia "videoInput" będącego interfejsem wyjściowym konektora msg_stream_connector
        
    def run(self):    #główna metoda usługi
        audio_input = self.get_input("audioInput")    #obiekt interfejsu wejściowego
        input_start = True
        out = None

        while self.running():   #pętla główna usługi
            try:
                #################################################################
                # na razie leci video, ma leciec audio!!!
                #################################################################
                frame_obj = audio_input.read()  #odebranie danych z interfejsu wejściowego
            except Exception as e:
                audio_input.close()
                if out != None:
                    out.release()
                break
            if input_start:
                #######################################################
                # tu inicjalizacja pliku do zapisu
                #######################################################
                input_start = False
            ###########################################################
            # tu zapisywanie audio
            ###########################################################

if __name__=="__main__":
    sc = ServiceController(SaveVideoService, "save_audio_service.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi
