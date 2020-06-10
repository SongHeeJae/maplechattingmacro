from tkinter import *
from time import sleep
import pyautogui as pag
from threading import Thread
import winsound
import pyperclip

stopped = False

def add_item(items, window) :
    item = Entry(window, width=60)
    items.append(item)
    item.pack()
    
def alarm() :
    for i in range(5) :
        winsound.Beep(493, 250)

def run(items) :
    global stopped
    sleep(3)
    i = 0
    while True :
        if(items[i].get().strip() == '') :
            i = (i+1)%len(items)
            continue

        pag.press('enter')
        sleep(0.1)
        pyperclip.copy(items[i].get())
        pag.keyDown('ctrl')
        pag.press('v')
        pag.keyUp('ctrl')
        sleep(0.1)
        pag.press('enter')
        sleep(0.1)
        pag.press('esc')
        sleep(0.1)
        
        btn = pag.locateCenterOnScreen('./btn.PNG', confidence=0.8)
        print(btn)
        if (btn != None) :
            pag.click(btn)
            alarm()
            break
        
        if(stopped == True) :
            break
        i = (i+1)%len(items)
        sleep(0.8)
    stopped = False
    for item in items :
        item['state'] = 'normal'


def start(items) :
    global stopped
    if stopped == True :
        return
    stopped = False
    for item in items :
        item['state'] = 'disabled'
    task = Thread(target=run, args=(items,))
    task.start()

def stop(items) :
    global stopped
    stopped = True


if __name__ == '__main__' :
    
    window = Tk()
    window.title('chatting macro')

    items = []
    for i in range(4) :
        add_item(items, window)

    Button(window, text="시작", command=lambda items=items: start(items)).pack()
    Button(window, text="종료", command=lambda stopped=stopped, items=items: stop(items)).pack()
    window.mainloop()