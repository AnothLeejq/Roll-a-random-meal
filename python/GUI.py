import PySimpleGUI as sg
import python.basicDB as db
import python.onLoad as load
from datetime import datetime
from mysql.connector.locales.eng import client_error
sg.theme('DarkAmber')   # Add a touch of color
table_attributes = ['meat_type','dressing_type','cook_method']
meal_time_option = ['breakfast','lunch','dinner']
date_attributes = ['year','month','day']
input_size = (20,1)
text_size = (16,1)
button_size = (8,1)
currentDateAndTime = datetime.now()
now_date_year = int(str(currentDateAndTime.strftime("%Y")))
now_date_month = int(str(currentDateAndTime.strftime("%m")))
now_date_day = int(str(currentDateAndTime.strftime("%d")))
def add_a_meal_GUI(connection_info):
    # All the stuff inside your window.
    welcome_info = "**I hope you have enjoyed a wonderful meal!**\nWant to remind them again in the future?\nMark them to your history!\nMore details is recommended, or you can also add a virtual meal with your imagination!" 
    
    layout = [  [sg.Text('Add a meal')],
                [sg.Text('Date:',size = text_size), sg.Spin(list(range(2021,now_date_year+1)),initial_value = now_date_year,key='year'),sg.Spin(list(range(1,13)),initial_value = now_date_month,key='month'),sg.Spin(list(range(1,32)),initial_value = now_date_day,key='day')],
                [sg.Text('Meat type:',size = text_size), sg.Input(size = input_size,key='meat_type')],
                [sg.Text('Side dish:',size = text_size), sg.Input(size = input_size,key='dressing_type')],
                [sg.Text('Cooking method:',size = text_size), sg.Input(size = input_size,key='cook_method')],
                [sg.Text('This is your:',size = text_size), sg.CBox('breakfast',key='breakfast'),sg.CBox('lunch',key='lunch'),sg.CBox('dinner',key='dinner')],
                [sg.Button('Add',size = button_size), sg.Button('Cancel',size = button_size),sg.Button('Quit',size = button_size)],
                [sg.Text(welcome_info,size=(40,16), key='output')]
                ],
                

    # Create the Window
    window = sg.Window('What I eat today?', layout,enable_close_attempted_event=True)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if (event == sg.WIN_CLOSED or event == 'Quit') and sg.popup_yes_no('Do you really want to exit?\nThanks for using, I hope you have found what to eat!') == 'Yes': # if user closes window or clicks cancel
            window.close()
            break
        if event == 'Cancel':
            window.close()
            roll_a_meal_GUI(connection_info)
            break
        if event == 'Add':
            tmp_meal_option = ""
            tmp_date_option = ""
            for attribute in date_attributes:
                tmp_date_option += str(values[attribute])
            tmp_result = ""
            for option in meal_time_option:
                if values[option]:
                    tmp_meal_option += option + " "
                    tmp_execute_info = db.database_write_line(connection_info,tmp_date_option,values['meat_type'],values['cook_method'],option,values['dressing_type'])
                    
                    if tmp_execute_info[0] == "error":
                        tmp_result += "Fail to add log to database: {}".format(tmp_execute_info[1])
            if tmp_result != "":
                tmp_result += "\nError occurred, please check the error message and correct your input!"
            else:
                tmp_result += "date: {}\nmeat: {}\nside dish: {}\ncook method: {}\nThis is your {}\n".format(tmp_date_option,values['meat_type'],values['dressing_type'],values['cook_method'],tmp_meal_option)
                tmp_result += "New log have been added! Further rolls will have chance to select it!"
            
            window['output'].update(tmp_result)
    window.close()
def roll_a_meal_GUI(connection_info):
    db_info = load.onload_database(connection_info)
    welcome_info = "**Welcome to roll a meal**\nHard to decide what to cook?\nAsk yourself from history!\nDon't forget to add logs after you enjoy a meal :)" 
    # All the stuff inside your window.
    layout = [  [sg.Text('Roll a meal')],
                #[sg.Text('Roll for your ',size = text_size), sg.Input(size = input_size,key='meal_time')],
                [sg.Text('Roll for your ',size = text_size), sg.CBox('breakfast',key='breakfast'),sg.CBox('lunch',key='lunch'),sg.CBox('dinner',key='dinner')],
                [sg.Text('You dont need to roll ',size = text_size),  sg.CBox('meat',key='meat_type'),sg.CBox('sides',key='dressing_type'),sg.CBox('how to cook',key='cook_method')],
                [sg.Text('Search nearest ',size = text_size), sg.Input(size = input_size,key='date_range'),sg.Text('day(s)')],
                [sg.Button('Roll!',size = button_size), sg.Button('Add a meal',size = button_size),sg.Button('Quit',size = button_size)],
                [sg.Text(welcome_info,size=(40,16), key='output')]
                ]

    # Create the Window
    window = sg.Window('What I eat today?', layout,enable_close_attempted_event=True)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if (event == sg.WIN_CLOSED or event == 'Quit') and sg.popup_yes_no('Do you really want to exit?\nThanks for using, I hope you have found what to eat!') == 'Yes': # if user closes window or clicks cancel
            break
        if event == 'Add a meal':
            window.close()
            add_a_meal_GUI(connection_info)
            break
        if event == 'Roll!':
            tmp_result = ""
            for option in meal_time_option:
                if values[option]:
                    tmp_result += "----{}----".format(option) + "\n"
                    for attribute in table_attributes:
                        if attribute == "meat_type":
                            tmp_result += "Meat: "
                        if attribute == "dressing_type":
                            tmp_result += "Side dish: "
                        if attribute == "cook_method":
                            tmp_result += "How to cook: "
                        if values[attribute]:
                            tmp_result += "Up to you!\n"
                            continue
                        select_info = db.database_select_by_keys(connection_info,attribute,int(values['date_range']),option)
                        tmp_result += select_info[1] + "\n"
            if tmp_result != "":
                tmp_result += "Okay with the result? You can roll it again if you need!"
            else:
                tmp_result += "You have to select at least one option for which meal to roll! (e.g. tick the checkbox before 'breakfast')"
            window['output'].update(tmp_result)

    window.close()