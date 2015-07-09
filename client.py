from Tkinter import *
import time
import threading
import Queue
import socket
import io
from PIL import ImageTk, Image

class GuiPart:
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        # Set up the GUI

        self.l = Label(master, text='No Image yet')
        self.l.grid(row=1, column=0, columnspan=3)

        # Add more GUI stuff here depending on your specific needs
        b1 = Button(master, text = 'Quit', command=endCommand)
        b1.grid(row=0, column=0, sticky=W)

        b2 = Button(master, text = 'Forward')
        b2.grid(row=2, column=1, sticky=W+E)

        b3 = Button(master, text = 'Left')
        b3.grid(row=3, column=0, sticky=W+E)

        b4 = Button(master, text = 'Right')
        b4.grid(row=3, column=2, sticky=W+E)

        b5 = Button(master, text = 'Reverse')
        b5.grid(row=4, column=1, sticky=W+E)

        #bleft = Tkinter.Button(master, text="Left")
        #bleft.bind('<Button-1>', self._leftDown)
        #bleft.bind('<ButtonRelease-1>', self._stopMotion)
        #bleft.pack()

        #bright = Tkinter.Button(master, text="Right")
        #bright.bind('<Button-1>', self._rightDown)
        #bright.bind('<ButtonRelease-1>', self._stopMotion)
        #bright.pack()

        # Controlconnection
        # HOST, PORT = 'localhost', 9998
        # self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.csock.connect((HOST, PORT))

    def _leftDown(self, event):
        # TODO: Send a 'left' command to the control port
        #self.csock.send('left')
        print 'left'

    def _stopMotion(self, event):
        # TODO: Send a 'left' command to the control port
        #self.csock.send('stop')
        print 'stop'

    def _rightDown(self, event):
        # TODO: Send a 'left' command to the control port
        #self.csock.send('left')
        print 'right'


    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                img = ImageTk.PhotoImage(Image.open(io.BytesIO(msg)))
                self.l.configure(image = img)
                self.l.image = img
            except Queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass


class ThreadHandler:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = Queue.Queue(  )

        self.numThreads = 0

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        thread1 = threading.Thread(target=self.workerThread1)
        thread1.start()

        # This will run in the main thread.
        self.updateGui()

    def updateGui(self):

        if not self.running:
            return

        self.gui.processIncoming()
        self.master.after(200, self.updateGui)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        HOST, PORT = 'localhost', 9999
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        self.numThreads += 1
        while self.running:
            # Read messages (later images from the video link)
            reply = sock.recv(163840)  # limit reply to 16K
            self.queue.put(reply)

        sock.close()
        self.numThreads -= 1

    def endApplication(self):
        self.running = 0
        while self.numThreads > 0:
            time.sleep(0.1)
        self.master.quit()

root = Tk()

client = ThreadHandler(root)
root.mainloop()
