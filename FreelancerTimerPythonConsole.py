from sqlite3 import Time
import tkinter as tk
import json
import datetime
import winsound
import time

# GLOBALS
deadline_date = 0
current_remainder = 0
week_hours = 0
pommodoroMinutes = 0
current_pommodoro = 0
pommodoro_index = 0
hour_index = 0

remainder_data = []

on_pause = False

def read_json():
    global deadline_date, week_hours, pommodoroMinutes, remainder_data
    
    try:
        with open('setup.json') as file:
            data = json.load(file)
            project_name_label.config(text=data['projectName'])
            week_start = data['weekStart']
            week_hours=data['weekHours']
            pommodoroMinutes=data['pommodoroMinutes']
            deadline_label.config(text=f"{data['deadLineYear']}-{data['deadLineMonth']}-{data['deadLineDay']}")
            
            update_current_remainder(1000)
            
            deadline_date = datetime.datetime(data['deadLineYear'], data['deadLineMonth'], data['deadLineDay'])

            # Update the deadline text field with the remaining seconds
            update_deadline()
    except FileNotFoundError:
        print("JSON file not found!")
        
    try:
        with open('current_remainder.json') as file:
            remainder_data = json.load(file)
            remainder=remainder_data['current_remainder']
            update_current_remainder(remainder)
    except FileNotFoundError:
        print("JSON file not found!")

def update_deadline():
    global deadline_date
    
    now = datetime.datetime.now()
    remaining_seconds = (deadline_date - now).total_seconds() - 1
    if remaining_seconds >= 0:
        integer_seconds = int(remaining_seconds)
        formatted_seconds = "{:,}".format(integer_seconds)
        deadline_text = formatted_seconds
    else:
        deadline_text = "Deadline has passed"
        deadline_field.configure(bg="red")
        
    deadline_field.config(text=deadline_text)
    
    # Schedule the next update in 1 second
    deadline_field.after(1000, update_deadline)
    
def reset_week():
    global current_remainder, week_hours
    
    seconds = week_hours*60*60 
    update_current_remainder(seconds)
    
def update_current_remainder(seconds):
    global current_remainder
    
    current_remainder = seconds
    current_remainder_text = f"{int(current_remainder)}"
    current_week_field.config(text=current_remainder_text)
    
def update_pommodoro():
    global current_pommodoro, current_remainder, pommodoro_index, hour_index, pommodoros, remainder_data
    global on_pause

    current_pommodoro = current_pommodoro -1
    
    if current_pommodoro >= 0:
        formatted_seconds = "{:,}".format(int(current_pommodoro))
        current_pommodoro_field.config(text=formatted_seconds)
        
        current_remainder = current_remainder - 1
        update_current_remainder(current_remainder)
        
        # Schedule the next update in 1 second
        if not on_pause:
            current_pommodoro_field.after(1000, update_pommodoro)
    else:
        print("Pommodoro finished")
        pause_resume_button.config(state="disabled")
        start_button.config(state="active")
        current_pommodoro = 0
        current_pommodoro_field.config(text="click START to start")
        
        # Update the "current_remainder" value
        remainder_data["current_remainder"] = current_remainder
        # Write the updated data back to the JSON file
        with open('current_remainder.json', 'w') as json_file:
            json.dump(remainder_data, json_file)
        
        # Play a sound
        winsound.PlaySound("Alarm05.wav", winsound.SND_ASYNC)
        
        if pommodoro_index < 3:
            pommodoros[pommodoro_index].configure(bg="red")
            pommodoro_index = pommodoro_index + 1
            
        if pommodoro_index >= 3:
            if hour_index < 12:
                if hour_index < 8:
                    hours[hour_index].configure(bg="green")
                else:
                    if hour_index < 10:
                        hours[hour_index].configure(bg="orange")
                    else:
                        hours[hour_index].configure(bg="red")
                hour_index = hour_index + 1
            
        
    
def pause_resume():
    global on_pause
    print("pause/resume")
    
    if on_pause:
        pause_resume_button.config(text='||')
        on_pause = False
        update_pommodoro()
    else:
        pause_resume_button.config(text='>>')
        on_pause = True
        

def start():
    global current_pommodoro, pommodoro_index, pommodoros, pommodoroMinutes
    
    print("start")
    start_button.config(state="disabled")
    pause_resume_button.config(state="active")
    current_pommodoro = int(pommodoroMinutes * 60)
    #current_pommodoro = int(15)
    
    if pommodoro_index >= 3:
        pommodoro_index = 0
        for i in range(3):
            pommodoros[i].configure(bg="yellow")
            
    update_pommodoro()


root = tk.Tk()
root.title("Freelancers timer")
root.attributes("-topmost", True)  # Set the window to be always on top


# Set initial dimensions of the GUI window
#root.geometry("500x300")

# Create labels
project_name_label = tk.Label(root, text="Project Name: ")
project_name_label.pack()

# Create a label for the deadline countdown
delimiter_label01 = tk.Label(root, text="***********************")
delimiter_label01.pack()

# Create button start new week
new_week_button = tk.Button(root, text="start new week", command=reset_week)
new_week_button.pack()
# Create a label for the current week reminder
current_week_field = tk.Label(root, text="current reminder...")
current_week_field.pack()

# Create a label for the deadline countdown
delimiter_label01 = tk.Label(root, text="***********************")
delimiter_label01.pack()

# Create a label for the deadline
deadline_signature_label = tk.Label(root, text="Deadline: ")
deadline_signature_label.pack()
deadline_label = tk.Label(root, text="Deadline: ")
deadline_label.pack()

# Create a label for the deadline countdown
deadline_field = tk.Label(root, text="Calculating remaining seconds...")
deadline_field.pack()

# Create a label for the deadline countdown
delimiter_label0 = tk.Label(root, text="***********************")
delimiter_label0.pack()

# Create button pause/resume
pause_resume_button = tk.Button(root, text="||", command=pause_resume)
pause_resume_button.pack()
pause_resume_button.config(state="disabled")

# Create button start
start_button = tk.Button(root, text="START", command=start)
start_button.pack()

# Create a label for the deadline
current_pommodoro_field = tk.Label(root, text="click START to start")
current_pommodoro_field.pack()

# Create a label for the deadline countdown
delimiter_label1 = tk.Label(root, text="***********************")
delimiter_label1.pack()

# Create a frame to hold the labels
pommodoro_frame = tk.Frame(root)
pommodoro_frame.pack()

# Create the three labels and place them in the bottom frame
pommodoro1 = tk.Label(pommodoro_frame, text="    ")
pommodoro1.pack(side="left", padx=10)
pommodoro1.configure(bg="yellow")

pommodoro2 = tk.Label(pommodoro_frame, text="    ")
pommodoro2.pack(side="left", padx=10)
pommodoro2.configure(bg="yellow")

pommodoro3 = tk.Label(pommodoro_frame, text="    ")
pommodoro3.pack(side="left", padx=10)
pommodoro3.configure(bg="yellow")

pommodoros = [pommodoro1, pommodoro2, pommodoro3]

# Create a frame to hold the labels
regular_hours_frame = tk.Frame(root)
regular_hours_frame.pack()

# Create the labels and place them in the bottom frame
hour1 = tk.Label(regular_hours_frame, text=" ")
hour1.pack(side="left", padx=10)

hour2 = tk.Label(regular_hours_frame, text=" ")
hour2.pack(side="left", padx=10)

hour3 = tk.Label(regular_hours_frame, text=" ")
hour3.pack(side="left", padx=10)

hour4 = tk.Label(regular_hours_frame, text=" ")
hour4.pack(side="left", padx=10)

hour5 = tk.Label(regular_hours_frame, text=" ")
hour5.pack(side="left", padx=10)

hour6 = tk.Label(regular_hours_frame, text=" ")
hour6.pack(side="left", padx=10)

hour7 = tk.Label(regular_hours_frame, text=" ")
hour7.pack(side="left", padx=10)

hour8 = tk.Label(regular_hours_frame, text=" ")
hour8.pack(side="left", padx=10)

# Create a frame to hold the labels
extra_hours_frame = tk.Frame(root)
extra_hours_frame.pack()

# Create the labels and place them in the bottom frame
hour9 = tk.Label(extra_hours_frame, text=" ")
hour9.pack(side="left", padx=10)

hour10 = tk.Label(extra_hours_frame, text=" ")
hour10.pack(side="left", padx=10)

hour11 = tk.Label(extra_hours_frame, text=" ")
hour11.pack(side="left", padx=10)

hour12 = tk.Label(extra_hours_frame, text=" ")
hour12.pack(side="left", padx=10)

hours = [hour1, hour2, hour3, hour4, hour5, hour6, hour7, hour8, hour9, hour10, hour11, hour12]

read_json()

root.mainloop()