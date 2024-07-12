import pyautogui as pag
import random
import screeninfo
import time
import pyperclip
import tkinter as tk
from tkinter import filedialog
import configparser
import keyboard


#------------GLOBAL VARIABLES--------------------------------------------------

def convert_value(value):
    # Convert boolean strings to actual boolean values
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    # Try to convert to int
    try:
        return int(value)
    except ValueError:
        pass
    # Try to convert to float
    try:
        return float(value)
    except ValueError:
        pass
    # Return as string if nothing else matches
    return value


# here is the index of the screen
# if you have 2 screen, first screen is 0, second screen is 1, and so on...
config = configparser.ConfigParser()
config.read('eureka.cfg')

settings = {}
for key, value in config.items('Settings'):
    settings[key] = convert_value(value)


screen_index = settings.get("screen_index")
# laixi app configuration screen
columns = settings.get("columns")
rows = settings.get("rows")

whatsapp_per_phone=settings.get("whatsapp_per_phone")

monitors = list(screeninfo.get_monitors())
monitor = monitors[screen_index]

screen_pos_x = monitor.x
screen_total_width = monitor.width
screen_pos_y = monitor.y
screen_total_height = monitor.height

# here you can set up any type of screen with coordinates
screen_phone_x_start = screen_pos_x + settings.get("screen_phone_x_start")
screen_phone_total_width = settings.get("screen_phone_total_width")
space_beetwen_phones = settings.get("space_beetwen_phones")

screen_phone_y_start = screen_pos_y + settings.get("screen_phone_y_start")
screen_phone_total_height = settings.get("screen_phone_total_height")
gap_space_beetwen_phones = settings.get("gap_space_beetwen_phones")

SCROLL_DELAY = settings.get("scroll_delay")

phone_btns_x=screen_pos_x + settings.get("phone_btns_x")   # 1920 + 1900  ### xxx change
close_phone_btn_y=screen_pos_y + settings.get("close_phone_btn_y")    # 0 + 165    ### xxx change

home_phone_btn_y=close_phone_btn_y+settings.get("home_phone_btn_y")    # 132 + 33 = 165
back_phone_btn_y=close_phone_btn_y+settings.get("back_phone_btn_y")    # 132 + 108 = 240

line_whatsapp_x=screen_pos_x+settings.get("line_whatsapp_x") # 1920 + 1462  ### xxx change
line_whatsapp_y=screen_pos_y+settings.get("line_whatsapp_y") # 0 + 176     ### xxx change
whatsapp_increment=settings.get("whatsapp_icon_increment")

search_whatsapp_x=screen_pos_x+settings.get("search_whatsapp_x")           ### xxx change
search_whatsapp_y=screen_pos_y+settings.get("search_whatsapp_y")            ### xxx change

first_contact_whatsapp_x=screen_pos_x+settings.get("first_contact_whatsapp_x")   # 1920 + 1542  ### xxx change
first_contact_whatsapp_y=screen_pos_y+settings.get("first_contact_whatsapp_y")    # 0 + 264     ### xxx change

microphone_whatsapp_x=screen_pos_x+settings.get("microphone_whatsapp_x")
microphone_whatsapp_y=screen_pos_y+settings.get("microphone_whatsapp_y")

notification_bar_x=screen_pos_x+ settings.get("notification_bar_x")
notification_bar_y=screen_pos_y+ settings.get("notification_bar_y")

notification_not_disturb_btn_x=screen_pos_x+ settings.get("notification_not_disturb_btn_x")
notification_not_disturb_btn_y=screen_pos_y+ settings.get("notification_not_disturb_btn_y")

is_phone_open=settings.get("is_phone_open")
is_phone_in_home=settings.get("is_phone_in_home")

path_phones_file=settings.get("path_phones_file")
path_message_file=settings.get("path_message_file")
path_phones_success=settings.get("path_phones_success")
path_phones_failed=settings.get("path_phones_failed")

msg_separator=settings.get("msg_separator")
number_index=settings.get("number_index")
stop=settings.get("stop")
estado=settings.get("app_state")
current_phone=settings.get("current_phone")
current_ws=settings.get("current_ws")

pause_flag=False



#------------------------------------------------------------------------------



#-------FUNCTIONS--------------------------------------------------------------
def write_with_paste(message=''):
    pyperclip.copy(message)
    pag.hotkey('ctrl', 'v')

def click_at_screen(i, x, y):
    monitors = list(screeninfo.get_monitors())
    print(monitors)
    if i < len(monitors):
        monitor = monitors[i]
        abs_x = monitor.x + x
        abs_y = monitor.y + y
        pag.click(abs_x, abs_y)
    else:
        print("Screen index "+screen_index+" out of range.")
        
#------------------------------------------------------------------------------
def scroll_to_top():
    global screen_total_width, screen_total_height, screen_pos_x, screen_pos_y
    middle_x=screen_pos_x+(screen_total_width/2)
    middle_y=screen_pos_y+(screen_total_height/2)
    pag.moveTo(middle_x, middle_y)
    pag.scroll(10000)
    time.sleep(SCROLL_DELAY)

#------------------------------------------------------------------------------
def get_cell(i):
    global columns,rows
    count=0
    c=0
    r=0
    for k in range(0, rows):
        for j in range(0,columns):
            count+=1
            if (count==i):
                c=j
                r=k
                k=rows+1
                j=columns+1
                
    return r,c

#------------------------------------------------------------------------------
def open_phone(i):
    global screen_phone_total_width, screen_phone_total_,screen_phone_x_start,screen_phone_y_start, columns, rows, is_phone_open,is_phone_in_home
    
    if(i <= columns*rows):
        # 0. click on app
        # 1. scroll at top
        scroll_to_top()
        # 2. scroll to the position of phone
        row, column  = get_cell(i)
        
        calc_scroll_down=( - (screen_phone_total_height+gap_space_beetwen_phones) * (row)  )
        pag.scroll(calc_scroll_down)
        
        # 3. do double click on phone position (middle)    
        
        # every time is up but in the case of the final is at end, take this in mind
        calc_x=screen_pos_x + (screen_phone_total_width+space_beetwen_phones)*(column+1) + (screen_phone_total_width/2)
        
        calc_y_extra=0
        if(rows==(row+1)):
            calc_y_extra=screen_phone_total_height+gap_space_beetwen_phones
            
        calc_y=(screen_phone_total_height/2) + calc_y_extra
        pag.moveTo(calc_x,calc_y)
        pag.doubleClick()
        is_phone_open=True
        is_phone_in_home=False
    else: 
        print("Phone index out of bounds: "+i+" | maxIndex: "+(columns*rows))
    
    print('Abriendo telefono...')


#------------------------------------------------------------------------------
def close_phone():
    global is_phone_open,is_phone_in_home
    if(is_phone_open):
        is_phone_open=False
        is_phone_in_home=False
        pag.click(phone_btns_x,close_phone_btn_y)
        print('Cerrando telefono...')

#------------------------------------------------------------------------------
def phone_btn_home():
    global is_phone_in_home
    if(not is_phone_in_home):
        is_phone_in_home=True
        pag.click(phone_btns_x,home_phone_btn_y)
        print('Inicio ...')
        
#------------------------------------------------------------------------------
def phone_btn_back(clicks=1):
    pag.click(phone_btns_x,back_phone_btn_y,clicks=clicks)
    
#------------------------------------------------------------------------------
def open_search_whatsapp():
    pag.click(search_whatsapp_x,search_whatsapp_y,duration=0.15,clicks=2,interval=0.07)
    print('Abriendo busqueda WS...')
    
#------------------------------------------------------------------------------
def open_whatsapp(i):
    global line_whatsapp_x, line_whatsapp_y,whatsapp_increment,is_phone_in_home
    is_phone_in_home=False
    calc_x=line_whatsapp_x+(whatsapp_increment*i)
    calc_y=line_whatsapp_y
    pag.click(calc_x,calc_y)
    print('Abriendo WS...')
    
#------------------------------------------------------------------------------
def toggle_not_disturb():
    global is_phone_in_home
    if(is_phone_in_home):
        pag.moveTo(notification_bar_x,notification_bar_y)
        pag.dragTo(notification_bar_x,notification_bar_y+710,1,button='left')
        time.sleep(1)
        pag.click(notification_not_disturb_btn_x,notification_not_disturb_btn_y)
        time.sleep(3)
        is_phone_in_home=False
        phone_btn_home()
        time.sleep(3)
        print("Activando/Desactivando No Molestar...")    

#------------------------------------------------------------------------------
def read_file(file_path,separator=None):
    try:
        with open(file_path, mode='r',encoding='utf-8') as file:
            if separator is None:
               return [line.rstrip('\n') for line in file]
            else:
               return file.read().split(separator)
            
    except FileNotFoundError:
        print("The file '"+file_path+"' was not found.")
    except IOError:
        print("Error reading from the file '"+file_path+"'.")


#------------------------------------------------------------------------------
numbers=read_file(path_phones_file)
messages=read_file(path_message_file,msg_separator)

#------------------------------------------------------------------------------
def open_and_send_all_whatsapp(): # is required that phone has been open
    global whatsapp_per_phone, is_phone_open, path_phones_file,first_contact_whatsapp_x,first_contact_whatsapp_y,path_phones_file,msg_separator,microphone_whatsapp_x,microphone_whatsapp_y,number_index
    
    if(is_phone_open):
        msg_len=len(messages)
        for i in range(current_ws,whatsapp_per_phone-1):
            save_in_conf_int('number_index',number_index)
            save_in_conf_int('current_ws',i)
            if pause_flag:
                break
            open_whatsapp(i)
            time.sleep(3)
            if pause_flag:
                break
            open_search_whatsapp()
            time.sleep(3)
            if pause_flag:
                break
            num=numbers[number_index].replace('\n','')
            pag.typewrite(num)
            time.sleep(3)
            if pause_flag:
                break
            pag.click(first_contact_whatsapp_x,first_contact_whatsapp_y)
            time.sleep(2)
            if pause_flag:
                break
            
            # send note
            pag.moveTo(microphone_whatsapp_x,microphone_whatsapp_y)
            pag.dragTo(microphone_whatsapp_x,microphone_whatsapp_y-10,2,button='left')
            time.sleep(2)
            
            msg=''
            while msg=='':
                msg=messages[random.randint(0, msg_len-1)].replace('\n','')
            
            pag.typewrite("\n")
            write_with_paste(msg)
            
            adm_cant=random.randint(1, 10)
            for i in range(1,adm_cant):
                pag.typewrite("!")
                
            time.sleep(2)
            pag.click(microphone_whatsapp_x,microphone_whatsapp_y,duration=1)
            time.sleep(1)
            phone_btn_home()
            time.sleep(3)
            number_index+=1
            if(number_index>=len(numbers)):
                break
            # send random message
            
    else: 
        print(" Phone isn't open!")
        
    print("all message are send!") # finished
    
        
#------------------------------------------------------------------------------
def do_work():
    title="Error al iniciar proceso"
    if(numbers is None):
        tk.messagebox.showerror(title=title,message="El archivo de los Numeros no existe! Ingrese un archivo valido y vuelva a intentarlo")
        return
    elif len(numbers)==0:
        tk.messagebox.showerror(title=title,message="El archivo de los Numeros esta vacio! Ingrese un archivo valido y vuelva a intentarlo")
        return
    elif(messages is None):
        tk.messagebox.showerror(title=title,message="El archivo de los Mensajes no existe! Ingrese un archivo valido y vuelva a intentarlo")
        return
    elif len(messages)==0:
        tk.messagebox.showerror(title=title,message="El archivo de los Mensajes esta vacio! Ingrese un archivo valido y vuelva a intentarlo")
        return
    
    global current_phone
    change_status("En proceso...")
    
    for i in range(current_phone,(columns*rows)+1):
        if number_index<len(numbers):
            if pause_flag:
                break
            open_phone(i)
            save_in_conf_int('current_phone',i)
            time.sleep(2)
            if pause_flag:
                break
            phone_btn_home()
            time.sleep(2)
            if pause_flag:
                break
            toggle_not_disturb()
            open_and_send_all_whatsapp()
            time.sleep(2)
            toggle_not_disturb()
            close_phone()
            if pause_flag:
                break
        else:
            break

    if number_index==(columns*rows):
        change_status("Terminado!")
        reset_all()
        

#------------------------------------------------------------------------------
def reset_all():
    save_in_conf_int('number_index',1)
    save_in_conf_int('current_phone',1)
    save_in_conf_int('current_ws',1)
    
    
#------------------------------------------------------------------------------
def pause_work():
    global pause_flag
    if estado=='En proceso...':
        pause_flag=True
        change_status("Pausado")
        
        

#------------------------------------------------------------------------------
def stop_work():
    global estado
    if estado in ("En proceso...","Pausado"):
        pause_work()
        change_status("Detenido")
        reset_all()
        

#------------------------------------------------------------------------------
def change_status(estatus):
    global estado
    
    estado=estatus
    config.set('Settings','app_state',estado)
    save_save_cfg()
    label0.config(text=estado)

   
#------------------------------------------------------------------------------
def select_file1():
    global path_phones_file,path_message_file
    file_path = filedialog.askopenfilename()
    if file_path:
        path_phones_file=file_path
        config.set('Settings','path_phones_file',path_phones_file)
        save_save_cfg()
        label1.config(text="> "+path_phones_file)

#------------------------------------------------------------------------------            
def select_file2():
    global path_phones_file,path_message_file
    file_path = filedialog.askopenfilename()
    if file_path:    
        path_message_file=file_path
        config.set('Settings','path_message_file',path_message_file)
        save_save_cfg()
        label2.config(text="> "+path_message_file)

#------------------------------------------------------------------------------
def save_save_cfg():
    with open('eureka.cfg','w') as configfile:
        config.write(configfile)

#------------------------------------------------------------------------------
def save_in_conf_int(key,value):
    global current_ws, current_phone, number_index
    
    new_value=0

    try:
        new_value= int(value)
    except ValueError:
        new_value=1
        pass

    if new_value<=0:
        new_value=1


    file_len=0
    if(numbers is not None):
        file_len=len(numbers)

    
    if key=='current_ws':
        if new_value>5:
            new_value=1
        current_ws=new_value-1
        txt_field5.delete(0,tk.END)
        txt_field5.insert(0,new_value)
    
    elif key=='number_index':
        if file_len<new_value:
            new_value=1
        number_index=new_value-1
        txt_field3.delete(0,tk.END)
        txt_field3.insert(0,new_value)

    else: #current_phone
        if new_value>(columns*rows):
            new_value=1
        current_phone=new_value
        txt_field4.delete(0,tk.END)
        txt_field4.insert(0,new_value)

    
    if key in ('current_ws','number_index'):
        config.set('Settings',key,f"{new_value-1}")
    else:
        config.set('Settings',key,f"{new_value}")
    save_save_cfg()
    
    

#------------------------------------------------------------------------------
def save_number_index():
    if estado in ('Detenido','Pausado','Terminado!'):
        save_in_conf_int('number_index',txt_field3.get())
        
#------------------------------------------------------------------------------
def save_current_phone():
    if estado in ('Detenido','Pausado','Terminado!'):
        save_in_conf_int('current_phone',txt_field4.get())

#------------------------------------------------------------------------------
def save_current_ws():
    if estado in ('Detenido','Pausado','Terminado!'):
        save_in_conf_int('current_ws',txt_field5.get())


#------------------------------------------------------------------------------
        
root = tk.Tk()
root.title('EurekaMoney')

label0 = tk.Label(root, text=estado ,anchor=tk.CENTER,bg="white",font=("Calibri",16,"bold"))
label0.grid(row=0,column=1,pady=20,padx=10)

select_button2 = tk.Button(root, text='Select Num.', command=select_file1)
select_button2.grid(row=1, column=0,pady=10,padx=10)

label1 = tk.Label(root, text="> "+path_phones_file)
label1.grid(row=1, column=1,pady=10,padx=10)


select_button2 = tk.Button(root, text='Select Msg.', command=select_file2)
select_button2.grid(row=2, column=0,pady=10,padx=10)

label2 = tk.Label(root, text="> "+path_message_file)
label2.grid(row=2, column=1,pady=10,padx=10)

#----
display_number=''
if(numbers is not None):
    display_number=numbers[number_index]
    
label3 = tk.Label(root, text="Number/Name: ["+display_number+"]",anchor=tk.CENTER)
label3.grid(row=3,column=0,pady=20,padx=10)

txt_field3= tk.Entry(root,width=10)
txt_field3.insert(0,number_index+1)
txt_field3.grid(row=3,column=1,pady=20,padx=10)

select_button3 = tk.Button(root, text='Save', command=save_number_index)
select_button3.grid(row=3, column=2,pady=10,padx=10)

#---
    
label4 = tk.Label(root, text='Actual Phone:',anchor=tk.CENTER)
label4.grid(row=4,column=0,pady=20,padx=10)

txt_field4= tk.Entry(root,width=10)
txt_field4.insert(0,current_phone)
txt_field4.grid(row=4,column=1,pady=20,padx=10)

select_button4 = tk.Button(root, text='Save', command=save_current_phone)
select_button4.grid(row=4, column=2,pady=10,padx=10)

#---

label5 = tk.Label(root, text='Actual Whatsapp:',anchor=tk.CENTER)
label5.grid(row=5,column=0,pady=20,padx=10)

txt_field5= tk.Entry(root,width=10)
txt_field5.insert(0,current_ws+1)
txt_field5.grid(row=5,column=1,pady=20,padx=10)

select_button5 = tk.Button(root, text='Save', command=save_current_ws)
select_button5.grid(row=5, column=2,pady=10,padx=10)

#---

keyboard.add_hotkey('f5',do_work)
start_button = tk.Button(root, text='Start [F5]',command=do_work)
start_button.grid(row=6, column=1,pady=10,padx=10)


keyboard.add_hotkey('f6',pause_work)
pause_button = tk.Button(root, text='Pause [F6]',command=pause_work)
pause_button.grid(row=6, column=2,pady=10,padx=10)

keyboard.add_hotkey('f7',stop_work)
stop_button = tk.Button(root, text='Stop [F7]',command=stop_work)
stop_button.grid(row=6, column=3,pady=10,padx=10)


#------MAIN FUNCTION-----------------------------------------------------------    

if __name__ == "__main__":
    root.mainloop()


