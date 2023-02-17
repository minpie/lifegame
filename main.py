import turtle
import sys
import time



# define data:
SIZE_AREA_WIDTH = 9 # 영역 너비(셀)
SIZE_AREA_HEIGHT = 9 # 영역 높이(셀)

SIZE_PER_CELL_WIDTH = 70 # 한 셀당 너비
SIZE_PER_CELL_HEIGHT = 70 # 한 셀당 높이

SIZE_SCREEN_WIDTH = SIZE_AREA_WIDTH * SIZE_PER_CELL_WIDTH # 총 화면크기(셀 가로 개수 * 셀당 너비)
SIZE_SCREEN_HEIGHT = SIZE_AREA_HEIGHT * SIZE_PER_CELL_HEIGHT # 총 화면크기(셀 세로 개수 * 셀당 높이)

CELL_COLORS = ["white", "yellow"]

IS_EDIT_LOCKED = False # 초기 지정이 끝났는지 여부 0: 초기상태 1: 초기지정 완료


# define function:
def drawOneCell():
    # 한 셀 그리기:
    for i in range(4):
        turt.forward(SIZE_PER_CELL_WIDTH)
        turt.right(90)
        pass
    pass

def endInitialTime():
    # 초기 지정 완료 처리용
    global IS_EDIT_LOCKED
    IS_EDIT_LOCKED = True
    pass

def endProgram():
    # 프로그램 종료용
    sys.exit()

def calcOneCell(index):
    # True: 다음 세대에 생존
    # False: 다음 세대에 죽어있음
    nears = list()
    nears_tmp = [
    index+1,
    index-1,
    index+SIZE_AREA_WIDTH,
    index+SIZE_AREA_WIDTH+1,
    index+SIZE_AREA_WIDTH-1,
    index-SIZE_AREA_WIDTH,
    index-SIZE_AREA_WIDTH-1,
    index-SIZE_AREA_WIDTH+1]
    for i in nears_tmp:
        nears.append(i)
    check = 0
    for i in nears:
        try:
            check += int(cells[i])
        except IndexError:
            continue
    if cells[index] == "0":
        if check == 3:
            return True
    else:
        #print(check)
        if (check == 2) or (check == 3):
            return True
    return False


def editInitialCell(mouse_x, mouse_y):
    # 초기 셀 생성/삭제 함수:
    if IS_EDIT_LOCKED:
        return # 초기지정 완료시 수행 불가처리
    # 초기상태 라면:


    pos_x = int(((SIZE_SCREEN_WIDTH / 2) + mouse_x) / SIZE_PER_CELL_WIDTH) # 가로로 x번지
    pos_y = int(((SIZE_SCREEN_HEIGHT / 2) - mouse_y) / SIZE_PER_CELL_HEIGHT) # 세로로 y번지
    #print(pos_x, pos_y)
    pos = (pos_y * (SIZE_AREA_WIDTH)) + pos_x # 1차원배열로써 위치
    #print(pos)
    cells[pos] = str(int(not (bool(int(cells[pos])))))

    # 그리기:
    turt.penup()
    current_color = CELL_COLORS[int(cells[pos])]
    turt.fillcolor(current_color)
    turt.begin_fill()
    turt.goto(
        (pos_x * SIZE_PER_CELL_WIDTH) - (SIZE_SCREEN_WIDTH / 2),   
        (SIZE_SCREEN_HEIGHT / 2) - (pos_y * SIZE_PER_CELL_HEIGHT)
        )
    turt.pendown()
    drawOneCell()
    turt.end_fill()
    

    #print(cells[pos])
    pass






# initial job:
turt = turtle.Turtle() # turtle 객체
turtle.setup(width=SIZE_SCREEN_WIDTH, height=SIZE_SCREEN_HEIGHT) # 화면 크기 설정
turt.speed(0)
turt.pencolor("white")


cells = "" # 셀들
cells = "0" * SIZE_AREA_HEIGHT * SIZE_AREA_WIDTH # 전체 셀 개수만큼 "0"으로 초기화
cells = list(cells)



# user input:
turtle.onscreenclick(editInitialCell)
turtle.onkey(endInitialTime, "s")
turtle.onkey(endProgram, "q")
turtle.listen()





# main loop:



def looping():
    global cells
    if IS_EDIT_LOCKED:
        # loop:
        #print(cells)
        next_cells = list("0" * len(cells))
        for i in range(0, SIZE_AREA_HEIGHT * SIZE_AREA_HEIGHT):
            if calcOneCell(i):
                next_cells[i] = "1"
                current_color = CELL_COLORS[1]
            else:
                next_cells[i] = "0"
                current_color = CELL_COLORS[0]
            

            if((cells[i]) == (next_cells[i])):
                continue
            
            pos_x = i % SIZE_AREA_WIDTH
            pos_y = int(i / SIZE_AREA_WIDTH)
            
            # 그리기:
            turt.fillcolor(current_color)
            turt.begin_fill()
            turt.goto(
                    (pos_x * SIZE_PER_CELL_WIDTH) - (SIZE_SCREEN_WIDTH / 2),   
                    (SIZE_SCREEN_HEIGHT / 2) - (pos_y * SIZE_PER_CELL_HEIGHT)
                    )
            turt.pendown()
            drawOneCell()
            turt.end_fill()
            turt.penup()
        cells = next_cells
        
    turtle.ontimer(looping, 400)
turt.penup()
looping()
turtle.mainloop()
print("End!")
# end main loop



turtle.exitonclick() # 자동으로 창 닫히지 않도록