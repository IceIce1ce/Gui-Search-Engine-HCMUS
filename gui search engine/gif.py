import numpy as np
import os
import webbrowser
import tfidf as tf
import dictionary as diction
from tkinter import *
from tkinter import messagebox, font
from PIL import Image, ImageTk, ImageSequence


def search(query, text, dict, number_of_document, list3, idf, list_of_word):
    step1 = tf.get_list(query)  # normalize query
    step2 = diction.query(step1)  # add relevant queries
    step2 = tf.snowball(step2)  # change the query to the basic form
    # print(step1)
    step2 = [dic for dic in step2 if dic in dict]
    if step2 != []:
        query_dict = tf.tfidf(step2)  # find the term-frequency for each word in the query
        query_dict = tf.caculate_tfidf(query_dict, idf, number_of_document)  # find tf-idf for each word in the query
        vector_space = np.zeros((len(query_dict.keys()), number_of_document))  # create array zero
        x = 0
        y = 0
        vector = np.zeros((1, len(query_dict.keys())))
        for lis in query_dict:
            vector[0][x] = query_dict[lis]  # create a tf-idf vector for each word search in the document
            for word in list3:
                if word not in dict[lis]:
                    y += 1
                else:
                    vector_space[x][y] = dict[lis][word]
                    y += 1
            x += 1
            y = 0
        vectorize = np.linalg.norm(vector_space, axis=0)  # change document vector to unit vector
        np.seterr(divide='ignore', invalid='ignore')
        vector_space = np.divide(vector_space, vectorize)
        vector_space[np.isnan(vector_space)] = 0
        query_vectorize = np.linalg.norm(vector, axis=1)  # change the query vector to the unit vector
        vector = np.divide(vector, query_vectorize)
        cosin_similarity = np.dot(vector, vector_space)  # calculate the scalar product value of each document vector with the query vector
        cosin_similarity = cosin_similarity.tolist()
        rank_based = list(zip(cosin_similarity[0], list3))  # sorting cosine scores for ranking all documents.
        rank_based.sort(reverse=True)
        top = Toplevel()
        top.wm_title('Search Engine')
        top.config(background="white")
        blank = '           '
        label = Label(top, text=blank * 15, font=("Arial", 10), background="white")
        # label1 = Label(top, text=query + '\n\n', font=("Arial", 20))
        label1 = Label(top, text='Ranking' + '\n', font=("Arial", 25), background="white")
        label.pack()
        label1.pack()

        def callback(event):
            webbrowser.open_new(event.widget.cget("text"))
        for rank in rank_based[:10]:
            label2 = Label(top, text=rank[1], font=("Arial", 15), justify=LEFT, fg="blue", cursor="hand2", bg="white")
            label2.bind("<Button-1>", callback)
            label2.pack()
    else:
        messagebox.showerror("Error 404", "Sorry, this word doesn't exist")


path_directory = "meta data"  # folder directory
path = [os.path.join(path_directory, file) for file in os.listdir(path_directory)]
doc = {}
docs = []
number_of_document = len(path)
for file in path:  # read each txt file in folder
    doc1 = open(file, 'r')
    texts = [text.strip() for text in doc1.readlines()]
    index = 0
    lines = []
    while True:
        if index >= len(texts):
            break
        tex = texts[index]
        lines.append(tex)
        index += 1
    # tokenize and change text to basic form
    preprocessed = tf.get_list(lines)
    preprocessed = tf.snowball(preprocessed)
    doc = tf.create_index(preprocessed, file, doc)  # make a dictionary to hold every tf-idf score
    docs.append(file)
doc, idf = tf.vector_tfidf(doc, number_of_document)
list_of_words = sorted(doc.keys())
docs.sort()


class GUI:
    def __init__(self, parent):
        self.parent = parent
        parent.title("Search Engine")
        self.canvas = Canvas(parent, width=1200, height=900, bg="White")
        self.sequence = [ImageTk.PhotoImage(img)
                    for img in ImageSequence.Iterator(Image.open('hole.gif'))]
        self.image = self.canvas.create_image(960, 180, image=self.sequence[0])
        self.animating = True
        self.animate(0)
        self.canvas.pack(fill=BOTH, expand=True)
        self.label3 = Label(parent, background="white")
        self.label3.pack()
        self.entry = Entry(parent, bd=8, width=60, font='Arial 18', relief="groove")
        self.entry.insert(END, '')
        self.entry.place(relx=0.5, rely=0.35, anchor=CENTER)
        self.button = Button(parent, text="Google Search", command=lambda: search(self.entry.get(), path, doc, number_of_document, docs, idf, list_of_words))
        self.button.place(relx=0.465, rely=0.4, anchor=CENTER)
        self.button.config(height=2, width=15)
        self.button1 = Button(parent, text="I'm Feeling Lucky", command=lambda: self.open_url("https://www.google.com/doodles"))
        self.button1.place(relx=0.535, rely=0.4, anchor=CENTER)
        self.button1.config(height=2, width=15)
        self.label3 = Label(parent, text="        Advertising        Business        About", font='Arial 10')
        self.label3.bind("<Button-1>", self.callback2)
        self.label3.pack(side=LEFT, padx=0.01, pady=1)
        self.label4 = Label(parent, text="Privacy       Terms       Settings        ", font='Arial 10')
        self.label4.bind("<Button-1>", self.callbackl3)
        self.label4.pack(side=RIGHT, padx=2, pady=1)
        self.my_font = font.Font(weight='bold', size=10)
        self.button2 = Button(parent, text="Sign in", command=lambda: self.open_url1("https://accounts.google.com/ServiceLogin/signinchooser?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com.vn%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin"))
        self.button2.place(relx=0.96, rely=0.04, anchor=CENTER)
        self.button2.config(height=2, width=9, bg="Blue", fg="White", font=self.my_font)
        self.label5 = Label(self.canvas, text="                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Gmail    Images", fg="black", cursor="hand2", bg="white")
        self.label5.bind("<Button-1>", self.callback1)
        self.label5.pack(side=TOP, pady=33)
        self.button3 = Button(parent)
        self.photo = PhotoImage(file="grid.png")
        self.button3.config(image=self.photo, width="13", height="13", bg="white", fg="white")
        self.button3.place(relx=0.919, rely=0.032)
        self.button4 = Button(parent)
        self.photo1 = PhotoImage(file="voice.png")
        self.button4.config(image=self.photo1, width="22", height="22", bg="white", fg="White")
        self.button4.place(relx=0.687, rely=0.335)

    def animate(self, counter):
        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        if not self.animating:
            return
        self.parent.after(30, lambda: self.animate((counter + 1) % len(self.sequence)))

    def open_url(self, url):
        webbrowser.open_new("https://www.google.com/doodles")

    def open_url1(self, url):
        webbrowser.open_new("https://accounts.google.com/ServiceLogin/signinchooser?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com.vn%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

    def callback1(self, url):
        webbrowser.open_new("https://www.google.com.vn/imghp?hl=vi&tab=ri")

    def callback2(self, url):
        webbrowser.open_new("https://about.google/intl/en_vn/?utm_source=google-VN&utm_medium=referral&utm_campaign=hp-footer&fg=1")

    def callbackl3(self, url):
        webbrowser.open_new("https://policies.google.com/privacy?hl=en&gl=vn")


root = Tk()
gui = GUI(root)
root.mainloop()