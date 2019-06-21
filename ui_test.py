from tkinter import *
from tkinter import ttk


def click_button():
    print('clicked')
    print('group', group_txt_msg.get())
    print('age', age_txt_msg.get())
    print('tol', tol_txt_msg.get())
    print('country', country_txt_msg.get())
    print('city', city_txt_msg.get())
    print('m', sex_m_val.get())
    print('w', sex_w_val.get())
    # print('pol', pol_spin.get())
    # print('life_m', life_spin.get())
    # print('people_m', ppl_spin.get())
    # print('smoking', sm_spin.get())
    # print('alcohol', al_spin.get())


window = Tk()
window.title("VK Match")
window.geometry('300x215')
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Первая')
tab_control.add(tab2, text='Вторая')
tab_control.pack(expand=1, fill='both')

group_lbl = Label(tab1, text="Group id:", font=("Open sans", 15))
group_lbl.grid(column=0, row=0, columnspan=2)

group_txt_msg = StringVar()
group_txt = Entry(tab1, textvariable=group_txt_msg, width=22, font=("Open sans", 12))
group_txt.grid(column=2, row=0, columnspan=2)
group_txt.focus()

sex_lbl = Label(tab1, text="Sex:", font=("Open sans", 15))
sex_lbl.grid(column=0, row=1, columnspan=2)

sex_m_val = IntVar()
sex_m_chk = Checkbutton(tab1, variable=sex_m_val, text='Man', font=("Open sans", 12))  # , var=chk_state
sex_m_chk.grid(column=2, row=1)

sex_w_val = IntVar()
sex_w_chk = Checkbutton(tab1, variable=sex_w_val, text='Woman', font=("Open sans", 12))  # , var=chk_state
sex_w_chk.grid(column=3, row=1)

age_lbl = Label(tab1, text="Age:", font=("Open sans", 15))
age_lbl.grid(column=0, row=2)

age_txt_msg = StringVar()
age_txt = Entry(tab1, textvariable=age_txt_msg, width=3, font=("Open sans", 12))
age_txt.grid(column=1, row=2)
age_txt.insert(0, '0')

tol_lbl = Label(tab1, text="Tolerance:", font=("Open sans", 15))
tol_lbl.grid(column=2, row=2)

tol_txt_msg = StringVar()
tol_txt = Entry(tab1, textvariable=tol_txt_msg, width=3, font=("Open sans", 12))
tol_txt.grid(column=3, row=2)
tol_txt.insert(0, '0')

country_lbl = Label(tab1, text="Country:", font=("Open sans", 15))
country_lbl.grid(column=0, row=3, columnspan=2)

country_txt_msg = StringVar()
country_txt = Entry(tab1, textvariable=country_txt_msg, width=22, font=("Open sans", 12))
country_txt.grid(column=2, row=3, columnspan=2)
country_txt.insert(0, '0')

city_lbl = Label(tab1, text="City:", font=("Open sans", 15))
city_lbl.grid(column=0, row=4, columnspan=2)

city_txt_msg = StringVar()
city_txt = Entry(tab1, textvariable=city_txt_msg, width=22, font=("Open sans", 12))
city_txt.grid(column=2, row=4, columnspan=2)
city_txt.insert(0, '0')

# personal_lbl = Label(window, text="Personal", font=("Open sans", 15))
# personal_lbl.grid(column=0, row=5, columnspan=4)
#
# pol_lbl = Label(window, text="Political", font=("Open sans", 15))
# pol_lbl.grid(column=0, row=9, columnspan=2)
#
# pol_spin = Spinbox(window, from_=0, to=8, width=2, font=("Open sans", 12), )
# pol_spin.grid(column=2, row=6, columnspan=4)
#
# life_lbl = Label(window, text="Life main", font=("Open sans", 15))
# life_lbl.grid(column=0, row=7, columnspan=2)
#
# life_spin = Spinbox(window, from_=0, to=5, width=2, font=("Open sans", 12))
# life_spin.grid(column=2, row=7, columnspan=2)
#
# ppl_lbl = Label(window, text="People main", font=("Open sans", 11))
# ppl_lbl.grid(column=0, row=8, columnspan=2)
#
# ppl_spin = Spinbox(window, from_=0, to=5, width=2, font=("Open sans", 12))
# ppl_spin.grid(column=2, row=8, columnspan=2)
#
# sm_lbl = Label(window, text="Smoking", font=("Open sans", 15))
# sm_lbl.grid(column=0, row=9, columnspan=2)
#
# sm_spin = Spinbox(window, from_=0, to=5, width=2, font=("Open sans", 12))
# sm_spin.grid(column=2, row=9, columnspan=2)
#
# al_lbl = Label(window, text="Alcohol", font=("Open sans", 15))
# al_lbl.grid(column=0, row=10, columnspan=2)
#
# al_spin = Spinbox(window, from_=0, to=5, width=2, font=("Open sans", 12))
# al_spin.grid(column=2, row=10, columnspan=2)

start = Button(tab1, text="Start", font=("Open sans", 15), command=click_button)
start.grid(column=0, row=11, columnspan=4)

# btn = Button(window, text="Не нажимать!", command=clicked)
# btn.grid(column=1, row=1)


window.mainloop()
