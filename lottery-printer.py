import tkinter as tk
import tkinter.font as font
from sam4s.message import Message
from sam4s.text import TextLanguage, TextModification, TextFont, TextAlign
from sam4s.barcode import BarcodeType, BarcodeHri, BarcodeFont, Barcode
import serial
from datetime import datetime
import time



def initialize():
    global num_button_states

    num_button_states = [False] * 9
    for i in num_buttons:
        i.config(state=tk.NORMAL, relief=tk.RAISED)
    confirm_button.config(state=tk.DISABLED)

def confirm():
    global num_button_states

    now=datetime.now()
    time = str(now.hour)+":"+str(now.minute)

    if now.minute >= 50:
        target_hour = now.hour+1
        target_min = 0
        target_time = str(now.hour+1)+":00"
    else:
        target_hour = now.hour
        target_min = (now.hour//10+1)*10
        target_time = str(now.hour)+":"+str((now.hour//10+1)*10)
    

    numbers = []

    for (i, val) in enumerate(num_button_states):
        if val:
            numbers.append(i+1)

    message = Message()
    message.add_text_align(TextAlign.CENTER)
    message.add_text_size(3, 3)
    message.add_text_lang(TextLanguage.EN)
    message.add_text("Mechatronics\n")
    message.add_text_size(2, 2)
    message.add_text_lang(TextLanguage.KO)
    message.add_text("메카트로닉스\n")
    message.add_text_size(1, 1)
    message.add_feed_line(1)

    message.add_text_size(2, 2)
    message.add_text_lang(TextLanguage.EN)
    message.add_text("Lottery v2.0\n")
    message.add_text_size(1, 1)
    message.add_feed_line(1)

    barcode = Barcode(str(bytes(bytearray([target_hour+33, target_min+33, numbers[0]+33, numbers[1]+33, numbers[2]+33])), 'ascii'), BarcodeType.CODE93, BarcodeHri.NONE, BarcodeFont.A, 3, 162)
    message.add_barcode(barcode)
    message.add_feed_line(1)
    
    message.add_text_lang(TextLanguage.KO)
    message.add_text_align(TextAlign.CENTER)
    message.add_text("선택한 번호:"+ " " + str(numbers[0]) + " " + str(numbers[1]) + " " + str(numbers[2]) + "\n")
    message.add_text("추첨 시각:" + " " + target_time + "\n")
    message.add_feed_line(2)

    message.add_text_align(TextAlign.CENTER)
    message.add_text_lang(TextLanguage.EN)
    message.add_text_size(1,3)
    message.add_text("2023/10/21" + " " + time)
    message.add_feed_line(4)
    message.add_cut(True)
    output = message.generate_message()

    s.write(output)
    s.flush()
    initialize()

window = tk.Tk()
btn_font = font.Font(size=60, weight='bold')

initialize_buttons = []
initialize_button = tk.Button(window, text="초기화", command=initialize)
initialize_button['font'] = btn_font
initialize_button.place(relx=0, rely=0.8, relwidth=2/3, relheight=0.2)

confirm_buttons = []
confirm_button = tk.Button(window, text="확인", command=confirm)
confirm_button['font'] = btn_font
confirm_button.place(relx=2/3, rely=0.8, relwidth=1/3, relheight=0.2)
confirm_button.config(state=tk.DISABLED)

def num_button_click(num_button_index):
    global num_button_states
    
    if num_button_states[num_button_index]:  
        num_button_states[num_button_index] = False
        num_buttons[num_button_index].config(relief=tk.RAISED)  
    else:  
        num_button_states[num_button_index] = True
        num_buttons[num_button_index].config(relief=tk.SUNKEN)

    if num_button_states.count(True) >= 3:
        for (i, num_button) in enumerate(num_buttons):
            if not num_button_states[i]:
                num_button.config(state=tk.DISABLED)
        confirm_button.config(state=tk.NORMAL)
    else:
        for num_button in num_buttons:
            num_button.config(state=tk.NORMAL)
        confirm_button.config(state=tk.DISABLED)

"""
s = serial.Serial(
    port="COM3",
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    xonxoff=True,
    rtscts=False,
    dsrdtr=False,
)
"""

def create_barcode_data(hour, minute, number1, number2, number3):
    x = [hour, minute, num_button[0], num_button[1], num_button[2]]
    b = bytes(x)
    data = str(b, 'ascii')
    return data

def print_barcode(barcode_data, barcode_type):
    barcode = Barcode(barcode_data, BarcodeType.CODE93, BarcodeHri.NONE, BarcodeFont.A, 3, 162)
    message = barcode.to_message()
    output = message.generate_message()

num_button_states = [False] * 9

num_buttons = []
for i in range(1, 10):
    num_button = tk.Button(window, text=str(i), command=lambda index=i-1: num_button_click(index))
    num_button["font"] = btn_font
    num_button.place(relx=(i-1)%3/3, rely=(i-1)//3*0.8/3, relwidth=1/3, relheight=0.8/3)
    num_buttons.append(num_button)

window.columnconfigure(1, weight=1)
window.rowconfigure(1, weight=1)

window.mainloop()

