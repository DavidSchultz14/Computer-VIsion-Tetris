from operator import truediv
import cv2 as cv
import threading
import time
x, y = 0, 0
stop = False
squares = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
shapes = [[[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]]
starting_local = 5, 10
localx, localy = 5, 10
grid_size = 1
current_shape = shapes[0]
pause = True
bottom_x, bottom_y = 0, 0


def check_and_place():
    global pause
    global squares
    global starting_local
    pause = True
    global localx, localy
    bottom = 0
    if(current_shape[0] == [0, 0, 0, 0]):
        bottom = -1
        if(shapes[0] == [0, 0, 0, 0]):
            bottom = -2

    if(localy <= 11):
        for i in range(4):
            if(pause == False):
                break
            for j in range(4):
                if(current_shape[i][j] == 1 and i+localy-1 < len(squares[0]) and j+localx < len(squares) and 0 < j+localx < len(squares) and squares[i+localy-1][j+localx] or localy == bottom):
                    for k in range(4):
                        for z in range(4):
                            if(current_shape[k][z] == 1):
                                squares[k+localy][z+localx] = 1

                    localx, localy = starting_local
                    pause = False
                    break
        pause = False


def display_block(frame):
    frame1 = frame
    global current_shape
    global localx, localy
    global bottom_x, bottom_y
    global grid_size
    for i in range(4):
        for j in range(4):
            if(current_shape[i][j]):
                cv.rectangle(frame1, (bottom_x+(j+localx)*grid_size, bottom_y-(i+localy)*grid_size),
                             (bottom_x+(j+1+localx)*grid_size, bottom_y-(i+1+localy)*grid_size), (0, 255, 100), -1)
    return frame1


def display_squares(frame):
    frame1 = frame
    global squares
    global bottom_x, bottom_y
    width = frame.shape[1]
    height = frame.shape[0]
    bottom_x, bottom_y = width//3, height
    square_size = bottom_x//10
    global grid_size
    grid_size = square_size
    for i in range(len(squares)):
        for j in range(len(squares[i])):
            if(squares[i][j] == 1):
                cv.rectangle(frame1, (bottom_x + j*square_size, bottom_y-i*square_size),
                             (bottom_x + (j+1)*square_size, bottom_y-(i+1)*square_size), (0, 255, 0), -1)
    return frame1


def dropdown():
    global pause
    global localy
    if(pause == False):
        localy = localy - 1
        time.sleep(2)


def horiz():
    global grid_size
    global bottom_x
    global pause
    global localx
    global x
    x1 = x - bottom_x
    gridx = x1//grid_size
    print(gridx)
    print(x1)
    print(x)
    boundb = 0
    boundtop = 6
    # i know it is bad to hardcode numbers, but its tetris. blocks are always 4x4
    if(current_shape[0][0] == 0 and current_shape[1][0] == 0 and current_shape[2][0] == 0 and current_shape[3][0] == 0):
        boundb = boundb + 1
        if(current_shape[0][1] == 0 and current_shape[1][1] == 0 and current_shape[2][1] == 0 and current_shape[3][1] == 0):
            boundb = boundb + 1
    if(current_shape[0][3] == 0 and current_shape[1][3] == 0 and current_shape[2][3] == 0 and current_shape[3][3] == 0):
        boundtop = boundtop - 1
        if(current_shape[0][2] == 0 and current_shape[1][2] == 0 and current_shape[2][2] == 0 and current_shape[3][2] == 0):
            boundtop = boundtop - 1
    if(pause == False and gridx >= 0 and gridx <= boundtop):
        localx = gridx


def center(rect):  # updates main x value
    global x, y
    if(len(rect) > 0):
        x = rect[0][0]
        y = rect[0][1]
    print(x, y)


def run_cv():  # updates the main x value and then runs the game
    t2 = threading.Thread(target=run_print)
    t3 = threading.Thread(target=run_print2)
    global stop
    capture = cv.VideoCapture(0, cv.CAP_DSHOW)
    haar_cascade = cv.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')
    t2.start()
    t3.start()
    while True:
        isTrue, frame = capture.read()
        square_frame = display_squares(frame)
        square_frame2 = display_block(square_frame)
        cv.imshow('Video', square_frame2)
        grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        rects = haar_cascade.detectMultiScale(
            grey, scaleFactor=1.1, minNeighbors=1)
        check_and_place()
        center(rects)
        if cv.waitKey(25) & 0xFF == ord('q'):
            stop = True
            break
    t2.join()
    capture.release
    cv.destroyAllWindows()


def run_print():
    global stop
    while True:
        dropdown()
        horiz()
        if stop:
            break


def run_print2():
    global stop
    while True:
        horiz()
        if stop:
            break


run_cv()
print("Done")
