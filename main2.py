from tkinter import *
import time
from threading import Thread

class Timer:
    def __init__(self, label, status_label):
        self.label = label
        self.limit = None
        self.isRunning = False
        self.status_label = status_label
        self.isReset = False
        self.isStopped = False
        self.isPaused = False

    def _seconds_to_format(self, seconds):
        hours = str(seconds // 3600)
        minutes = str(seconds // 60 % 60)
        seconds = str(seconds % 60)

        return "0" * (2 - len(hours)) + hours + ":" + "0" * (2 - len(minutes)) + minutes + ":" + "0" * (2 - len(seconds)) + seconds

    def start(self):
        t = Thread(target=self.__start)
        t.start()

    def __start(self):
        self.status_label.config(fg="black")
        if not self.limit or self.isRunning:
            return
        self.isRunning = True
        while self.limit >= 0 if self.limit else self.isRunning:
            if(not self.isRunning):
                break
            self.label.config(text=self._seconds_to_format(self.limit))
            self.limit -= 1
            time.sleep(1)
        self.isRunning = False
        status = "Reset" if self.isReset else ("Stopped" if self.isStopped else ("Paused" if self.isPaused else  "Time's up!"))
        self.status_label.config(text=status)
        self.status_label.config(fg="red" if not self.isReset and self.isStopped and self.isPaused else "black")
        if not self.isPaused:
            self.limit = None
        self.isReset = False
        self.isStopped = False

    def pause(self):
        self.isRunning = False
        


def main():
    root = Tk()
    root.title("Countdown Timer")
    root.geometry('500x400')
    label = Label(root, text="Countdown Timer", font=("Arial", 20))
    label.pack()
    countdown = Label(root, text="00:00:00", font=("Arial", 60))
    countdown.pack()
    entry_frame = Frame(root)
    hours_label = Label(entry_frame, text="Hours:", font=("Arial", 10), padx=10, pady=10)
    hours_label.pack(side=LEFT)
    hours_entry = Entry(entry_frame, font=("Arial", 10))
    hours_entry.pack(side=LEFT)
    hours_entry.focus()
    hours_entry.config(width=10)
    hours_entry.insert(0, "0")
    minutes_label = Label(entry_frame, text="Minutes:", font=("Arial", 10), padx=10, pady=10)
    minutes_label.pack(side=LEFT)
    minutes_entry = Entry(entry_frame, font=("Arial", 10))
    minutes_entry.pack(side=LEFT)
    minutes_entry.insert(0, "0")
    minutes_entry.config(width=10)
    seconds_label = Label(entry_frame, text="Seconds:", font=("Arial", 10), padx=10, pady=10)
    seconds_label.pack(side=LEFT)
    seconds_entry = Entry(entry_frame, font=("Arial", 10))
    seconds_entry.pack(side=LEFT)
    seconds_entry.insert(0, "0")
    seconds_entry.config(width=10)
    entry_frame.pack()
    button_frame = Frame(root, padx=10, pady=10)
    button_col_1_frame = Frame(button_frame, relief='flat')
    button_col_2_frame = Frame(button_frame, relief='flat')
    start_button = Button(button_col_1_frame, text="Start", font=("Arial", 10), width=10, height=2, relief='flat', bg='#0F9D58', fg='white')
    start_button.pack(side=LEFT, anchor=CENTER, pady=10, padx=10)
    pause_button = Button(button_col_1_frame, text="Pause", font=("Arial", 10), width=10,height=2, relief='flat', bg='#F4B400', fg='black')
    pause_button.pack(side=LEFT, anchor=CENTER, pady=10, padx=10)
    reset_button = Button(button_col_2_frame, text="Reset", font=("Arial", 10), width=10,height=2, relief='flat', bg='#4285F4', fg='white')
    reset_button.pack(side=LEFT, anchor=CENTER, pady=10, padx=10)
    stop_button = Button(button_col_2_frame, text="Stop", font=("Arial", 10), width=10,height=2, relief='flat', bg='#DB4437', fg='white')
    stop_button.pack(side=LEFT, anchor=CENTER, pady=10, padx=10)
    button_col_1_frame.pack(fill=X)
    button_col_2_frame.pack(fill=X)
    button_frame.pack()
    status_label = Label(root, text="Ready", font=("Arial", 10), padx=10, pady=10)
    status_label.pack()
    t = Timer(countdown, status_label)
    
    def start_timer():
        if not t.limit:
            try:
                t.limit = int(hours_entry.get()) * 60 * 60 + int(minutes_entry.get()) * 60 + int(seconds_entry.get())
            except ValueError:
                status_label.config(fg="red")
                status_label.config(text="Enter a valid number")
                time.sleep(1)
                status_label.config(text="Ready")
                status_label.config(fg="black")
        t.start()
        status_label.config(text="Running")

    def pause_timer():
        if not t.limit:
            return
        if t.isRunning:
            t.isRunning = False
            t.isPaused = True
            t.pause()
            pause_button.config(text="Resume") 
        else:
            pause_button.config(text="Pause")
            t.isPaused = False
            status_label.config(text="Running")
            t.start()
            

    def reset_timer():
        t.isReset = True
        t.isRunning = False
        t.limit = None
        countdown.config(text="00:00:00")
        pause_button.config(text="Pause")
        status_label.config(fg="black", text="Reset")

    def stop_timer():
        t.isStopped = True
        t.isRunning = False
        t.limit = None
        pause_button.config(text="Pause")
        status_label.config(fg="black", text="Stopped")

    

    start_button.config(command=start_timer)
    pause_button.config(command=pause_timer)
    stop_button.config(command=stop_timer)
    reset_button.config(command=reset_timer)

    root.mainloop()

if __name__ == '__main__':
    main()