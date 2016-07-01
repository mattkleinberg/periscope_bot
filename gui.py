from reddit_bot import RedditBot
from tkinter import *
from tkinter import ttk
from multiprocessing import Process, Queue
import time
import get_periscope


class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self)
        self.bot_running = False
        self.update_text_job = None
        self.labels = []
        self.dl_btns = []
        self.download_list = []
        self.counter = 1

        self.parent = parent
        self.grid()
        self.q = Queue()
        self.q2 = Queue()
        self.init_ui()

    def init_ui(self):
        self.top_lf = LabelFrame(self.parent, text="Reddit Bot Controls")
        self.top_lf.grid(row=0, columnspan=4, sticky="WE", padx=10, pady=10)

        self.bottom_lf = LabelFrame(self.parent, text="Periscope Status")
        self.bottom_lf.grid(row=1, columnspan=4, sticky="WE", padx=10, pady=10)

        self.bot_label = Label(self.top_lf, text="Bot Status: ", font=24)
        self.bot_status = Label(self.top_lf, text='Not Running', bg='red', fg="white", width=15)
        # change on_click to start_bot later
        self.bot_start = Button(self.top_lf, command=self.start_bot, text="Start Bot")
        # change on_click to stop_bot later
        self.bot_stop = Button(self.top_lf, command=self.stop_bot, text="Stop Bot", state=DISABLED)
        self.bot_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.bot_status.grid(row=0, column=1, sticky=N+S+W, padx=25, pady=5)
        self.bot_start.grid(row=0, column=2, sticky=E, padx=5, pady=5)
        self.bot_stop.grid(row=0, column=3, sticky=E, padx=5, pady=5)

        self.bot_label = Label(self.bottom_lf, text="Bot is currently offline.", font='bold')
        self.bot_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)

    def start_bot(self):
        self.update_text()
        self.bot_running = True
        self.bot_status.config(text='Running', bg='green')
        self.bot_label.config(text="Searching for periscope posts...")
        self.bot_start.config(state=DISABLED)
        self.bot_stop.config(state="normal")
        # need to do multi threading for reddit bot searching
        global process
        process = Process(target=bot_start, args=(self.q,))
        process.start()

    def stop_bot(self):
        self.bot_running = False
        self.counter = 1
        self.labels[:] = []
        self.dl_btns[:] = []

        self.bot_status.config(text='Not Running', bg='red')
        self.bot_label.config(text="Bot is currently offline.")
        self.bot_stop.config(state=DISABLED)
        self.bot_start.config(state="normal")
        # shouldnt need to do multi threading here but might have to
        print('stopping bot')
        # may need to uncomment the below line later as it may lead to memory leaks
        # look more into Queues being left open
        # self.q.close()
        if self.update_text_job is not None:
            self.after_cancel(self.update_text_job)
            self.update_text_job = None
        process.terminate()

    def update_text(self):
        print('update text running')
        if self.q.empty() is False:
            print('queue not empty')
            # create new labels under existing ones
            x = self.q.get()
            for i, value in enumerate(x):
                self.counter += 1
                self.labels.append(Label(self.bottom_lf, text=value))
                self.dl_btns.append(Button(self.bottom_lf, text="Download",
                                           command=lambda url=value, row=self.counter: self.download(url, row)))

                self.labels[i].grid(row=self.counter, column=0, padx=5, pady=5, sticky=W)
                self.dl_btns[i].grid(row=self.counter, column=1, padx=5, pady=5, sticky=E)
                # self.bot_label.config(text=self.q.get())
        self.update_text_job = self.after(10000, self.update_text)

    def download(self, url, row):
        global p2
        self.progress = ttk.Progressbar(self.bottom_lf, orient=HORIZONTAL, length=75, mode='indeterminate')
        if self.q2.empty() is False:
            x = self.q2.get()
            print(x)
            self.progress.stop()
            p2.terminate()

        else:
            p2 = Process(target=download_start, args=(url, self.q2))
            # will start new process to download the video to folder
            self.progress.grid(row=row, column=2, padx=5, pady=5, sticky=E)
            self.progress.start()
            p2.start()
            # On download complete switch button to show open folder

    def check_downloads(self, download_index):
        if self.download_list[download_index]:
            print('hello')


def bot_start(q):
    print('starting bot test')
    testing = RedditBot()
    while True:
        # checks every two minutes for periscope post
        output = testing.reddit_search()
        if output:
            q.put(output)
        time.sleep(120)


def download_start(url, q2):
    output = get_periscope.download_periscope(url)
    q2.put(output)


if __name__ == '__main__':
    root = Tk()
    root.title("Reddit Periscope Bot")
    # root.geometry("600x400")
    app = GUI(root)
    app.mainloop()
