import re
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as sql

# DATABASE (SQL) PASSWORD
PASSWORD = "eiffel100504"

class KulinerFinder():
    # Constructor
    def __init__(self, root):
        self.root = root
        self.query = StringVar()
        self.currentIdx = 0

        # Frame
        self.frame = Frame(self.root, bg="#111111")
        self.frame.place(x = 0, y = 0, width = 1280, height = 720)

        # SEARCH FRAME
        searchFrame = Frame(self.frame, bg="#181818")
        searchFrame.place(x = 0, y = 0, width = 1280, height = 150)

        searchLabel = Label(searchFrame, text = "Cari Menu/Harga Sesuai", font = "Montserrat 20 bold", bg = "#181818", fg = "#FFFFFF")
        searchLabel.place(relx = 0.5, rely = 0.52, anchor = "s")

        searchEntry = Entry(searchFrame, bd = 2, bg = "#FFFFFF", relief = GROOVE, width = 60, textvariable = self.query)
        searchEntry.place(anchor = "ne", relx = 0.6, rely = 0.6)

        searchButton = Button(searchFrame, text = "Search", font = "Montserrat 8 bold", activebackground = "#FFFFFF", fg = "#FFFFFF", bg = "#A7121D", padx=15, pady=0, relief=FLAT, width=10, command = lambda:self.searchQuery())
        searchButton.place(anchor = "nw", relx = 0.61, rely = 0.585)

        # FOOTER FRAME
        footerFrame = Frame(self.frame, bg="#181818")
        footerFrame.place(x = 0, y = 685, width = 1280, height = 35)

        searchLabel = Label(footerFrame, text = "Eiffel Aqila Amarendra - 13520074", font = "Montserrat 8 bold", bg = "#181818", fg = "#FFFFFF")
        searchLabel.place(relx = 0.5, rely = 0.5, anchor = "center")

    # Process Query
    def searchQuery(self):
        if (self.query.get() == ""):
            messagebox.showinfo("Error", "Query is empty")
        else:
            # Pull database
            mycon = sql.connect(host='localhost', user='root', password=PASSWORD, database='kulinerfinder')
            cursor = mycon.cursor()
            cursor.execute('SELECT nama, harga, img_path FROM Menu')
            datas = cursor.fetchall()
            
            self.validateQuery(self.query.get(), datas)


    def validateQuery(self, query, datas):
        dataFiltered = []
        
        # Query Type
        nameOnly = re.compile(r"\w\w*")
        priceOnly = re.compile(r"\d\d*")
        namePrice = re.compile(r"\w\w* \d\d*")

        if (namePrice.fullmatch(query)):
            queries = query.split()

            for data in datas:
                if (self.matchBM(data[0], queries[0]) and (int(data[1]) == int(queries[1]))):
                    dataFiltered.append(data)
            
            if (len(dataFiltered) > 0):
                self.displayItemFrames(self.frame, dataFiltered, 0)
            else:
                messagebox.showinfo("Error", "No data found")
            
        elif (priceOnly.fullmatch(query)):

            for data in datas:
                if ((int(data[1]) == int(query))):
                    dataFiltered.append(data)
            
            if (len(dataFiltered) > 0):
                self.displayItemFrames(self.frame, dataFiltered, 0)
            else:
                messagebox.showinfo("Error", "No data found")
        
        elif (nameOnly.fullmatch(query)):
            for data in datas:
                if (self.matchBM(data[0], query)):
                    dataFiltered.append(data)
            
            if (len(dataFiltered) > 0):
                self.displayItemFrames(self.frame, dataFiltered, 0)
            else:
                messagebox.showinfo("Error", "No data found")

        else:
            messagebox.showinfo("Error", "Invalid input: " + query)
    
    def matchBM(self, text, pattern):
        lastOccurrence = self.buildLast(pattern)
        n = len(text)
        m = len(pattern)

        # Pattern lebih panjang dari text
        if (m > n):
            return False

        else:
            i = m - 1
            j = m - 1
            while (i <= n - 1):
                if (pattern[j] == text[i]):
                    if (j == 0):
                        return True
                    else:
                        j -= 1
                        i -= 1
                else:
                    lo = lastOccurrence[ord(text[i])]
                    i = i + m - min(j, lo+1)
                    j = m - 1
        return False


    def buildLast(self, pattern):
        # Penyimpanan index last occurrence
        lastOccurrence = []
        for i in range (128):
            lastOccurrence.append(-1)
        
        for i in range (len(pattern)):
            lastOccurrence[ord(pattern[i])] = i 
        
        return lastOccurrence

    # Item Search Frame
    def displayItemFrames(self, mainFrame, datas, curIdx):   
        largeItemFrame = Frame(mainFrame, bg="#181818")
        largeItemFrame.place(relx=0.5, rely=0.58, anchor="center", width=800, height=475)
        position = 70

        # Left Button
        if (self.currentIdx >= 4):
            leftButton = Button(mainFrame, text="<", font = "Montserrat 18 bold", activebackground="#FFFFFF", fg = "#FFFFFF", bg = "#A7121D", command=lambda:self.moveLeft(datas))
            leftButton.place(x=100, rely=0.57, anchor="center")
        else:
            leftButton = Button(mainFrame, text="<", font = "Montserrat 18 bold", relief = "flat", activebackground="#1e1e1e", fg = "#1e1e1e", bg = "#181818", command=lambda:self.moveLeft(datas))
            leftButton.place(x=100, rely=0.57, anchor="center")
        # Right Button
        if (self.currentIdx + 4 <= len(datas)):
            rightButton = Button(mainFrame, text=">", font = "Montserrat 18 bold", activebackground="#FFFFFF", fg = "#FFFFFF", bg = "#A7121D", command=lambda:self.moveRight(datas))
            rightButton.place(x=1180, rely=0.57, anchor="center")
        else:
            rightButton = Button(mainFrame, text=">", font = "Montserrat 18 bold", relief = "flat", activebackground="#1e1e1e", fg = "#1e1e1e", bg = "#181818", command=lambda:self.moveRight(datas))
            rightButton.place(x=1180, rely=0.57, anchor="center")

        if(curIdx <= len(datas) - 1):
            global img1
            img1 = ImageTk.PhotoImage(Image.open("../img/" + str(datas[curIdx + 0][2])).resize((100, 100)))

            # Item Frame
            itemFrame1 = Frame(largeItemFrame, bg = "#1e1e1e")
            itemFrame1.place(relx=0.5, y=position, anchor="center", width=750, height=100)

            # Image Tanaman
            imgPlace1 = Label(itemFrame1, image=img1, bg="#1e1e1e")
            imgPlace1.place(x=0, rely=0.5, anchor="w")

            # Name Label
            nameLabel1 = Label(itemFrame1, text=datas[curIdx][0], font="Montserrat 18 bold", bg="#1e1e1e", fg="#FFFFFF")
            nameLabel1.place(x=120, rely=0.1, anchor="nw")

            # Price Label
            priceLabel1 = Label(itemFrame1, text="Rp." + str(datas[curIdx][1]), font="Montserrat 12 bold", bg="#1e1e1e", fg="#A7121D")
            priceLabel1.place(x=120, rely=0.9, anchor="sw")

            position += 110
            if (curIdx <= len(datas) - 2):
                global img2
                img2 = ImageTk.PhotoImage(Image.open("../img/" + str(datas[curIdx + 1][2])).resize((100, 100)))

                # Item Frame
                itemFrame2 = Frame(largeItemFrame, bg = "#1e1e1e")
                itemFrame2.place(relx=0.5, y=position, anchor="center", width=750, height=100)

                # Image Tanaman
                imgPlace2 = Label(itemFrame2, image=img2, bg="#1e1e1e")
                imgPlace2.place(x=0, rely=0.5, anchor="w")

                # Name Label
                nameLabel2 = Label(itemFrame2, text=datas[curIdx + 1][0], font="Montserrat 18 bold", bg="#1e1e1e", fg="#FFFFFF")
                nameLabel2.place(x=120, rely=0.1, anchor="nw")

                # Price Label
                priceLabel2 = Label(itemFrame2, text="Rp." + str(datas[curIdx + 1][1]), font="Montserrat 12 bold", bg="#1e1e1e", fg="#A7121D")
                priceLabel2.place(x=120, rely=0.9, anchor="sw")


                position += 110
                if (curIdx <= len(datas) - 3):
                    global img3
                    img3 = ImageTk.PhotoImage(Image.open("../img/" + str(datas[curIdx + 2][2])).resize((100, 100)))

                    # Item Frame
                    itemFrame3 = Frame(largeItemFrame, bg = "#1e1e1e")
                    itemFrame3.place(relx=0.5, y=position, anchor="center", width=750, height=100)

                    # Image Tanaman
                    imgPlace3 = Label(itemFrame3, image=img3, bg="#1e1e1e")
                    imgPlace3.place(x=0, rely=0.5, anchor="w")

                    # Name Label
                    nameLabel3 = Label(itemFrame3, text=datas[curIdx + 2][0], font="Montserrat 18 bold", bg="#1e1e1e", fg="#FFFFFF")
                    nameLabel3.place(x=120, rely=0.1, anchor="nw")

                    # Price Label
                    priceLabel3 = Label(itemFrame3, text="Rp." + str(datas[curIdx + 2][1]), font="Montserrat 12 bold", bg="#1e1e1e", fg="#A7121D")
                    priceLabel3.place(x=120, rely=0.9, anchor="sw")

                    position += 110
                    if (curIdx <= len(datas) - 4):
                        global img4
                        img4 = ImageTk.PhotoImage(Image.open("../img/" + str(datas[curIdx + 3][2])).resize((100, 100)))

                        # Item Frame
                        itemFrame4 = Frame(largeItemFrame, bg = "#1e1e1e")
                        itemFrame4.place(relx=0.5, y = position, anchor="center", width=750, height=100)

                        # Image Tanaman
                        imgPlace4 = Label(itemFrame4, image=img4, bg="#1e1e1e")
                        imgPlace4.place(x=0, rely=0.5, anchor="w")

                        # Name Label
                        nameLabel4 = Label(itemFrame4, text=datas[curIdx + 3][0], font="Montserrat 18 bold", bg="#1e1e1e", fg="#FFFFFF")
                        nameLabel4.place(x=120, rely=0.1, anchor="nw")

                        # Price Label
                        priceLabel4 = Label(itemFrame4, text="Rp." + str(datas[curIdx + 3][1]), font="Montserrat 12 bold", bg="#1e1e1e", fg="#A7121D")
                        priceLabel4.place(x=120, rely=0.9, anchor="sw")


                        position += 110
                    
    def moveLeft(self, datas):
        if (self.currentIdx > 4):
            self.currentIdx = self.currentIdx - 4
            self.displayItemFrames(self.frame, datas, self.currentIdx)
        else:
            self.currentIdx = 0
            self.displayItemFrames(self.frame, datas, self.currentIdx)

    def moveRight(self, datas):
        if (self.currentIdx + 4 < len(datas)):
            self.currentIdx = self.currentIdx + 4
            self.displayItemFrames(self.frame, datas, self.currentIdx)
        else:
            self.displayItemFrames(self.frame, datas, self.currentIdx)
            
def connectDatabase():
    try:
        # Create/Connect Database
        mycon = sql.connect(host='localhost', user='root', password=PASSWORD)
        cursor = mycon.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS `kulinerfinder`")

        mycon.close()

        # Setup Database
        mycon = sql.connect(host='localhost', user='root', password=PASSWORD, database='kulinerfinder')
        cursor = mycon.cursor()

        sqlRestore = open("KulinerFinder.sql").read()
        cursor.execute(sqlRestore, multi=True)

        mycon.close()
    except sql.Error as msg:
        messagebox.showerror("Gagal menggunakan basis data: ", msg)


# MAIN PROGRAM
if __name__ == '__main__':
    # Root window
    root = Tk()
    root.title("Kuliner Finder")
    root.geometry("1280x720+100+50")
    root.config(bg = "#DCE1DE")
    connectDatabase()
    KulinerFinder(root)

    # Main Loop
    root.mainloop()