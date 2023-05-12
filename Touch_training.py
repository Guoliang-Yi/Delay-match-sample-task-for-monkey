
import pygame
import time
import random
import serial
from psychopy import gui

Monkey_infomation = {'Monkey_number':'','Experimenter':'','Total_trials':'','Time':'','Sequence':''}
inputDlg  = gui.DlgFromDict(dictionary=Monkey_infomation,title='delay match task',order=['Monkey_number','Experimenter','Total_trials','Time','Sequence'])
serialPort = 'COM4'
baudRate = 115200
ser = serial.Serial(serialPort, baudRate, timeout=0.01)
pygame.init()
window = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN)
clock = pygame.time.Clock()

def run_trials():
    targets = [pygame.Rect(860, 440, 200, 200)]
    pygame.draw.rect(window,(255,0,0),(860,440,200,200)) 
    pygame.display.flip()
    test_response = 0
    T0 = time.time()
    while time.time()-T0<5:
        fingers = {}
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.FINGERDOWN:
                x = event.x * 1920
                y = event.y * 1080
                fingers[event.finger_id] = x, y
            if event.type == pygame.FINGERUP:
                fingers.pop(event.finger_id, None)
        highlight = []  
        for i, rect in enumerate(targets): 
            touched = False
            for finger, pos in fingers.items():       
                if rect.collidepoint(pos):
                    touched = True
            highlight.append(touched)

        if highlight[0]:
            test_response = 1
            ser.write('d0250d'.encode())  # Reward signal
            pygame.draw.rect(window,(0,255,0),(860,440,200,200))
            pygame.display.flip()
            time.sleep(0.3)
            break
    window.fill((0,0,0))
    pygame.display.flip()
    time.sleep(1)
    return (test_response)

Total_trial = int(Monkey_infomation['Total_trials'])
Correct_number = 0
abandon_number = 0
for i in range(Total_trial):
    f = open('Touch_training_{}_VM{}_2023{}_{}.txt'.format(Monkey_infomation['Experimenter'],Monkey_infomation['Monkey_number'],Monkey_infomation['Time'],Monkey_infomation['Sequence']),'a')
    a = run_trials()
    if a == 1:
        Correct_number = Correct_number+1
    else:
        abandon_number = abandon_number+1
    Performance_total = (Correct_number,abandon_number)
    f.write('Trial')
    f.write(str(i))
    f.write(',')
    f.write(str(a))
    f.write(str(Performance_total))
    f.write("\n")
    print('Total trial'+':'+ str(i)+','+'Correct'+':'+str(Correct_number)) 


