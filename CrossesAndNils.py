from array import *
import time
import threading
from threading import Thread
from threading import Lock

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")

N = 3

lock = Lock()

COUNT = 0
CROSS_WIN = 0
NILLS_WIN = 0

f = None

def evaluate(board):
    # columns
    for j in range(0, N):
        sum1 = 0
        for i in range(0, N):
            sum1 += board[i][j]
        if (sum1 == +N):
            return +1
        if (sum1 == -N):
            return -1
    # rows
    for i in range(0, N):
        sum2 = 0
        for j in range(0, N):
            sum2 += board[i][j]
        if (sum2 == +N):
            return +1
        if (sum2 == -N):
            return -1
    # diags
    sum = 0
    for i in range(0, N):
        sum += board[i][i]
    if (sum == +N):
        return +1
    if (sum == -N):
        return -1
    #
    sum = 0
    for i in range(0, N):
        sum += board[i][N - i - 1]
    if (sum == +N):
        return +1
    if (sum == -N):
        return -1
    return 0
    
def get_string(board):
    ss = "";
    for i in range(0, N):
        ss = ss + "["
        for j in range(0, N):
            if board[i][j] == +1: 
                ss += "x" 
            elif board[i][j] == -1:
                ss += "o"
            else:
                ss += "_"
        ss =ss + "]";
    return ss;

def who_move(board):
    sum0 = 0
    sum1 = 0
    sum2 = 0
    for i in range(0, N):
        for j in range(0, N):
            v = board[i][j]
            if (v == 0):
                sum0 += 1;
            elif (v == 1):
                sum1 += 1
            elif (v == -1):
                sum2 += 1
            else:
                pass

    if (sum0 == 0):
        return 0
    if (sum1 <= sum2):
        return 1
    else:
        return -1

def move(board, idx, dir):
    s = get_string(board)
    who_win = evaluate(board)
    if (who_win == +1):
        s.replace('x','X')
    if (who_win == -1):
        s.replace('o','O')
    dir += s

    global lock

    global f
    lock.acquire()
    f.write(dir)
    f.write("\n")
    lock.release()

    global COUNT
    global CROSS_WIN
    global NILLS_WIN
        
    lock.acquire()
    COUNT += 1
    lock.release()

    if COUNT % 100000 == 0: 
        print(COUNT)
        #print('.',end=" ")

    if who_win == +1: 
        lock.acquire()
        CROSS_WIN += 1 
        lock.release()
        return 1
    elif who_win == -1: 
        lock.acquire()
        NILLS_WIN += 1
        lock.release()
        return -1
    else:
        pass

    who = who_move(board);
    moved = 0;
    for i in range(0, N):
        for j in range(0, N):
            if (board[i][j] == 0):
                board[i][j] = who
                moved = 1
                idx = 0
                move(board, idx, dir)
                board[i][j] = 0 # restore the board
    return moved

def run():
    print()
    print("This is single thread implementation")

    global COUNT 
    COUNT = 0
    
    global CROSS_WIN 
    CROSS_WIN = 0

    global NILLS_WIN 
    NILLS_WIN = 0

    board = [[0,0,0], [0,0,0], [0,0,0]];

    move(board, 0, "")

    print()
    print("COUNT     " + str(COUNT))
    print("CROSS_WIN " + str(CROSS_WIN))
    print("NILLS_WIN " + str(NILLS_WIN))

def run_mt():
    print()
    print("This is multithreading implementation")

    global COUNT 
    COUNT = 1
    
    global CROSS_WIN 
    CROSS_WIN = 0

    global NILLS_WIN 
    NILLS_WIN = 0

    threads = []
    for i in range(0, N):
        for j in range(0, N):
            board = [[0,0,0], [0,0,0], [0,0,0]];
            board[i][j] = 1
            idx = 10*i + j
            t = Thread(target=move, args=(board, idx, ""))
            t.start() 
            threads.append(t)

    for t in threads:
        t.join()

    print()
    print("COUNT     " + str(COUNT))
    print("CROSS_WIN " +str(CROSS_WIN))
    print("NILLS_WIN " +str(NILLS_WIN))


print("This is full enumeration  of " + str(N) + "x"+ str(N) + " Crosses and Nills game")

t = Timer()

################################################################################################

t.start()

f = open("CrossesAndNils_py.txt", "w")

run()

f.close()

t.stop()  

################################################################################################

t.start()

f = open("CrossesAndNils_py_mt.txt", "w")

run_mt()

f.close()

t.stop()
