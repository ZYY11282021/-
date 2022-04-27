import fk_ar
import pygame, sys, random, time, numpy
from pygame.locals import *

fk_ar = fk_ar.fk_ar
BACK_array = numpy.full((25, 16), 0)
BACK_array[0:25, 0:3] = 1
BACK_array[0:25, 13:16] = 1
BACK_array[22:25, 0:16] = 1
SCREEN_array = numpy.full((6, 29), 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WALLCOLOR = (0,0,20)
YELLOW=(255,255,0)
FKCOLOR=[(0,0,0),(173,240,47),(15,240,140),(240,100,180),(140,20,230),(155,125,195),(100,135,220),(15,150,140)]
#定义每一种类方块的颜色##(1)###########(2)##########(3)###########(4)##########(5)###########(6)############(7)####

My_next_color_RED = 0
My_next_color_way_RED = 1
My_next_color_GREEN = 0
My_next_color_way_GREEN = 1
My_next_color_BLUE = 0
My_next_color_way_BLUE = 1

GAME_fk_count = GAME_level = GAME_score = GAME_speed = GAME_over = 0
Mymouse_x = Mymouse_y = 0

Key_h_time=0
Pressed_key = 0
Hold_t_crtl=0.2
GAME_paused=0

BOX_ADD_SUCCEED = 0
pygame.init()  # 初始化pygame模块
pygame.mixer.init()
pygame.mixer.music.load("wav/backmp3.mp3")
pygame.mixer.music.play(-1, 0)
sound_key = pygame.mixer.Sound("wav\key.wav")
sound_hu = pygame.mixer.Sound("wav\hu.wav")
sound_tang = pygame.mixer.Sound("wav\dang.wav")
sound_didi = pygame.mixer.Sound("wav\didi.wav")
sound_dianci = pygame.mixer.Sound("wav\dianci.wav")
sound_over = pygame.mixer.Sound("wav\over.wav")
music_on_off = 0
music_stop = 0
sound_on_off = 0
sound_stop = 0
clock = pygame.time.Clock()
infoObject = pygame.display.Info()  # 获取当前屏幕信息
Screen_w = infoObject.current_w  # 获取屏幕宽度w
Screen_h = infoObject.current_h  # 获取屏幕高度h
MYX = Screen_w / 100
MYY = Screen_h / 100
main_x = round(MYX * 32)
main_y = round(MYY * 6)

fk_bc = round(MYY * 4)
Screem_type = FULLSCREEN  # 设置全屏幕
DISPLAYSURF = pygame.display.set_mode((Screen_w, Screen_h), Screem_type,32)
pygame.mouse.set_visible(False)   #设置鼠标不可见


def time_wait(second):
    t1 = time.time()
    while True:
        t2 = time.time()
        if t2 - t1 > second:
            break
    return

def put_text(x, y, text, color, size, center_on_off):
    fontObj = pygame.font.SysFont("simhei", size)
    textSurfaceObj = fontObj.render(text, True, color)
    if center_on_off:
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (round(x), round(y))
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    else:
        DISPLAYSURF.blit(textSurfaceObj, (x, y))

def my_time_color_RED(start_color):
    global My_next_color_RED
    global My_next_color_way_RED
    if My_next_color_RED + start_color == 255:
        My_next_color_way_RED = -1
    if My_next_color_RED + start_color == 0:
        My_next_color_way_RED = 1
    My_next_color_RED = My_next_color_RED + My_next_color_way_RED
    return My_next_color_RED + start_color

def my_time_color_GREEN(start_color):
    global My_next_color_GREEN
    global My_next_color_way_GREEN
    if My_next_color_GREEN + start_color >= 254:
        My_next_color_way_GREEN = -2
    if My_next_color_GREEN + start_color <= 1:
        My_next_color_way_GREEN = 2
    My_next_color_GREEN = My_next_color_GREEN + My_next_color_way_GREEN
    return My_next_color_GREEN + start_color

def my_time_color_BLUE(start_color):
    global My_next_color_BLUE
    global My_next_color_way_BLUE
    if My_next_color_BLUE + start_color >= 253:
        My_next_color_way_BLUE = -3
    if My_next_color_BLUE + start_color <= 2:
        My_next_color_way_BLUE = 3
    My_next_color_BLUE = My_next_color_BLUE + My_next_color_way_BLUE
    return My_next_color_BLUE + start_color


def my_danmic_color(myrange):
    return (random.randint(60,myrange),random.randint(60,myrange),random.randint(60,myrange))

def my_line_box(x, y, w, h, dr, dg, db):
    pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, w, h), 1)
    pygame.draw.rect(DISPLAYSURF, (100,100,140), (x+1, y+1, w-1, h-1), 1)
    pygame.draw.rect(DISPLAYSURF, WHITE, (x + 10, y + 10, w - 20, h - 20), 1)
    pygame.draw.rect(DISPLAYSURF,BLACK, (x + 10, y + 10, w - 21, h - 21), 1)

"""
    r,g,b=1,2,3
    nextr,nextg,nextb = 0,0,0
    for i in range(round(h-22)):
        if nextr + dr >= 255:          r = -1
        if nextg + dg >= 254:          g = -2
        if nextb + db >= 253:          b = -3
        if nextr + dr <= 0:            r = 1
        if nextg + dg <= 1:            g = 2
        if nextb + db <= 2:            b = 3
        nextr = nextr + r
        nextg = nextg + g
        nextb = nextb + b
        pygame.draw.line(DISPLAYSURF, (nextr + dr, nextg + dg, nextb + db), (x + 11, y + 11+i), (x+w -12, y+11+i))

"""
def els_box(x, y, bianchang, mycolor , bgbox): #bgbox=1实心背景，0，空心边框，3是立体方块。
    d3d=10   #3d 深度
    c_c=35  #3d时候，方块立体部分颜色增减量
    c_c2=15
    x1 = round(x + 2)
    y1 = round(y + 2)
    bc = round(bianchang - 2)
    x2=x1+bc
    y2=y1+bc
    xx1 = x1 + d3d
    yy1 = y1 + d3d
    xx2 = x2 - d3d
    yy2 = y2 - d3d
    redadd = mycolor[0] + c_c
    if redadd>255:redadd=255
    greenadd = mycolor[1] + c_c
    if greenadd>255:greenadd=255
    blueadd = mycolor[2] + c_c
    if blueadd>255:blueadd=255
    redsub = mycolor[0] - c_c
    if redsub < 0: redsub = 0
    greensub = mycolor[1] - c_c
    if greensub < 0: greensub = 0
    bluesub = mycolor[2] - c_c
    if bluesub < 0: bluesub = 0
    redadd2 = mycolor[0] + c_c2
    if redadd2 > 255: redadd2 = 255
    greenadd2 = mycolor[1] + c_c2
    if greenadd2 > 255: greenadd2 = 255
    blueadd2 = mycolor[2] + c_c2
    if blueadd2 > 255: blueadd2 = 255
    redsub2 = mycolor[0] - c_c2
    if redsub2 < 0: redsub2 = 0
    greensub2 = mycolor[1] - c_c2
    if greensub2 < 0: greensub2 = 0
    bluesub2 = mycolor[2] - c_c2
    if bluesub2 < 0: bluesub2 = 0
    mycoloradd = (redadd, greenadd, blueadd)
    mycolorsub = (redsub, greensub, bluesub)
    mycoloradd2 = (redadd2, greenadd2, blueadd2)
    mycolorsub2 = (redsub2, greensub2, bluesub2)
    mylist=[(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
    flist1 = [(x1, y1), (x2, y1), (xx2, yy1), (xx1, yy1)]
    flist2 = [(xx2, yy1), (x2, y1), (x2, y2), (xx2, yy2)]
    flist3 = [(xx1, yy2), (xx2, yy2), (x2, y2), (x1, y2)]
    flist4 = [(x1, y1), (xx1, yy1), (xx1, yy2), (x1, y2)]
    if bgbox == 0:
        pass
    elif bgbox == 1:
        pygame.draw.polygon(DISPLAYSURF,WALLCOLOR,mylist,0)
    elif bgbox==3:
        pygame.draw.polygon(DISPLAYSURF, mycolor, mylist, 0)
        pygame.draw.polygon(DISPLAYSURF, mycoloradd, flist1, 0)
        pygame.draw.polygon(DISPLAYSURF, mycolorsub2, flist2, 0)
        pygame.draw.polygon(DISPLAYSURF, mycolorsub, flist3, 0)
        pygame.draw.polygon(DISPLAYSURF, mycoloradd2, flist4, 0)
    elif bgbox==2:
        pygame.draw.line(DISPLAYSURF, mycolor, (x1, y1), (x1 + bc, y1), 1)
        pygame.draw.line(DISPLAYSURF, mycolor, (x1, y1), (x1, y1 + bc), 1)
        pygame.draw.line(DISPLAYSURF, mycolor, (x1 + bc, y1), (x1 + bc, y1 + bc), 1)
        pygame.draw.line(DISPLAYSURF, mycolor, (x1, y1 + bc), (x1 + bc, y1 + bc), 1)
    elif bgbox==4:
        cc=random.randint(1,3)
        if cc==1:
            for i in range(1+int(bc/2)):
                pygame.draw.rect(DISPLAYSURF, (i*12,0,0),(x1+i,y1+i,bc-2*i,bc-2*i),1)
        if cc==2:
            for i in range(1+int(bc/2)):
                pygame.draw.rect(DISPLAYSURF, (0,i*12,0),(x1+i,y1+i,bc-2*i,bc-2*i),1)
        if cc==3:
            for i in range(1+int(bc/2)):
                pygame.draw.rect(DISPLAYSURF, (0,0,i*12),(x1+i,y1+i,bc-2*i,bc-2*i),1)

def music_control():
    global music_stop
    global music_on_off
    if music_on_off == 1:
        music_on_off = 0
        if music_stop == 0:
            music_stop = 1
            pygame.mixer.music.pause()
        elif music_stop == 1:
            music_stop = 0
            pygame.mixer.music.unpause()

def sound_control():
    global sound_stop
    global sound_on_off
    if sound_on_off == 1:
        sound_on_off = 0
        if sound_stop == 0:
            sound_stop = 1
        elif sound_stop == 1:
            sound_stop = 0

def keybroad_and_mouse():
    global key_hold_start_time
    global Key_h_time
    global Pressed_key
    global Mymouse_x, Mymouse_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
           key_hold_start_time=time.time()
           Pressed_key=event.key
        elif event.type == pygame.KEYUP:
            Pressed_key = 0
            Key_h_time = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            key_hold_start_time = time.time()
            Pressed_key=event.button
        elif event.type == pygame.MOUSEBUTTONUP:
            Pressed_key = 0
            Key_h_time = 0
        if event.type == pygame.MOUSEMOTION:
            Mymouse_x, Mymouse_y = pygame.mouse.get_pos()
    if Pressed_key:
        Key_h_time = time.time() - key_hold_start_time
    return (Pressed_key, Key_h_time, Mymouse_x, Mymouse_y)


def wait_enter_key_pressed():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in(pygame.K_RETURN,pygame.K_KP_ENTER,pygame.K_SPACE,pygame.K_DOWN):
                    return

def add_array(main_array, slave_array, x, y):
    global BOX_ADD_SUCCEED
    global GAME_over
    temp_array = main_array.copy()
    temp_back_array=temp_array[x:(x + 4), y:(y + 4)]
    for i in range(4):
        for j in range(4):
            if temp_back_array[i,j]>0 and slave_array[i,j]>0:
                BOX_ADD_SUCCEED = 0
                if x == 0 and y == 6:
                    GAME_over = 1
                return main_array
    temp_array[x:(x + 4), y:(y + 4)] = temp_array[x:(x + 4), (y):(y + 4)] + slave_array
    BOX_ADD_SUCCEED = 1
    return temp_array


def draw_array_wall(x, y, bianchang, mycolor, boxarray):
    row = len(boxarray)
    col = len(boxarray[0])
    for i in range(22):
        pygame.draw.rect(DISPLAYSURF,(0,0,200-i*9),(x-i,y-i,bianchang*(col-6)+3+2*i,bianchang*(row-3)+3+2*i),1)
    mx = x
    my = y
    for i in range(0, row - 3):  # hang
        for j in range(col):  # lie
            if i in range(0, row - 3) and j in range(3, 13):
                if boxarray[i][j] >0:
                    els_box(mx, my, bianchang, FKCOLOR[boxarray[i][j]],3)
                else:
                    els_box(mx, my, bianchang, mycolor,1)
                mx = mx + bianchang
        my = my + bianchang
        mx = x


def draw_array_wall_color(x, y, bianchang, mycolor, boxarray):
    row = len(boxarray)
    col = len(boxarray[0])
    for i in range(22):
        pygame.draw.rect(DISPLAYSURF,(200-i*9,0,0),(x-i,y-i,bianchang*(col-6)+3+2*i,bianchang*(row-3)+3+2*i),1)
    mx = x
    my = y
    for i in range(0, row - 3):  # hang
        for j in range(col):  # lie
            if i in range(0, row - 3) and j in range(3, 13):
                if boxarray[i][j] ==100:
                    els_box(mx, my, bianchang,mycolor,4)#将要消除的酷炫块
                    pygame.display.update((mx, my, bianchang,bianchang))
                    time_wait(0.006)
                elif boxarray[i][j] >0 :
                    els_box(mx, my, bianchang, RED,3)  #正常3D形状
                #else:
                 #   els_box(mx, my, bianchang, mycolor,0)  # 颜色参数输入BLACK，实际颜色为随机颜色
                mx = mx + bianchang
        my = my + bianchang
        mx = x

def draw_array_wall_welcome(x, y, mycolor, boxarray):
    global MYX
    row = len(boxarray)
    col = len(boxarray[0])
    bianchang = Screen_w / (col-3)
    mx = x
    my = y
    for i in range(row):  # hang
        for j in range(3,col):  # lie
            if boxarray[i][j] > 0:
                els_box(mx, my, bianchang, FKCOLOR[boxarray[i][j]],3)  # 颜色参数输入BLACK，实际颜色为随机颜色
            #else:
             #   els_box(mx, my, bianchang, mycolor,0)  # 颜色参数输入BLACK，实际颜色为随机颜色
            mx = mx + bianchang
        my = my + bianchang
        mx = x

def draw_array_wall_next(x, y, bianchang, mycolor, boxarray,mytext):
    row = len(boxarray)
    col = len(boxarray[0])
    mx = x
    my = y
    put_text(x+20,y-60, mytext, my_danmic_color(255), round(MYY * 4), 0)
    for i in range(row):  # hang
        for j in range(col):  # lie
            if boxarray[i][j] > 0:
                els_box(mx, my, bianchang, FKCOLOR[boxarray[i][j]],3)
            mx = mx + bianchang
        my = my + bianchang
        mx = x

def mark_can_disapper_line(main_array):
    row = len(main_array)
    for i in range(row - 3):
        can_dis = 0
        for j in range(3,13):
            if main_array[i, j]>0:
                can_dis=can_dis+1
        if can_dis==10:
            main_array[i, 3:13] = 100

def disapper_line(main_array):
    global GAME_score
    dis_area_row = len(main_array)
    once_disapper_lines = 0
    for i in range(dis_area_row - 3):
        if main_array[i, 3:13].sum() == 1000:
            if sound_stop == 0:
                sound_dianci.play()
            once_disapper_lines = once_disapper_lines + 1
            main_array[1:i + 1, 3:13] = main_array[0:i, 3:13]
            main_array[0, 3:13] = 0
    if once_disapper_lines == 1:
        GAME_score = GAME_score + 10
    elif once_disapper_lines == 2:
        GAME_score = GAME_score + 40
    elif once_disapper_lines == 3:
        GAME_score = GAME_score + 90
    elif once_disapper_lines == 4:
        GAME_score = GAME_score + 160


my_fk_list=[0, 0, 0, 0, 0, 0, 0]
def draw_count(x,y,nextfk):
    global my_fk_list
    my_fk_list[nextfk]=my_fk_list[nextfk]+1
    for i in range(7):
        draw_array_wall_next(x,y+(fk_bc*3)*i, fk_bc-10, RED, fk_ar[i,0],"")
        put_text(x+fk_bc*5,y+(fk_bc*3+6)*i+fk_bc,"第"+str(my_fk_list[i])+"个",my_danmic_color(255),38,1)



def wellcom_seceen():
    imgback_wallcome = pygame.image.load("img/winter.jpg")
    imgback_wallcome = pygame.transform.scale(imgback_wallcome, (Screen_w, Screen_h))
    global Pressed_key
    i = 0
    while True:
        keybroad_and_mouse()
        t_red = my_time_color_RED(0)
        t_green = my_time_color_GREEN(85)
        t_blue = my_time_color_BLUE(170)
        thistimecolor=(t_red,t_green,t_blue)
        DISPLAYSURF.blit(imgback_wallcome, (0,0))
        if i == 8:#每向右西东8个空格后，再加入一个新随机小方块
            i = 0
            fk_next = fk_ar[random.randint(0, len(fk_ar) - 1), random.randint(0, 3)]
            SCREEN_array[1:5, 0:4] = fk_next
        draw_array_wall_welcome(0, MYY * 33, thistimecolor, SCREEN_array)
        temparray = SCREEN_array.copy()
        SCREEN_array[0:6, 1:29] = temparray[0:6, 0:28]
        SCREEN_array[0:6, 0:1] = 0
        rdx = random.randint(-3, 3)
        rdy = random.randint(-3, 3)
        put_text(round(Screen_w / 2) + rdx+2, round(Screen_h / 5) + rdy+2, "欢乐俄罗斯方块",WHITE,round(MYY * 16), 1)
        put_text(round(Screen_w / 2) + rdx, round(Screen_h / 5) + rdy, "欢乐俄罗斯方块", (t_red, t_green, t_blue),
                 round(MYY * 16), 1)
        put_text(round(MYX * 50), round(MYY * 80), "Programed by msw Press ‘ESC’ to QUIT", thistimecolor, round(MYY * 3), 0)
        put_text(round(MYX * 50), round(MYY * 86), "Press ‘Enter’ to Start Game", thistimecolor, round(MYY * 3), 0)
        put_text(round(MYX * 50), round(MYY * 92), "By ZYY", thistimecolor, round(MYY * 3),
                 0)
        put_text(round(MYX * 10), round(MYY * 82), "按 M 开关背景音乐", thistimecolor, round(MYY * 3), 0)
        put_text(round(MYX * 10), round(MYY * 90), "按 S 开关游戏音效", thistimecolor, round(MYY * 3), 0)
        pygame.display.update()
        i = i + 1
        #music_control() #检测是否要开关背景音乐
        clock.tick(16)
        if Pressed_key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif Pressed_key in(pygame.K_RETURN,pygame.K_KP_ENTER,pygame.K_SPACE):
            Pressed_key=0
            break

"""
#####     程序开始执行部分    ###########
"""

while GAME_over == 0:
    GAME_fk_count = 0
    GAME_level = 0
    GAME_score = 0
    GAME_speed = 0
    GAME_over = 0
    Trun_around = 0
    Trun_left_and_right = 0
    Trun_down = 0
    Next_around = 1
    TIME_delay_control = 1.5
    FRONT_BOX = BACK_array.copy()
    TIME_delay = 0
    TIME1 = time.time()
    before_Trunround = random.randint(0, 3)
    my_fk_list = [0, 0, 0, 0, 0, 0, 0]
    fk_next_num = random.randint(0, len(fk_ar) - 1)
    draw_count(round(MYX*80), round(MYY*8), fk_next_num)
    fk_next = fk_ar[fk_next_num].copy()
    wellcom_seceen()
    imgback = pygame.image.load("img/Cloudscape.jpg")
    imgback = pygame.transform.scale(imgback, (Screen_w, Screen_h))
    DISPLAYSURF.blit(imgback, (0,0))
    draw_array_wall_color(main_x, main_y, fk_bc, WALLCOLOR, BACK_array)
    while True:
        if Next_around == 1:
            Next_around = 0
            GAME_fk_count = GAME_fk_count + 1
            Trun_around = before_Trunround
            before_Trunround = random.randint(0, 3)
            fk_now = fk_next.copy()
            fk_next_num=random.randint(0, len(fk_ar) - 1)
            fk_next = fk_ar[fk_next_num].copy()
            Trun_left_and_right = 6
            Trun_down = 0
            TIME_delay_control = 2 - (2 * GAME_score / 10000)
            if TIME_delay_control <= 0.1:TIME_delay_control = 0.1
            GAME_speed = round(GAME_score / 1000)
            DISPLAYSURF.blit(imgback, (0, 0))
            put_text(main_x + fk_bc * 11, round(MYY * 26), "成绩: " + str(GAME_score), my_danmic_color(255), round(MYY * 4), 0)
            put_text(main_x + fk_bc * 11, round(MYY * 34), "速度: " + str(GAME_speed), my_danmic_color(255), round(MYY * 4), 0)
            put_text(main_x + fk_bc * 11, round(MYY * 42), "计数: " + str(GAME_fk_count), my_danmic_color(255), round(MYY * 4), 0)
            put_text(main_x + fk_bc * 11, round(MYY * 50), "均分: " + str(round(GAME_score / GAME_fk_count, 2)), my_danmic_color(255), round(MYY * 4), 0)
            put_text(round(MYX * 4), round(MYY * 62), "按“ M ”开关背景音乐", my_danmic_color(255), round(MYY * 2), 0)
            put_text(round(MYX * 4), round(MYY * 68), "按“ S ”开关游戏音效", my_danmic_color(255), round(MYY * 2), 0)
            put_text(round(MYX * 4), round(MYY * 74), "按“空格” 暂停游戏", my_danmic_color(255), round(MYY * 2), 0)
            draw_count(round(MYX*80), round(MYY*8), fk_next_num)
            Pressed_key=0
            draw_array_wall_next(main_x + fk_bc * 11, round(MYY * 64),fk_bc, WALLCOLOR, fk_next[before_Trunround],"下一个")
            pygame.display.update()
        keybroad_and_mouse()
        if Pressed_key == pygame.K_SPACE and Key_h_time==0:  #按下空格键键，游戏暂停。
            if GAME_paused==0:
                GAME_paused =1
                put_text(main_x + 10, round(Screen_h / 2), "游戏暂停中……", RED, 60, 0)
            else:
                GAME_paused = 0
                Pressed_key = 0
        if GAME_paused == 0:
            if TIME_delay > TIME_delay_control:
                if sound_stop == 0 and Key_h_time<=0.3:
                    sound_key.play()
                TIME1 = time.time()
                Trun_down = Trun_down + 1
                TIME_delay = 0
            else:
                TIME2 = time.time()
                TIME_delay = TIME2 - TIME1
            if Pressed_key == pygame.K_UP:
                if Key_h_time==0:
                    if sound_stop == 0 and Key_h_time<=0.3:
                        sound_hu.play()
                    Trun_around = Trun_around + 1
                    if Trun_around == 4:
                        Trun_around = 0

            if Pressed_key == pygame.K_LEFT:
                if Key_h_time == 0 or Key_h_time >= Hold_t_crtl:
                    if sound_stop == 0 and Key_h_time<=0.2:
                        sound_key.play()
                    Trun_left_and_right = Trun_left_and_right - 1

            if Pressed_key == pygame.K_RIGHT:
                if Key_h_time == 0 or Key_h_time >= Hold_t_crtl:
                    if sound_stop == 0 and Key_h_time<=0.2:
                        sound_key.play()
                    Trun_left_and_right = Trun_left_and_right + 1

            if Pressed_key == pygame.K_DOWN:
                if TIME_delay !=0:
                    Trun_down = Trun_down + 1
                    TIME_delay = 0
                    TIME1 = time.time()

            tempFRONTBOX = add_array(FRONT_BOX, fk_now[Trun_around], Trun_down, Trun_left_and_right)
            if BOX_ADD_SUCCEED == 1:
                BACK_array = tempFRONTBOX.copy()  # 合并成功之后，记录一下合并情况
                draw_array_wall(main_x, main_y, fk_bc, WALLCOLOR, BACK_array)
            elif Pressed_key == pygame.K_LEFT:
                if sound_stop == 0 and Key_h_time<=0.1:
                    sound_didi.play()
                Trun_left_and_right = Trun_left_and_right + 1
                draw_array_wall_color(main_x, main_y, fk_bc, WALLCOLOR, BACK_array)

            elif Pressed_key == pygame.K_RIGHT:
                if sound_stop == 0 and Key_h_time<=0.1:
                    sound_didi.play()
                Trun_left_and_right = Trun_left_and_right - 1
                draw_array_wall_color(main_x, main_y, fk_bc, WALLCOLOR, BACK_array)

            elif Pressed_key == pygame.K_UP:
                if sound_stop == 0 and Key_h_time<=0.1:
                    sound_didi.play()
                Trun_around = Trun_around - 1
                #draw_array_wall_color(main_x, main_y, fk_bc, WALLCOLOR, BACK_array)
            else:  # 下一轮方块开始(自动到底，或者按键到底）
                if sound_stop == 0:
                    sound_hu.play()
                FRONT_BOX = BACK_array.copy()
                mark_can_disapper_line(FRONT_BOX)   #标记可以消除的行为100
                draw_array_wall_color(main_x, main_y, fk_bc, WALLCOLOR, FRONT_BOX)
                disapper_line(FRONT_BOX)            #对已经被标注为100的行进行数据消除。
                Next_around = 1
                Pressed_key = 0
                draw_array_wall(main_x, main_y, fk_bc, WALLCOLOR, BACK_array)
                if sound_stop == 0:
                    sound_tang.play()
                if GAME_over == 1:  # 下移一格不成功 并且my_add_array 返回游戏结束指令，游戏应该结束
                    if sound_stop == 0:
                        sound_over.play()
                    BACK_array[0:22, 3:13] = 0
                    GAME_over = 0
                    for i in range(10):
                        put_text(round(Screen_w / 2) + i, main_y + 460 + i, "GAME OVER", (90, 90, 90), 260, 1)
                    put_text(round(Screen_w / 2), main_y + 460, "GAME OVER", WHITE, 260, 1)
                    pygame.display.update()
                    wait_enter_key_pressed()
                    break

        if Pressed_key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        pygame.display.update()

        if Pressed_key == pygame.K_m:  #开关背景音乐
            music_on_off = 1
            Pressed_key = 0
        if Pressed_key == pygame.K_s:  #开关游戏音效
            sound_on_off = 1
            Pressed_key = 0
        music_control()  # 监测背景音乐是否要停
        sound_control()  # 监测音效是否要停
        clock.tick(60)
