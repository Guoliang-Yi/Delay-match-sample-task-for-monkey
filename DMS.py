
import pygame
import time
import random
import serial
from psychopy import gui
import sys

Monkey_infomation = {'Monkey_number':'','Experimenter':'','Total_trials':'','Time':'','Sequence':''}
inputDlg  = gui.DlgFromDict(dictionary=Monkey_infomation,title='delay match task',order=['Monkey_number','Experimenter','Total_trials','Time','Sequence'])
serialPort = 'COM4'
baudRate = 115200
ser = serial.Serial(serialPort, baudRate, timeout=0.01)
pygame.init()
window = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
def run_trials():
    sample_rect = pygame.Rect(random.uniform(200,1720),random.uniform(540,880),200,200)
    target_group = ([pygame.Rect(860, 510, 200, 200),pygame.Rect(860, 880, 200, 200)],
                    [pygame.Rect(660, 710, 200, 200),pygame.Rect(1060, 710, 200, 200)],
                    [pygame.Rect(860, 880, 200, 200),pygame.Rect(860, 510, 200, 200)],
                    [pygame.Rect(1060, 710, 200, 200),pygame.Rect(660, 710, 200, 200)])
    
    target_rect = random.choice(target_group)

    target1_position = [target_rect[0].centerx,target_rect[0].centery]
    target2_position = [target_rect[1].centerx,target_rect[1].centery]
    sample_position = [sample_rect.centerx,sample_rect.centery]

    Sample_label = random.choice([1,2,3,4,5,7,8,9,10,11,12,13,14])
    test1_label = random.choice([1,2,3,4,5,7,8,9,10,11,12,13,14])
    test2_label = random.choice([1,2,3,4,5,7,8,9,10,11,12,13,14])
    sample_change = random.choice((1,-1))
    rotation = random.uniform(-90,90)
    scalezoom = random.uniform(0.5,1)
    # print(Sample_label)
    test_response = 0
    if sample_change ==1:
        T0 = time.time()
        while time.time()-T0<2:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            sample = pygame.image.load('S{}.png'.format(Sample_label))   
            window.fill((0,0,0))
            sample_1 = pygame.transform.rotozoom(sample,rotation,scalezoom)
            window.blit(sample_1,sample_rect)
            pygame.display.flip()

        T1  =time.time()
        while time.time()-T1<2:
            for event in pygame.event.get():
              if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            window.fill((0,0,0))
            pygame.display.flip()
        window.fill((0,0,0))
        test1 = pygame.image.load('S{}.png'.format(test1_label))
        test2 = pygame.image.load('Y{}.png'.format(test2_label))
        window.blit(test1,target_rect[0])
        window.blit(test2,target_rect[1])
        pygame.display.flip()
        # fingers = {}
        T2 = time.time()
        while time.time()-T2<5:
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
            for i, rect in enumerate(target_rect): 
                touched = False
                for finger, pos in fingers.items():       
                    if rect.collidepoint(pos):
                        touched = True
                highlight.append(touched)

            if highlight[0]:
                test_response = 1
                ser.write('d0250d'.encode())  # Reward signal
                window.fill((0,0,0))
                test1 = pygame.image.load('S6.png')
                test2 = pygame.image.load('Y{}.png'.format(test2_label))
                window.blit(test1,target_rect[0])
                window.blit(test2,target_rect[1])
                pygame.display.flip()
                time.sleep(0.3)
                break
            elif highlight[1]:
                test_response = -1
                window.fill((255,255,255))
                pygame.display.flip()
                time.sleep(2)
                break
    else:
        T0 = time.time()
        while time.time()-T0<2:
            for event in pygame.event.get():
              if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            window.fill((0,0,0))
            sample = pygame.image.load('Y{}.png'.format(Sample_label))
            sample_1 = pygame.transform.rotozoom(sample,rotation,scalezoom)
            window.blit(sample_1,sample_rect)
            pygame.display.flip()    
        T1  =time.time()
        while time.time()-T1<2:
            for event in pygame.event.get():
              if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            window.fill((0,0,0))
            pygame.display.flip()
        window.fill((0,0,0))
        test1 = pygame.image.load('Y{}.png'.format(test1_label))
        test1_1 = pygame.transform.rotozoom(test1,rotation,scalezoom)
        test2 = pygame.image.load('S{}.png'.format(test2_label))
        test2_1 = pygame.transform.rotozoom(test2,rotation,scalezoom)
        window.blit(test1_1,target_rect[0])
        window.blit(test2_1,target_rect[1])
        pygame.display.flip()
        # fingers = {}
        T2 = time.time()
        while time.time()-T2<5:
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
            for i, rect in enumerate(target_rect): 
                touched = False
                for finger, pos in fingers.items():       
                    if rect.collidepoint(pos):
                        touched = True
                highlight.append(touched)

            if highlight[0]:
                test_response = 1
                ser.write('d0250d'.encode())  # Reward signal
                window.fill((0,0,0))
                test1 = pygame.image.load('Y6.png')
                test1_1 = pygame.transform.rotozoom(test1,rotation,scalezoom)
                test2 = pygame.image.load('S{}.png'.format(test2_label))
                test2_1 = pygame.transform.rotozoom(test2,rotation,scalezoom)
                window.blit(test1_1,target_rect[0])
                window.blit(test2_1,target_rect[1])
                pygame.display.flip()
                time.sleep(0.3)
                break
            elif highlight[1]:
                test_response = -1
                window.fill((255,255,255))
                pygame.display.flip()
                time.sleep(2)
    #             break
    window.fill((0,0,0))
    pygame.display.flip()
    time.sleep(1)
    pygame.event.clear()
    return(sample_change,test_response)

Total_trial = int(Monkey_infomation['Total_trials'])
Y_Correct_number = 0
Y_Error_number = 0
Y_abandon_number = 0
S_Correct_number= 0
S_Error_number = 0
S_abandon_number = 0

for i in range(Total_trial):
    f = open('Delay_match_sample_{}_VM{}_2023{}_{}.txt'.format(Monkey_infomation['Experimenter'],Monkey_infomation['Monkey_number'],Monkey_infomation['Time'],Monkey_infomation['Sequence']),'a')
    a = run_trials()
    if a[0] == 1:
        if a[1]==1:
            S_Correct_number = S_Correct_number+1
        elif a[1]==-1:
            S_Error_number = S_Error_number+1
        else:
            S_abandon_number = S_abandon_number+1
    elif a[0]==-1:
        if a[1]==1:
            Y_Correct_number = Y_Correct_number+1
        elif a[1]==-1:
            Y_Error_number = Y_Error_number+1
        else:
            Y_abandon_number = Y_abandon_number+1 
    Performance_total = (S_Correct_number,S_Error_number,S_abandon_number,Y_Correct_number,Y_Error_number,Y_abandon_number)
    f.write('Trial')
    f.write(str(i))
    f.write(',')
    f.write(str(a))
    f.write(str(Performance_total))
    f.write("\n")
    # print('Total trial'+':'+ str(i)+','+'S_Correct'+':'+str(Performance_total)+','+'Y_Correct'+':'+str(Y_Correct_number)) #trial数从0开始

    print('Total trial'+':'+ str(i)+','+str(Performance_total))
    

