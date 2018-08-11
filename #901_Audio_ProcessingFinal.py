############################################################################
#									   #
#			Musical Note Identification			   #
#									   #
############################################################################

########################################################################################
#                                                                                      #
# Team Id           eYRC-BV#901                                                        #
# Author List       Chetan Chawla, Divyansh Malhotra, Harshil Bansal, Ishani Janveja   #
# Filename          #901_Audio_Processing.py                                           #
# Track             3                                                                  #
# Theme             Bothoven                                                           #
# Fuctions          findNote,findFrequency,play                                        #
# Gloabal Varibles  sampling_freq,window_size,notes,note_freq,Identified_Notes1,k      # 
#                                                                                      #
########################################################################################

import numpy as np
import wave
import struct
import serial
import time

ser = serial.Serial("COM8", 9600)   # open serial port through which data is to be sent

sampling_freq = 44100	                                                                                            # Sampling frequency of audio signal
window_size = 1000                                                                                                  # Window size for silence detection
notes=['C6','D6','E6','F6','G6','A6','B6','C7','D7','E7','F7','G7','A7','B7','C8','D8','E8','F8','G8','A8','B8']
rep=[2,3,4,5,6,0,1,9,10,11,12,13,7,8,16,17,18,19,20,14,15]                                                                                                                    #notes-list containing all the notes in order
#rep=['c','d','e','f','g','a','b','j','k','l','m','n','h','i','q','r','s','t','u','o','p']                                                                                                                    #of increasing frequency
note_freq=[1080,1204,1350,1430,1590,1794,2010,2150,2382,2690,2848,3190,3573,3970,4240,4752,5325,5642,6325,7095,7990]
                                                                                                                    #note_freq-list containing the upper limit of
                                                                                                                    #the frequencies respective to the note array
Identified_Notes1=[]#it is the array storing the final notes
mapNotes=[]
k=[]#it is storing the frequncies calculated from the samples
def mapp(i):
    if(i==0):
        ser.write(b'c')
    if(i==1):
        ser.write(b'd')
    if(i==2):
        ser.write(b'e')
    if(i==3):
        ser.write(b'f')
    if(i==4):
        ser.write(b'g')
    if(i==5):
        ser.write(b'a')
    if(i==6):
        ser.write(b'b')
    if(i==7):
        ser.write(b'j')
    if(i==8):
        ser.write(b'k')
    if(i==9):
        ser.write(b'l')
    if(i==10):
        ser.write(b'm')
    if(i==11):
        ser.write(b'n')
    if(i==12):
        ser.write(b'h')
    if(i==13):
        ser.write(b'i')
    if(i==14):
        ser.write(b'q')
    if(i==15):
        ser.write(b'r')
    if(i==16):
        ser.write(b's')
    if(i==17):
        ser.write(b't')
    if(i==18):
        ser.write(b'u')
    if(i==19):
        ser.write(b'q')
    if(i==20):
        ser.write(b'r')
    
def findNote(frequency):                                                                                            #this function is used to find the note corresponding to the frequency
    i=0
    while(frequency>note_freq[i]):
        i=i+1
    Identified_Notes1.append(notes[i])
    mapNotes.append(rep[i])
    #mapp(i)
    #ser.write(b'k')
    #time.sleep(1)
    return 0

def findFrequency():
                                                                                                                    #this function removes the repetitive values corresponding to the same note
                                                                                                                    #and silences and gets the notes for the found frequencies 
    j=0              
    temp=1
    while(j<len(k)-4):
        if(k[j]==0):
            temp=1
        if((k[j]!=temp) & (k[j]!=0)):
            if(k[j]==k[j+1]):
                temp=k[j]
                findNote (temp)
        j=j+1
    return Identified_Notes1


def play(sound_file):                                                                                                 #sound_file-- test audio_file as input argument
    Identified_Notes1.clear()                                                                                         #clears the Identified_Notes1 list
    k.clear()                                                                                                         #clears the k list 
    file_length = sound_file.getnframes()                                                                             #finds the length of audio file
    for i in range(int(file_length/window_size)):
        data = sound_file.readframes(window_size)                                                                     #reads the data for window_size frames
        data = struct.unpack('{n}h'.format(n=window_size), data)                                                      #converts data to decimal format
        sound = np.array(data)
        w = np.fft.fft(sound)                                                                                         #finds fourier transform 
        freqs = np.fft.fftfreq(len(w))                                                                                #finds frequency with respect to data 
        idx = np.argmax(np.abs(w))                                                                                    #finds the max argument(frequency) index
        freq = freqs[idx]                                                                                             #retrieves the frequency
        k.append(abs(freq * sampling_freq))                                                                           #appends the frequency to k
    findFrequency()        #calls findFrequency function
    #ser.write(b'z')
    return Identified_Notes1

################################################################### Read Audio File #####################################################################

if __name__ == "__main__":                                                                                            #code for checking output for single audio file
    
    
    sound_file = wave.open('Audio.wav', 'r')
    Identified_Notes = play(sound_file)
    print ("Notes = ", Identified_Notes)
    ser.write(struct.pack("B",len(mapNotes)))
    time.sleep(1)
    #to send the notes serially
    for i in mapNotes:
        ser.write(struct.pack("B",i))
        time.sleep(0.1)
    #for multiple files
    '''
    for file_number in range(1,6):                                                                                     #code for checking output of all audio files 
        file_name = "Test_Audio_files/Audio_"+str(file_number)+".wav"
        print("\n"+file_name+":")                                                                                      #prints the name of the file being accessed
        sound_file = wave.open(file_name)
        Identified_Notes = play(sound_file)                                                                            #calls the play function
        print (Identified_Notes)                                                                                       #prints the notes of the accessed file
        Identified_Notes.clear()                                                                                       #clears the Identified_Notes list  
    '''        
################################################################### Send Serial data #####################################################################


