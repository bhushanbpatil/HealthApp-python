from tkinter import *
import xlrd
import tkinter.font as tkFont

def raise_frame(frame):
    frame.tkraise()

file_location=r"C:\Users\admin\Desktop\python proj\learning\nutrition (2).xls"
workbook=xlrd.open_workbook(file_location)
sheet=workbook.sheet_by_index(0)
lista=[]
d={}
for i in range(1,sheet.nrows):
	lista.append(sheet.cell_value(i,0))
	l=[]
	l.append(sheet.cell_value(i,1))
	l.append(sheet.cell_value(i,3))
	l.append(sheet.cell_value(i,4)) 	
	d[sheet.cell_value(i,0)]=l

#lista = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle', 'are', 'as', 'be', 'bind', 'bracket', 'brackets', 'button', 'can', 'cases', 'configure', 'course', 'detail', 'enter', 'event', 'events', 'example', 'field', 'fields', 'for', 'give', 'important', 'in', 'information', 'is', 'it', 'just', 'key', 'keyboard', 'kind', 'leave', 'left', 'like', 'manager', 'many', 'match', 'modifier', 'most', 'of', 'or', 'others', 'out', 'part', 'simplify', 'space', 'specifier', 'specifies', 'string;', 'that', 'the', 'there', 'to', 'type', 'unless', 'use', 'used', 'user', 'various', 'ways', 'we', 'window', 'wish', 'you']


class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):  

        if self.var.get() == '':
        	self.lb.destroy()
        	self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

#############################################################################################33

root = Tk()
root.configure(background='black')
root.title("Health App")
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
f1 = Frame(root)
f2 = Frame(root,bg='#ff7580')
f3 = Frame(root,bg='#f73848')
f4 = Frame(root, bg='#fc0015')

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

Button(f1, text='DAILY',font=tkFont.Font(family='Sans-serif', size=24), command=lambda:raise_frame(f2),bg='#ff7580').pack(fill=BOTH,ipadx=0,ipady=20,expand=0)
Button(f1, text='MONTHLY', command=lambda:raise_frame(f3),font=tkFont.Font(family='Sans-serif', size=24),bg='#f73848').pack(fill=BOTH,ipadx=0,ipady=20,expand=0)
Button(f1, text='YEARLY', command=lambda:raise_frame(f4),font=tkFont.Font(family='Sans-serif', size=24), bg='#fc0015').pack(fill=BOTH,ipadx=0,ipady=20,expand=0)

############ f2
Label(f2, text = " How many servings did you eat today?",bg='#ff7580',font=tkFont.Font(family='Sans-serif')).grid(row = 0, column = 0)
Servings = Entry(f2)
Servings.grid(row = 1, column = 0,sticky='e,w')
Servings.insert(0, "0")       
Button(f2, text = "Submit",command=lambda:serve(),bg='#a0010e').grid(row=3,column=0)
Button(f2, text='Main Menu', command=lambda:raise_frame(f1),bg='#ffe5e5').grid(row=4,column=0)
Button(f3, text='Main Menu', command=lambda:raise_frame(f1),bg='#ffe5e5').grid(row=16,columnspan=1)
Button(f4, text='Main Menu', command=lambda:raise_frame(f1),bg='#ffe5e5').grid(row=400,column=0)
def serve():

	serve = int(Servings.get())
	temp=1
	tserv=serve

	servelist=[]
	while serve>0:
		serve=serve-1
		Label(f2, text = "Food "+str(tserv-serve),bg='#ff7580',font=tkFont.Font(family='Sans-serif')).grid(row = 5+temp, column = 0)
		Serving = AutocompleteEntry(lista, f2)
		Serving.grid(row = 6+temp, column = 0,sticky='e,w')
		Serving.insert(0, "")
		servelist.append(Serving)
		temp=temp+2
	Button(f2, text = "Enter",command=lambda:calcal(servelist,temp),bg='#a0010e').grid(row=5+temp,column=0)	

def calcal(servelist,temp):

	kcal=0
	prot=0
	fat=0

	for i in servelist: 
		kcal=kcal+int(d[i.get()][0])

	for i in servelist: 
		prot=prot+int(d[i.get()][1])
		
	for i in servelist: 
		fat=fat+int(d[i.get()][2])		

	Label(f2, text = ("Kcal=",kcal)).grid(row = 6+temp, column = 0)
	Label(f2, text = ("Protein=",prot,'g')).grid(row = 7+temp, column = 0)
	Label(f2, text = ("Fats=",fat,'g')).grid(row = 8+temp, column = 0)


Label(f2, text = "___________________________________________________________________________________",bg='#ff7580').grid(row = 5, column = 0)
############ f2

############ F3
Label(f3, text = "BMI Calculator",bg='#f73848',font=("Helvetica", 16)).grid(row=0,columnspan = 6)

Label(f3, text = "Height (ft)",bg='#f73848').grid(row = 1, column = 0)
txtHeightFt = Entry(f3)
txtHeightFt.grid(row = 1, column = 1)
txtHeightFt.insert(0, "0")

Label(f3, text = "  Height (in)",bg='#f73848').grid(row = 1, column = 3)
txtHeightIn = Entry(f3)
txtHeightIn.grid(row = 1, column = 4)
txtHeightIn.insert(0, "0")

Label(f3, text = "Weight (lbs)",bg='#f73848').grid(row = 2, column = 0)
txtWeight = Entry(f3)
txtWeight.grid(row = 2, column = 1)
txtWeight.insert(0, "0")

Label(f3, text = "Your BMI:",bg='#f73848').grid(row = 5, column = 0)
f3.lblBMI = Label(f3, bg = "#fff",relief = "groove")
f3.lblBMI.grid(row = 5, column = 1, sticky = "we")
Label(f3, text = "You are:",bg='#f73848').grid(row = 5, column = 3)
f3.lblBMIStatus = Label(f3)
f3.lblBMIStatus.grid(row = 5, column = 4)

Label(f3, text = "____________________________________________________________________________________",bg='#f73848').grid(row = 11, columnspan = 10)
Label(f3, text = " Suggestions:",bg='#f73848').grid(row = 12, column = 0, sticky='w')
Label(f3, text = " Weight:",bg='#f73848').grid(row = 13, columnspan = 1,sticky='w')
Label(f3, text = " Calorie intake: ",bg='#f73848').grid(row = 14, columnspan = 1,sticky='w')
Label(f3, text = " Protein intake: ",bg='#f73848').grid(row = 15, columnspan = 1,sticky='w')
f3.SWeight=Label(f3)
f3.SWeight.grid(row = 13,column=1, columnspan = 3,sticky='w')
f3.SCalorie=Label(f3)
f3.SCalorie.grid(row = 14,column=1, columnspan = 3,sticky='w')
f3.SProtein=Label(f3)
f3.SProtein.grid(row = 15,column=1, columnspan = 3,sticky='w')

f3.btnCalc = Button(f3, text = "Calculate BMI",bg='#ffffff',command=lambda:calcBMI())
f3.btnCalc.grid(row = 10, columnspan = 5)

def calcBMI():
    """calculate the BMI of a person using the formula"""
    #calculate BMI
    feet = int(txtHeightFt.get())
    inches = int(txtHeightIn.get())
    totalHeight = (12 * feet) + inches
    weight = float(txtWeight.get())
    #BMI needs to be a float, int * float is float
    bmi = weight * 703 / (totalHeight * totalHeight)
    f3.lblBMI["text"] = "%.2f" % bmi


    #label for BMI status
    if bmi < 18.5:
    	f3.lblBMIStatus["text"] = "Underweight"
    	f3.SWeight["text"] = "Gain: 2 kg"
    	f3.SCalorie["text"] = "3000 Calorie if MALE, 2500 if FEMALE"
    	f3.SProtein["text"] = weight*0.48
    elif bmi < 24.9:
        f3.lblBMIStatus["text"] = "Normal"
        f3.SWeight["text"] = "Maintain"
        f3.SCalorie["text"] = "2500 Calorie if MALE, 2000 if FEMALE"
        f3.SProtein["text"] = weight*0.38
    elif bmi < 29.9:
        f3.lblBMIStatus["text"] = "Overweight"
        f3.SWeight["text"] = "Lose: 2 kg"
        f3.SCalorie["text"] = "2000 Calorie if MALE, 1500 if FEMALE"
        f3.SProtein["text"] = weight*0.48
    else:
        f3.lblBMIStatus["text"] = "Obese"
        f3.SWeight["text"] = "Lose: 4 kg"
        f3.SCalorie["text"] = "1600 Calorie if MALE, 1200 if FEMALE"
        f3.SProtein["text"] = weight*0.48
#f3.btnCalc["command"] = f3.calcBMI

############ F3

############ F4
Label(f4, text = "Triglycerides", bg='#fc0015').grid(row = 0,sticky='e,w',column=0)
Triglycerides = Entry(f4)
Triglycerides.grid(row = 2,sticky='e,w',column=0)
Triglycerides.insert(0, "0")
Label(f4, text = "Total Cholesterol", bg='#fc0015').grid(row = 3,sticky='e,w',column=0)
Cholesterol = Entry(f4)
Cholesterol.grid(row = 4,sticky='e,w',column=0)
Cholesterol.insert(0, "0")
Label(f4, text = "Hemoglobin", bg='#fc0015').grid(row = 5,sticky='e,w',column=0)
Hemoglobin = Entry(f4)
Hemoglobin.grid(row = 6,sticky='e,w',column=0)
Hemoglobin.insert(0, "0")
Label(f4, text = "White blood cells (WBC)", bg='#fc0015').grid(row = 7,sticky='e,w',column=0)
Label(f4, text = "____________________________________________________________________________________", bg='#fc0015').grid(row = 10,sticky='e,w',column=0)
WBC = Entry(f4)
WBC.grid(row = 8,sticky='e,w',column=0)
WBC.insert(0, "0")
Button(f4, text = "Enter",command=lambda:norms()).grid(row=9,column=0)

def norms():
    if int(Triglycerides.get()) < 50:
        Triglycerides.delete(0,END)
        Triglycerides.insert(0,'LOW')
  
    elif int(Triglycerides.get()) < 150:
        Triglycerides.delete(0,END)
        Triglycerides.insert(0,'NORMAL')
  
    elif int(Triglycerides.get()) > 150:
        Cholesterol.delete(0,END)
        Cholesterol.insert(0,'HIGH')

    if int(Cholesterol.get()) < 3:
        Cholesterol.delete(0,END)
        Cholesterol.insert(0,'LOW')
  
    elif int(Cholesterol.get()) < 5.5:
        Cholesterol.delete(0,END)
        Cholesterol.insert(0,'NORMAL')
  
    elif int(Cholesterol.get()) > 5.5:
        Cholesterol.delete(0,END)
        Cholesterol.insert(0,'HIGH')

    if int(Hemoglobin.get()) < 12:
        Hemoglobin.delete(0,END)
        Hemoglobin.insert(0,'LOW')
  
    elif int(Hemoglobin.get()) < 15:
        Hemoglobin.delete(0,END)
        Hemoglobin.insert(0,'NORMAL')
  
    elif int(Hemoglobin.get()) > 15:
        Hemoglobin.delete(0,END)
        Hemoglobin.insert(0,'HIGH')

    if int(WBC.get()) < 4:
        WBC.delete(0,END)
        WBC.insert(0,'LOW')
  
    elif int(WBC.get()) < 10:
        WBC.delete(0,END)
        WBC.insert(0,'NORMAL')
  
    elif int(WBC.get()) > 10:
        WBC.delete(0,END)
        WBC.insert(0,'HIGH')
############ F4

raise_frame(f1)
root.minsize(420,300)
icon = PhotoImage(file= r'C:\Users\admin\Desktop\python proj\learning\favicon.ico')
root.tk.call('wm','iconphoto',root._w,icon)
#f3.configure(background='#e20008')
root.mainloop()