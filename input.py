#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ComssServiceDevelopment.connectors.tcp.msg_stream_connector import OutputMessageConnector #import modułów konektora msg_stream_connector

from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi

import cv2 #import modułu biblioteki OpenCV
import Tkinter as tk #import modułu biblioteki Tkinter -- okienka

service_controller = DevServiceController("filter_service.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("videoInput", OutputMessageConnector(service_controller)) #deklaracja interfejsu wyjściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WEJŚCIEM usługi, do której "zaślepka" jest podłączana

service_controller2 = DevServiceController("save_video_service.json")

def update_all(root, cap, filters):
    read_successful, frame = cap.read() #odczyt obrazu z kamery
    new_filters = set()
    if check1.get()==1: #sprawdzenie czy checkbox był zaznaczony
        new_filters.add(1)
    if check2.get()==1:
        new_filters.add(2)
    print new_filters    
    if filters ^ new_filters:
        filters.clear()
        filters.update(new_filters)
        service_controller.update_params({"filtersOn": list(filters)}) #zmiana wartości parametru "filtersOn" w zależności od checkbox'a
    
    if read_successful:
        frame_dump = frame.dumps() #zrzut ramki wideo do postaci ciągu bajtów
        service_controller.get_connection("videoInput").send(frame_dump) #wysłanie danych
        root.update()
        root.after(20, func=lambda: update_all(root, cap, filters))
    else:
        service_controller.get_connection("videoInput").close()
        cap.release()
        root.quit()

root = tk.Tk()
root.title("Filters") #utworzenie okienka

cap = cv2.VideoCapture('test.mp4') #"podłączenie" do strumienia wideo z kamerki
video_format = list() # format video jako parametr
video_format.append(cap.get(5))
video_format.append(cap.get(3))
video_format.append(cap.get(4))
service_controller2.update_params({"videoFormat": video_format}) #frame rate, frame widrth, frame height do "videoFormat"

#obsługa checkbox'a
check1=tk.IntVar()
check2=tk.IntVar()
checkbox1 = tk.Checkbutton(root, text="Filter 1", variable=check1)
checkbox1.pack()
checkbox2 = tk.Checkbutton(root, text="Filter 2", variable=check2)
checkbox2.pack()

root.after(0, func=lambda: update_all(root, cap, set())) #dołączenie metody update_all do głównej pętli programu, wynika ze specyfiki TKinter
root.mainloop()