import tkinter as tk
import math


WIDTH = 264
HEIGHT = 349
simbol = [['1', '2', '3', '='],
          ['4', '5', '6', '+'],
          ['7', '8', '9', '-'],
          ['C', '0', '<<', 'sqrt'],
          [':', ',', '*', '^']]
boris = [] # list buttons
oni = [] # list arithmetic expression
mark = False
oper = ['^', '*', ':', '+', '-']


def click(event, s):
    global mark
    
    la = label['text']

    if la == 'На ноль делить нельзя':
        clear()
        la = ''
        oni.clear()
    
    if s == 'C':
        clear()
        oni.clear()
        mark = False

    elif s == 'sqrt':
        if la:
            la = str(round(math.sqrt(float(la.replace(' ', '').replace(',', '.'))), 5))
            if la[-1] == '0' and la[-2] == '.':
                la = la[0:-2]
            label['text'] = la.replace('.', ',')
            mark = True

    elif check(s):
        if la:
            if la[-1] == ',':
                la += '0'
            oni.append(la)
            oni.append(s)
            mark = True

    elif s == '=':
        if oni:
            decision(la)

    elif s == '<<':
        if la != '' and len(la) != 1:
            if label['text'][-1] == ' ':
                label['text'] = la[0:-2]
            else:
                label['text'] = la[0:-1]
        else:
            clear()
        if mark:
            mark = False

    elif s == ',':
        if mark:
            label['text'] = '0,'
            mark = False
            return
        if la and la.find(s) == -1:
            label['text'] += s

    elif len(la) < 19:
        if not ',' in la:
            if len(la) in [3, 7, 11, 15]:
                label['text'] += ' '
        if mark:
            label['text'] = s
            mark = False
            return
        if la == '0':
            return
        label['text'] += s


def decision(s):
    global mark, oni
    
    if s:
        oni.append(s)
    else:
        if oni:
            oni.pop()

    sp = []
    for u in range(len(oni)):
        sp.append(str(oni[u]).replace(' ', '').replace(',', '.'))
    else:
        oni = sp

    clear()

    label['text'] = calculation()
    mark = True
    oni.clear()


def clear():
    label['text'] = ''


def check(s):
    return s in oper


def calculation():
    global oni

    k = 0
    while len(oni) != 1:
        if oni.count(oper[k]) != 0:
            for o in range(oni.count(oper[k])):
                for idx, val in enumerate(oni):
                    if val == oper[k]:
                        if val == '^':
                            oni.insert(idx - 1, round(math.pow(float(oni[idx - 1]), float(oni[idx + 1])), 5))
                        elif val == '*':
                            oni.insert(idx - 1, round(float(oni[idx - 1]) * float(oni[idx + 1]), 5))
                        elif val == ':':
                            try:
                                oni.insert(idx - 1, round(float(oni[idx - 1]) / float(oni[idx + 1]), 5))
                            except ZeroDivisionError:
                                return 'На ноль делить нельзя'
                        elif val == '+':
                            oni.insert(idx - 1, round(float(oni[idx - 1]) + float(oni[idx + 1]), 5))
                        else:
                            oni.insert(idx - 1, round(float(oni[idx - 1]) - float(oni[idx + 1]), 5))

                        for k in range(3):
                            oni.pop(idx)

                        break
            k += 1
        else:
            k += 1

    oni[0] = str(oni[0]).replace('.', ',')

    if oni[0][-1] == '0' and oni[0][-2] == ',':
        return oni[0][0:-2]
    else:
        return oni[0]


window = tk.Tk()
window.geometry(f'{WIDTH}x{HEIGHT}')
window.resizable(width=False, height=False)
window.title('Калькулятор')

frame1 = tk.Frame(master=window, height=30)
frame1.pack()
label = tk.Label(master=frame1, text='',
                 bg='darkgrey', fg='black', width=WIDTH, height=4,
                 font=("Arial Bold", 18))
label.pack()

frame2 = tk.Frame(master=window, height=HEIGHT - 50)
frame2.pack()

for i in range(5):
    for j in range(4):
        si = simbol[i][j]
        boris.append(tk.Button(master=frame2, text=si, width=4,
                               height=1, bg='grey', fg='white',
                               font=("Arial Bold", 18), relief=[tk.FLAT]))
        boris[-1].bind('<Button-1>', lambda e, s=si: click(e, s))
        boris[-1].bind('<Enter>', lambda e, x=boris[-1]: x.config(bg='#C1C1C1'))
        boris[-1].bind('<Leave>', lambda e, x=boris[-1]: x.config(bg='grey'))
        boris[-1].grid(row=i, column=j)


if __name__ == '__main__':
    window.mainloop()
