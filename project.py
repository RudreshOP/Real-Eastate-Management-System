from tkinter import *
from tkinter import messagebox
import re, pymysql
import pandas as pd
import numpy as np
from PIL import ImageTk,Image
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar, DateEntry
from tkinter.ttk import Combobox
if sys.version_info[0] < 3:
    import Tkinter as sk
else:
    import tkinter as sk


df=pd.read_excel(r'C:\Users\Rudresh\Desktop\Datasetproperty.xlsx',skiprows=7)
headers=df.iloc[0]
global df1
df1=pd.DataFrame(df.values[1:],columns=headers)
for index, row in df1.iterrows():
    if row['UoM']=='HA':
        row['Area']=row['Area']*10000
df1['UoM'].replace(to_replace='HA', value='SQ-M', inplace=True)
df1['Agent'] =df1['Agent'].str.replace('\xa0 \xa0\xa0','') #REMOVING UNNECESSARY CHARACTERS
df1['Agent'] =df1['Agent'].str.replace(' ','')
df1.dropna(subset=['City','Address','Area','Agent'],inplace=True)





   
def viewpoint():
    global screen30
    screen30 = Toplevel(screen)
    screen30.title("VIEWPOINT")
    adjustWindow(screen30)
    con=pd.DataFrame(df1.groupby(['Country','Agent'])['Area'].sum())
    con.reset_index(inplace=True)
    con.set_index('Agent',inplace=True)
    ca_agents=con[con['Country']=='CA']
    ws_agents=con[con['Country']=='WS']
    f = Figure(figsize=(4,4), dpi=100)
    ax1 = f.add_subplot(1,2,1)
    ax2= f.add_subplot(1,2,2)
    width = .5
    rects1 = ax1.bar(ca_agents.index,ca_agents['Area'])
    rects2 = ax2.bar(ws_agents.index,ws_agents['Area'])
    ax1.set_xticklabels(ca_agents.index,rotation=40,horizontalalignment='right',fontsize='11')
    ax2.set_xticklabels(ws_agents.index,rotation=40,horizontalalignment='right',fontsize='11')
    ax1.set_title("AGENTS IN CA",fontsize='22')
    ax2.set_title("AGENTS IN WS",fontsize='22')
    canvas = FigureCanvasTkAgg(f, master=screen30)
    #canvas.show()
    canvas.get_tk_widget().pack(side=sk.TOP, fill=sk.BOTH, expand=1)
    Label(screen30, text='AS THERE ARE ONLY 4 AGENTS WORKING IN WS COUNTRY THE BUSINESS IS MUCH MORE LESS AS COMPARED TO CA.SO IF MORE AGENTS WORK IN WS LIKE IN CA THE BUSINESS IN',font=("Open Sans", 12, 'bold'),fg='white', bg='#174873').place(x=10,y=10)
    Label(screen30, text='WS CAN IMPROVE',font=("Open Sans", 12, 'bold'),fg='white', bg='#174873').place(x=10,y=40)
  #  messagebox.showinfo("VIEWPOINT","AS THERE ARE ONLY 4 AGENTS WORKING IN WS COUNTRY THE BUSINESS IS MUCH MORE LESS AS COMPARED TO CA.SO IF MORE AGENTS WORK IN WS LIKE IN CA THE BUSINESS IN WS CAN IMPROVE")
 
   
def get_customer_code():
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT CUST_CODE FROM customer" ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    customer_record = cursor.fetchall()
    connection.commit()
    connection.close()
    m=max(customer_record)         
    m1=m[0]  
    m2=m1[1:]
    m3=int(m2)
    m4=m3+1
    x="C00"+ str(m4)
    return x


def get_company_id():
    connection = pymysql.connect(host="localhost",port = 3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT COMPANY_ID FROM company" ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    company_record = cursor.fetchall()
    connection.commit()
    connection.close()
    m=(company_record[-1])
    m1=m[0]  
    m2=int(m1)
    m3=m2+1
    x=str(m3)
    return(x)


def get_agent_code():
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT AGENT_CODE FROM agents" ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    agent_record = cursor.fetchall()
    connection.commit()
    connection.close()
    m=max(agent_record)
    m1=m[0]  
    m2=m1[1:]           
    m3=int(m2)
    m4=m3+1
    x="A0"+ str(m4)
    return x


def get_order_no():
    connection = pymysql.connect(host="localhost",port = 3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT ORD_NUM FROM orders" ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    order_record = cursor.fetchall()
    connection.commit()
    connection.close()
    m=max(order_record)  
    m1=m[0]  
    m2=int(m1)
    m3=m2+1
    return m3


def advance_amount_validation():
    if (order_amount.get() > advance_amount.get()):
        return True
    else:
        return False


def amount_validation(amount):
    if (re.match('^[0-9]+$',amount)):
        return True
    else:
        return False
    

def company_id_validation(company_id):
    connection = pymysql.connect(host="localhost",port = 3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT COMPANY_ID FROM company " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    company_record = cursor.fetchall()
    connection.commit() # commiting the connection then closing it.
    connection.close()
    ids=list(company_record)
    if company_id in ids:
        return False
    else:
        return True
   
def customer_code_validation(customer_code):
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT CUST_CODE FROM customer" ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    customer_record = cursor.fetchall()
    connection.commit()
    connection.close()
    if len(customer_record)>0:
        for i in range (len(customer_record)):
            if (customer_code in customer_record[i][0]):
                return True
    else:
        return False
   
   
def agent_code_validation(agent_code):
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT AGENT_CODE FROM agents " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    agent_record = cursor.fetchall()
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if len(agent_record) > 0:
        for i in range(len(agent_record)):
            if (agent_code in agent_record[i][0]):
                return True
    else:
        return False

def is_valid_phone(agent_phone):
    if (re.match('(\d{3})\D*(\d{8})\D*(\d*)$',agent_phone)):
         return True
    else:
         return False

# This function is used for adjusting window size and making the necessary configuration on start of window
def adjustWindow(window):
 w = 600 # width for the window size
 h = 600 # height for the window size
 ws = screen.winfo_screenwidth() # width of the screen
 hs = screen.winfo_screenheight() # height of the screen
 x = (ws/2) - (w/2) # calculate x and y coordinates for the Tk window
 y = (hs/2) - (h/2)
 window.geometry('%dx%d+%d+%d' % (ws, hs, 0, 0)) # set the dimensions of the screen and where it is placed
 window.resizable(True, True) # disabling the resize option for the window
 window.configure(background='#dfe6e9') # making the background white of the window
 
 


def func1():
    global screen34
    order_date=year.get()+'-'+month.get()+'-'+date.get()
    con=pymysql.connect(host="localhost",port=3308,user="root",password="",database="project")
    cursorObj=con.cursor()
    select_query="SELECT ORD_NUM,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_DATE,CUST_CODE,AGENT_CODE,ORD_DESCRIPTION FROM orders where orders.ORD_DATE=%s"";"
    cursorObj.execute(select_query,order_date)
    orders=cursorObj.fetchall()        
    cust_code=customer_code_verify.get()
    order_num=int(order_number_verify.get())
    con.commit()
    con.close()
    if len(orders)>0:
        for i in range(len(orders)):
            if cust_code in orders[i][4]:
                if order_num == orders[i][0]:
                    screen34=Toplevel(screen)
                    adjustWindow(screen34)
                    Label(screen34, text="ORDERS", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
                    Label(screen34,text="ORDER NUMBER",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=0)
                    Label(screen34,text="ORDER AMOUNT",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=1)
                    Label(screen34,text="ADVANCE AMOUNT",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=2)
                    Label(screen34,text="ORDER DATE",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=3)
                    Label(screen34,text="CUSTOMER CODE",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=4)
                    Label(screen34,text="AGENT CODE",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=5)
                    Label(screen34,text="ORDER DESCRIPTION",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=6)
                    Label(screen34,text=orders[i][0],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=0)
                    Label(screen34,text=orders[i][1],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=1)
                    Label(screen34,text=orders[i][2],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=2)
                    Label(screen34,text=orders[i][3],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=3)
                    Label(screen34,text=orders[i][4],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=4)
                    Label(screen34,text=orders[i][5],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=5)
                    Label(screen34,text=orders[i][6],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=6)
        Button(screen34, text='Back->',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen34.destroy).place(x=600,y=550)

    else:
        messagebox.showerror('Error','Invalid Choice')            
                
def func2():
    #global screen34
    con=pymysql.connect(host="localhost",port=3308,user="root",password="",database="project")
    cursorObj=con.cursor()
    select_query="SELECT ORD_NUM,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_DATE,CUST_CODE,AGENT_CODE,ORD_DESCRIPTION FROM orders where orders.ORD_NUM=" +str(order_number_verify.get())+";"
    cursorObj.execute(select_query)
    orders=cursorObj.fetchall()
    con.commit()
    con.close()
    if len(orders)>0:
        screen34=Toplevel(screen)
        adjustWindow(screen34)
        Label(screen34, text="ORDERS", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
        Label(screen34,text="ORDER NUMBER",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=0)
        Label(screen34,text="ORDER AMOUNT",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=1)
        Label(screen34,text="ADVANCE AMOUNT",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=2)
        Label(screen34,text="ORDER DATE",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=3)
        Label(screen34,text="CUSTOMER CODE",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=4)
        Label(screen34,text="AGENT CODE",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=5)
        Label(screen34,text="ORDER DESCRIPTION",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=6)
        for i in range(len(orders)):
            Label(screen34,text=orders[i][0],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=0)
            Label(screen34,text=orders[i][1],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=1)
            Label(screen34,text=orders[i][2],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=2)
            Label(screen34,text=orders[i][3],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=3)
            Label(screen34,text=orders[i][4],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=4)
            Label(screen34,text=orders[i][5],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=5)
            Label(screen34,text=orders[i][6],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=6)
        Button(screen34, text='Back->',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen34.destroy).place(x=600,y=550)
    else:
        messagebox.showerror('Empty','No Orders Available')         

def func3():
    con=pymysql.connect(host="localhost",port=3308,user="root",password="",database="project")
    cursorObj=con.cursor()
    select_query="SELECT ORD_NUM,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_DATE,CUST_CODE,AGENT_CODE,ORD_DESCRIPTION FROM orders where orders.CUST_CODE= %s"";"
    cursorObj.execute(select_query,customer_code_verify.get())
    orders=cursorObj.fetchall()
    con.commit()
    con.close()
    if len(orders)>0:
        screen34=Toplevel(screen)
        adjustWindow(screen34)
        Label(screen34, text="ORDERS", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
        Label(screen34,text="ORDER NUMBER",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=0)
        Label(screen34,text="ORDER AMOUNT",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=1)
        Label(screen34,text="ADVANCE AMOUNT",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=2)
        Label(screen34,text="ORDER DATE",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=3)
        Label(screen34,text="CUSTOMER CODE",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=4)
        Label(screen34,text="AGENT CODE",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=5)
        Label(screen34,text="ORDER DESCRIPTION",font=("Calibri", 14, 'bold'), fg='black',bg="#dfe6e9").grid(row=1,column=6)
        for i in range(len(orders)):
            Label(screen34,text=orders[i][0],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=0)
            Label(screen34,text=orders[i][1],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=1)
            Label(screen34,text=orders[i][2],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=2)
            Label(screen34,text=orders[i][3],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=3)
            Label(screen34,text=orders[i][4],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=4)
            Label(screen34,text=orders[i][5],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=5)
            Label(screen34,text=orders[i][6],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=6)
        
        Button(screen34, text='Back->',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen34.destroy).place(x=600,y=550)
    else:
        messagebox.showerror('Empty','No Orders Available')  

def func4():
    #global screen34
    order_date=year.get()+'-'+month.get()+'-'+date.get()
    #screen34=Toplevel(screen)
    #adjustWindow(screen34)
    con=pymysql.connect(host="localhost",port=3308,user="root",password="",database="project")
    cursorObj=con.cursor()
    select_query="SELECT ORD_NUM,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_DATE,CUST_CODE,AGENT_CODE,ORD_DESCRIPTION FROM orders where orders.ORD_DATE=%s"";"
    cursorObj.execute(select_query,order_date)
    orders=cursorObj.fetchall()
    con.commit()
    con.close()
    if len(orders)>0:
        screen34=Toplevel(screen)
        adjustWindow(screen34)
        Label(screen34, text="ORDERS", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="white").grid(row=0,sticky="N",columnspan=17)
        Label(screen34,text="ORDER NUMBER",font=("Calibri", 14, 'bold'), fg='black',bg="white").grid(row=1,column=0)
        Label(screen34,text="ORDER AMOUNT",font=("Calibri", 14, 'bold'), fg='black',bg="white").grid(row=1,column=1)
        Label(screen34,text="ADVANCE AMOUNT",font=("Calibri", 14, 'bold'), fg='black',bg="white").grid(row=1,column=2)
        Label(screen34,text="ORDER DATE",font=("Calibri", 14, 'bold'), fg='black',bg="white").grid(row=1,column=3)
        Label(screen34,text="CUSTOMER CODE",font=("Calibri", 14, 'bold'), fg='black',bg="white").grid(row=1,column=4)
        Label(screen34,text="AGENT CODE",font=("Calibri", 14, 'bold'), fg='black',bg="white").grid(row=1,column=5)
        Label(screen34,text="ORDER DESCRIPTION",font=("Calibri", 14, 'bold'), fg='black',bg="white").grid(row=1,column=6)
        for i in range(len(orders)):
            Label(screen34,text=orders[i][0],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=0)
            Label(screen34,text=orders[i][1],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=1)
            Label(screen34,text=orders[i][2],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=2)
            Label(screen34,text=orders[i][3],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=3)
            Label(screen34,text=orders[i][4],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=4)
            Label(screen34,text=orders[i][5],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=5)
            Label(screen34,text=orders[i][6],font=("Calibri", 14, 'bold'),fg='black',bg="#dfe6e9").grid(row=2+i,column=6)
        Button(screen34, text='Back->',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen34.destroy).place(x=600,y=550)
    else:
        messagebox.showerror('Empty','No Orders Available')  
 
 
def search_order():
    order_date=year.get()+'-'+month.get()+'-'+date.get()
    ord_num=order_number_verify.get()
    cust_num=customer_code_verify.get()
    if (ord_num and cust_num and order_date):
        func1()
    elif ord_num:
        func2()
    elif (customer_code_verify.get()):
        func3()
    elif (year.get() and month.get() and date.get()):
        func4()
 
def module2():
    global screen33,order_number_verify,date,year,month,customer_code_verify #global variables declared
    screen33 = Toplevel(screen)
    screen33.title("MODULE 2")
    adjustWindow(screen33)
    order_number_verify=StringVar() 
    date=StringVar()
    customer_code_verify=StringVar()
    screen33.title("SUNVILLE PROPERTIES") #title
    adjustWindow(screen33) #adjusting the screen size
    Label(screen33, text="SUNVILLE PROPERTIES", width="500", height="2",font=("Roboto", 22, 'bold'), fg='black', bg='#84DCC6').pack()
    Label(screen33,text='',bg="#dfe6e9").pack()
    Label(screen33, text="Enter Details",width='500', height="2",font=("Roboto", 22, 'bold'), fg='black',bg="#dfe6e9").pack() 
    Label(screen33,text='',bg="#dfe6e9").pack()
    Label(screen33, text="Enter the order number",font=("Roboto", 15, 'bold'), fg='black',bg="#dfe6e9").pack()
    Entry(screen33,textvariable=order_number_verify).pack() 
    Label(screen33,text='',bg="#dfe6e9").pack()
    order_number_verify.set("")
    Label(screen33, text="Enter the order date",font=("Roboto", 15, 'bold'), fg='black',bg="#dfe6e9").pack()
    year= StringVar() 
    choices= list(range(2005,2020))
    Label(screen33,text='',bg="#dfe6e9").pack()
    Combobox(screen33, width=5, values = choices ,textvariable = year).pack()
    month= StringVar() 
    choices= list(range(1,13)) 
    Label(screen33,text='',bg="#dfe6e9").pack()
    Combobox(screen33, width=5, values = choices ,textvariable = month).pack()
    date= StringVar() 
    choices= list(range(1,32)) 
    Label(screen33,text='',bg="#dfe6e9").pack()
    Combobox(screen33, width=5, values = choices ,textvariable = date).pack()
    Label(screen33,text='',bg="#dfe6e9").pack()
    Label(screen33, text="Enter the customer code",font=("Roboto", 15, 'bold'), fg='black',bg="#dfe6e9").pack()
    Entry(screen33,textvariable=customer_code_verify).pack() 
    customer_code_verify.set("")
    Label(screen33,text='',bg="#dfe6e9").pack()
    Label(screen33,text='',bg="#dfe6e9").pack()
    Button(screen33,text="Search", width=15,font=("Open Sans", 15, 'bold'),fg='white', bg='#2159ff',command=search_order).pack() 
    Label(screen33,text='',bg="#dfe6e9").pack()
    Label(screen33,text='',bg="#dfe6e9").pack()
    Button(screen33, text='Back->',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen33.destroy).pack()


def time_series():

    global screen32

    screen32 = Toplevel(screen)

    screen32.title("Time series for Area leased or owned")

    Label(screen32, text="",width='500', height='50').place(x=0, y=70)

    Label(screen32, text="Time series for Area leased and owned", width="500", height="2",font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").pack()

    adjustWindow(screen32)

    q7a = dict(df1.groupby('Year').count()['Prov'])

    q7ad = pd.DataFrame({'Year':list(q7a.keys()),'Number of orders':list(q7a.values())})

    figure = Figure(figsize=(10,6.1), dpi=100)

    ax = figure.add_subplot(111)
    

    chart_type = FigureCanvasTkAgg(figure, screen32)

    chart_type.get_tk_widget().pack()

    q7ad.plot(ax=ax,x='Year')

    ax.set_ylabel("Number of orders")

    ax.set_title('Time series for Area leased or owned')
    Button(screen32, text='Back ->', width=12, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen32.destroy).place(x=670, y=720)
    

def piechart_2017():
    global screen31
    screen31 = Toplevel(screen)
    screen31.title("2017")
    adjustWindow(screen31)
    labels = 'leased', 'Owned'
    sizes = [145403.87, 379589.8]
    f = Figure(figsize=(5,5), dpi=120)
    ax1 = f.add_subplot(1,2,1)
    explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
#    fig1, ax1 = plt.subplots()
    rects1 = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    #ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #plt.show()
    canvas = FigureCanvasTkAgg(f, master=screen31)
    canvas.get_tk_widget().pack(side=sk.TOP, fill=sk.BOTH, expand=1)
    Button(screen31, text='Back->',width=13, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen31.destroy).place(x=700,y=700)
    Label(screen31,text="Owned Area : ",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=10,y=30)
    Label(screen31,text="379589.8",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=170,y=30)
    Label(screen31,text="Leased Area: ",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=350,y=30)
    Label(screen31,text="145403.87",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=510,y=30)
   

def piechart_2018():
    global screen31
    screen31 = Toplevel(screen)
    screen31.title("2018")
    adjustWindow(screen31)
    labels = 'leased', 'Owned'
    sizes = [272277.96, 486892.37]
    f = Figure(figsize=(5,5), dpi=120)
    ax1 = f.add_subplot(1,2,1)
    explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    #fig1, ax1 = plt.subplots()
    rects1 = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
   # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #plt.show()
    canvas = FigureCanvasTkAgg(f, master=screen31)
    canvas.get_tk_widget().pack(side=sk.TOP, fill=sk.BOTH, expand=1)
    Button(screen31, text='Back->',width=13, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen31.destroy).place(x=700,y=700)
    Label(screen31,text="Owned Area : ",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=10,y=30)
    Label(screen31,text="486892.37",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=170,y=30)
    Label(screen31,text="Leased Area: ",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=350,y=30)
    Label(screen31,text="272277.96",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=510,y=30)
   
   
def piechart_2019():
    global screen31
    screen31 = Toplevel(screen)
    screen31.title("2019")
    adjustWindow(screen31)
    labels = 'leased', 'Owned'
    sizes = [909204.88,4348387.99]
    f = Figure(figsize=(5,5), dpi=120)
    ax1 = f.add_subplot(1,2,1)
    explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    #fig1, ax1 = plt.subplots()
    rects1 = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    #ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #plt.show()
    canvas = FigureCanvasTkAgg(f, master=screen31)
    canvas.get_tk_widget().pack(side=sk.TOP, fill=sk.BOTH, expand=1)
    Button(screen31, text='Back->',width=13, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen31.destroy).place(x=700,y=700)
    Label(screen31,text="Owned Area : ",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=10,y=30)
    Label(screen31,text="4348387.99",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=170,y=30)
    Label(screen31,text="Leased Area: ",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=350,y=30)
    Label(screen31,text="909204",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=510,y=30)
   
   
def piechart_2020():
    global screen31
    screen31 = Toplevel(screen)
    screen31.title("2020")
    adjustWindow(screen31)
    labels = 'leased', 'Owned'
    sizes = [118124.63,414104.24]
    f = Figure(figsize=(5,5), dpi=120)
    ax1 = f.add_subplot(1,2,1)
    explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    #fig1, ax1 = plt.subplots()
    rects1 = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    #ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #plt.show()
    canvas = FigureCanvasTkAgg(f, master=screen31)
    canvas.get_tk_widget().pack(side=sk.TOP, fill=sk.BOTH, expand=1)
    Button(screen31, text='Back->',width=13, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen31.destroy).place(x=700,y=700)
    Label(screen31,text="Owned Area : ",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=10,y=30)
    Label(screen31,text="414104",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=170,y=30)
    Label(screen31,text="Leased Area: ",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=350,y=30)
    Label(screen31,text="118124",font=("Open Sans", 15, 'bold'),bg="#dfe6e9").place(x=510,y=30)
   
def ans_a():
    global screen18
    screen18 = Toplevel(screen)
    screen18.title("ANSWER 1")
    adjustWindow(screen18)
    year=[2017,2018,2019,2020]
    owned_a=[379589.8,486892.37,4348387.99,414104.24]
    leased_a=[145403.87,272277.96,909204.88,118124.63]
   
       # Button(screen18, text='Back-->',width=15, font=("Open Sans", 15, 'bold'),fg='white', bg='#174873',command=screen18.destroy).place(x=570,y=650)
    Button(screen18, text='2017',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#E0ACD5',command=piechart_2017).place(x=200,y=200)
    Button(screen18, text='2018',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#E0ACD5',command=piechart_2018).place(x=400,y=200)
    Button(screen18, text='2019',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#E0ACD5',command=piechart_2019).place(x=600,y=200)
    Button(screen18, text='2020',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#E0ACD5',command=piechart_2020).place(x=800,y=200)
    Button(screen18, text='Back->',width=15, font=("Open Sans", 15, 'bold'),fg='black', bg='#84DCC6',command=screen18.destroy).place(x=700,y=700)

     

       
def ans_b():
    global screen26
    #year = StringVar()
    screen26 = Toplevel(screen)
    screen26.title("ANSWER 1")
    adjustWindow(screen26)
    li=[2017,2018,2019]
    max_leased_ca=[]
    for i in li:
        df3=df1[df1['Year']==i]
        df4=df3[(df3['Country']=='CA') & (df3['Tenure']=='Leased')]
        max_leased_ca.append(sum(df4['Area']))
    max_leased_ws=[]
    
    for i in li:
        df3=df1[df1['Year']==i]
        df4=df3[(df3['Country']=='WS') & (df3['Tenure']=='Leased')]
        max_leased_ws.append(sum(df4['Area']))
       
    f = Figure(figsize=(5,5), dpi=120)
    ax1 = f.add_subplot(1,2,1)
    ax2= f.add_subplot(1,2,2)
    width = .5
    rects1 = ax1.bar(li, max_leased_ca, width)
    rects2 = ax2.bar(li, max_leased_ws, width)
    ax1.set_title("CA AREA",fontsize='28')
    ax2.set_title("WS AREA",fontsize='28')
    canvas = FigureCanvasTkAgg(f, master=screen26)
    #canvas.show()
    canvas.get_tk_widget().pack(side=sk.TOP, fill=sk.BOTH, expand=1)
    Label(screen26, text='2019 GOT MAXIMUM LEASED AREA IN CA AND WS COUNTRIES',font=("Roboto", 15, 'bold'),fg='black',bg="#dfe6e9").place(x=500,y=10)
   

def ans_c():
    global screen9,ans_c_agent
    screen9 = Toplevel(screen)
    screen9.title("Welcome")
    adjustWindow(screen9)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT AGENT_CODE,AGENT_NAME FROM agents " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    agent_record_c = cursor.fetchall()
    connection.commit() # commiting the connection then closing it.
    connection.close()
    ans_c=df1[df1['Tenure']=='Owned']
    ans_c_agent=ans_c['Agent'].unique()
    Label(screen9,text='Agent Name',font=("Open Sans", 11, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=3,pady=(5,10))
    Label(screen9,text='Agent Code',font=("Open Sans", 11, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=4,pady=(5,10))

    for i in range(len(ans_c_agent)):
        for j in range(len(agent_record_c)):
            if (ans_c_agent[i] in agent_record_c[j][1]):
                Label(screen9,text=ans_c_agent[i],font=("Open Sans", 11, 'bold'),fg='black', bg="#dfe6e9").grid(row=i+4,column=3,pady=(5,10))
                Label(screen9,text=agent_record_c[j][0],font=("Open Sans", 11, 'bold'),fg='black', bg="#dfe6e9").grid(row=i+4,column=4,pady=(5,10))
    Button(screen9, text='Back ->', width=13, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen9.destroy).place(x=170, y=565) # button to navigate back to login page
             
def ans_d():
    global screen29
    screen29 = Toplevel(screen)
    screen29.title("MAXIMUM DEALS IN LEASED FORM IN CHILLIWACK")
    adjustWindow(screen29)
    chilwalk=df1[(df1['City']=='Chilliwack') & (df1['Tenure']=='Leased')]
    ans_d=chilwalk['Agent'].value_counts()
    f = Figure(figsize=(5,5), dpi=120)
    ax = f.add_subplot(111)
    width = .5
    rects1 = ax.bar(ans_d.index, ans_d.values, width)
    canvas = FigureCanvasTkAgg(f, master=screen29)
    #canvas.show()
    canvas.get_tk_widget().pack(side=sk.TOP, fill=sk.BOTH, expand=1)
    Label(screen29, text=ans_d.idxmax(),font=("Open Sans", 15, 'bold'),fg='black', bg='white').place(x=500,y=10)
    Label(screen29, text='got highest number of deals in Chilliwack i.e 7',font=("Open Sans", 15, 'bold'),fg='black', bg='white').place(x=560,y=10)

def ans_e():
    global screen27
    screen27 = Toplevel(screen)
    screen27.title("BEST PERFORMER")
    adjustWindow(screen27)
    ans_e=df1.groupby(['Agent','Tenure'])['Area'].sum()
    df_ans_e=pd.DataFrame(ans_e)
    df_ans_e.reset_index(inplace=True)

    df_ans_e_leased=df_ans_e[df_ans_e['Tenure']=='Leased']
    df_ans_e_owned=df_ans_e[df_ans_e['Tenure']=='Owned']
   
    f = Figure(figsize=(4,4), dpi=100)
    ax1 = f.add_subplot(1,2,1)
    ax2= f.add_subplot(1,2,2)
    width = .5
    rects1 = ax1.bar(df_ans_e_leased.groupby('Agent')['Area'].sum().index,df_ans_e_leased.groupby('Agent')['Area'].sum())
    rects2 = ax2.bar(df_ans_e_owned.groupby('Agent')['Area'].sum().index,df_ans_e_owned.groupby('Agent')['Area'].sum())
    ax1.set_xticklabels(df_ans_e_leased.groupby('Agent')['Area'].sum().index,rotation=20,horizontalalignment='right',fontsize='9')
    ax2.set_xticklabels(df_ans_e_owned.groupby('Agent')['Area'].sum().index,rotation=20,horizontalalignment='right',fontsize='9')
    ax1.set_title("LEASED AREA",fontsize='28')
    ax2.set_title("OWNED AREA",fontsize='28')
    canvas = FigureCanvasTkAgg(f, master=screen27)
    #canvas.show()
    canvas.get_tk_widget().pack(side=sk.TOP, fill=sk.BOTH, expand=1)
    Label(screen27, text='MUKESH IS THE BEST PERFORMER AS HE IS CONSISTENT IN BOTH THE CATEGORIES',font=("Open Sans", 12, 'bold'),fg='black', bg="#dfe6e9").place(x=10,y=10)
   
def ans_f():
    global screen28
    screen28 = Toplevel(screen)
    screen28.title("AMOUNT OF PROPERTY SOLD FOR THE MONTH OF JULY")
    adjustWindow(screen28)
    year=df1['Year'].unique()
    ans=df1.groupby('Year')['Area'].sum()  
 

    f = Figure(figsize=(5,5), dpi=120)
    ax = f.add_subplot(111)
    width = .5
    rects1 = ax.bar([2017,2018,2019,2020], ans, width)
    canvas = FigureCanvasTkAgg(f, master=screen28)

    canvas.get_tk_widget().pack(side=sk.TOP, fill=sk.BOTH, expand=1)
    val=np.round(ans.values,2)
    Label(screen28, text=ans.index[0],font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").place(x=400,y=10)
    Label(screen28, text=val[0],font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").place(x=460,y=10)
    Label(screen28, text=ans.index[1],font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").place(x=590,y=10)
    Label(screen28, text=val[1],font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").place(x=650,y=10)
    Label(screen28, text=ans.index[2],font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").place(x=790,y=10)
    Label(screen28, text=val[2],font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").place(x=850,y=10)
    Label(screen28, text=ans.index[3],font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").place(x=1010,y=10)
    Label(screen28, text=val[3],font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").place(x=1075,y=10)
   

def country():
    connection = pymysql.connect(host="localhost",port=3308, user="root", passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT CUST_COUNTRY,COUNT(*) as count FROM customer GROUP BY CUST_COUNTRY ORDER BY count DESC "
    cursor.execute(select_query)
    country_name = cursor.fetchone()
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    Label(screen17, text="Country and their total registration: ",font=("Roboto", 15, 'bold'),fg='black',bg="#dfe6e9").place(x=550,y=200)
    Label(screen17, text=country_name, font=("Roboto", 15, 'bold'), fg='black',bg="#dfe6e9").place(x=900,y=200)
         
def payment_amount():
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT SUM(PAYMENT_AMT) FROM customer WHERE CUST_COUNTRY='India'  "
    cursor.execute(select_query)
    payment_amt = cursor.fetchone()
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    Label(screen17, text="Payment Amount is: ",font=("Roboto", 15, 'bold'),fg='black',bg="#dfe6e9").place(x=550,y=300)
    Label(screen17, text=payment_amt, font=("Roboto", 15, 'bold'), fg='black',bg="#dfe6e9").place(x=765,y=300)

def outstanding_amount():
    connection = pymysql.connect(host="localhost",port=3308, user="root", passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT SUM(OUTSTANDING_AMT) FROM customer WHERE CUST_COUNTRY='India'  "
    cursor.execute(select_query)
    outstanding_amt = cursor.fetchone()
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    Label(screen17, text="Outstanding Amount is: ",font=("Roboto", 15, 'bold'),fg='black',bg="#dfe6e9").place(x=550,y=400)
    Label(screen17, text=outstanding_amt, font=("Roboto", 15, 'bold'),fg='black',bg="#dfe6e9").place(x=800,y=400)

def module4():
    global screen17
    screen17 = Toplevel(screen)
    screen17.title("Welcome")
    adjustWindow(screen17)
    Button(screen17, text="Click here to find the most number of registered countries and count", bg="#E0ACD5", width=60, height=1, font=("Roboto", 13, 'bold'), fg='black',command=country).pack()
    Label(screen17, text="",bg="#dfe6e9").pack()
    Button(screen17, text="Click here to find the collective payment amount ", bg="#E0ACD5", width=60, height=1, font=("Roboto", 13, 'bold'), fg='black',command=payment_amount).pack()
    Label(screen17, text="",bg="#dfe6e9").pack()
    Button(screen17, text="Click here to find the collective outstanding amount ", bg="#E0ACD5", width=60, height=1, font=("Roboto", 13, 'bold'), fg='black',command=outstanding_amount).pack()
    Button(screen17, text='Back ->', width=15, font=("Open Sans",15,'bold'), bg='#84DCC6', fg='black',command=screen17.destroy).place(x=600, y=565) # button to navigate back to login page

def report_info():
    global screen24
    screen24=Tk()

    screen24.title("Report")
    adjustWindow(screen24)
    connection = pymysql.connect(host="localhost",port=3308,user="root" ,passwd="", database="project") # database connection
    cursor = connection.cursor()

    #query3="ALTER TABLE orders ADD BALANCE int(100)"
    #cursor.execute(query3)

    query4="UPDATE orders SET BALANCE=(ORD_AMOUNT-ADVANCE_AMOUNT)"
    cursor.execute(query4)

    query5="SELECT orders.ORD_NUM,orders.AGENT_CODE,agents.AGENT_NAME,orders.BALANCE FROM orders INNER JOIN agents ON orders.AGENT_CODE = agents.AGENT_CODE ORDER BY BALANCE DESC LIMIT 0,25"
    cursor.execute(query5)

    table=cursor.fetchall()
    #print(table)
    res3= str(''.join(map(str,table)))
    connection.commit() # commiting the connection then closing it.
    connection.close()

    Label(screen24,text="ORDER NUMBER ",font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=0)
    Label(screen24,text="AGENT CODE ",font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=1)
    Label(screen24,text="AGENT NAME ",font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=2)
    Label(screen24,text="BALANCE AMOUNT",font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=3)


    i=1
    cols=['ORD_NUM','AGENT_CODE','AGENTS_NAME','BALANCE AMOUNT']

    for i in range(len(table)):
        for j in range(len(cols)):
            Label(screen24,text=table[i][j],font=("Calibri", 14, 'bold'),fg='black', bg="#dfe6e9").grid(row=i+1,column=j)

    Button(screen24, text='Next', width=15, font=("Open Sans", 15,'bold'), bg='#173aa3', fg='white',command=report2).place(x=1150, y=590)
    Button(screen24, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen24.destroy).place(x=950, y=590)


def report2():
    global screen25
    screen25=Tk()
    screen25.title("Report")
    adjustWindow(screen25)
    connection = pymysql.connect(host="localhost",port=3308,user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()


    query6= " SELECT orders.ORD_NUM,orders.AGENT_CODE,agents.AGENT_NAME,orders.BALANCE FROM orders INNER JOIN agents ON orders.AGENT_CODE = agents.AGENT_CODE ORDER BY BALANCE DESC LIMIT 25,36"

    cursor.execute(query6)
    table1=cursor.fetchall()
    res4=str(''.join(map(str,table1)))

   # print(table1)

    connection.commit() # commiting the connection then closing it.
    connection.close()


    Label(screen25,text="ORDER NUMBER ",font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=0)
    Label(screen25,text="AGENT CODE ",font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=1)
    Label(screen25,text="AGENT NAME ",font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=2)
    Label(screen25,text="BALANCE AMOUNT",font=("Open Sans", 15, 'bold'),fg='black', bg="#dfe6e9").grid(row=0,column=3)

    cols=['ORD_NUM','AGENT_CODE','AGENTS_NAME','BALANCE AMOUNT']
    for i in range(len(table1)):
        for j in range(len(cols)):
            Label(screen25,text=table1[i][j],font=("Calibri", 14, 'bold'),fg='black', bg="#dfe6e9").grid(row=i+1,column=j)
    Button(screen25, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen25.destroy).place(x=950, y=590)



def company_insights():
    global screen8
    screen8 = Toplevel(screen)
    screen8.title("Welcome")
    adjustWindow(screen8) # configuring the window

    Button(screen8, text='PROPERTY AREA SOLD VS LEASED', width=120, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=ans_a).pack()
    Label(screen8, text="",bg="#dfe6e9").pack()
    Button(screen8, text='YEAR WHICH GOT MAX LEASED AREA IN CA AND WS COUNTRIES', width=120, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=ans_b).pack()
    Label(screen8, text="",bg="#dfe6e9").pack()
    Button(screen8, text='AGENT CODES WHO GOT DEALS IN OWNED CATEGORY', width=120, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=ans_c).pack()
    Label(screen8, text="",bg="#dfe6e9").pack()
    Button(screen8, text='MAXIMUM DEALS IN LEASED FORM IN CHILLIWALK', width=120, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=ans_d).pack()
    Label(screen8, text="",bg="#dfe6e9").pack()
    Button(screen8, text='BEST PERFORMER', width=120, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=ans_e).pack()
    Label(screen8, text="",bg="#dfe6e9").pack()
    Button(screen8, text='PROPERTY SOLD IN JULY IN ALL YEARS', width=120, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=ans_f).pack()
    Label(screen8, text="",bg="#dfe6e9").pack()
    Button(screen8, text='TIME SERIES ANALYSIS', width=120, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=time_series).pack()
    Label(screen8, text="",bg="#dfe6e9").pack()
    Button(screen8, text='Back ->', width=12, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen8.destroy).place(x=670, y=665) # button to navigate back to login page
   


def agent_validation():
 global agent_code
 agent_code=get_agent_code()  
 if agent_name.get() and commission.get() and working_area.get() and agent_phone.get() and agent_country.get(): # checking for all empty values in entry field
       #  if agent_code.get(): # checking for Agent code
             if (re.match("^[A-Za-z]*$",agent_name.get())):# Check for Agent Name
                 if(re.match('^(?:[1-9]\d*|0)?(?:\.\d+)?$', commission.get())):
                     if(re.match('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', working_area.get())):
                         if is_valid_phone(agent_phone.get()):
                             if(re.match('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', agent_country.get())):
                                 # if u enter in this block everything is fine just enter the values in database
                                 connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection                                
                                 cursor = connection.cursor()
                                 insert_query = "INSERT INTO agents (AGENT_CODE, AGENT_NAME, WORKING_AREA, COMMISSION, PHONE_NO, COUNTRY) VALUES('"+ agent_code + "', '"+ agent_name.get() + "', '"+ working_area.get() +"', '"+ commission.get() + "', '"+ agent_phone.get() + "' ,'" +agent_country.get()+"');" # queries for inserting values
                                 cursor.execute(insert_query) # executing the queries
                                 connection.commit() # commiting the connection then closing it.
                                 connection.close() # closing the connection of the database
                                 Label(screen5, text="Registration Sucess", fg="green", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) # printing successful registration message
                                 
                              #   Button(screen5, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='brown', fg='white',command=screen5.destroy).place(x=170, y=565) # button to navigate back to login page
                             else:
                              Label(screen5, text="Country Name Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                              return                            
                         else:
                             Label(screen5, text="Phone Number Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                             return                              
                     else:
                        Label(screen5, text="Working Area Invaild", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                        return
                 else:
                     Label(screen5, text="Commission Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                     return
             else:
                 Label(screen5, text="Please enter valid name", fg="red",font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                 return
    #     else:
     #        Label(screen5, text="Please enter Code", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
      #       return
               
 else:
     Label(screen5, text="Please fill all the details", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
     return


def company_validation():
    global company_id
    company_id=get_company_id()
    if  company_name.get() and company_city.get(): # checking for all empty values in entry field
             if (re.match("^[A-Za-z]*$",company_name.get())):# Check for Company Name
                 if(re.match('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', company_city.get())):
                     connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
                     cursor = connection.cursor()
                     insert_query = "INSERT INTO company (COMPANY_ID,COMPANY_NAME, COMPANY_CITY) VALUES('"+ company_id + "','"+ company_name.get() + "', '"+ company_city.get() +"');" # queries for inserting values
                     cursor.execute(insert_query) # executing the queries
                     connection.commit() # commiting the connection then closing it.
                     connection.close() # closing the connection of the database
                     Label(screen6, text="Registration Sucess", fg="green", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) # printing successful registration message
                  #   Button(screen6, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='brown', fg='white',command=screen6.destroy).place(x=170, y=565) # button to navigate back to login page
                 else:
                     Label(screen6, text="Enter Correct City Name", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
                     return
                             
             else:
                 Label(screen6, text="Company Name Invaild", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
      
    else:
     Label(screen6, text="Please fill all the details", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
     return

def customer_validation():
    global customer_code
    customer_code=get_customer_code()
    if customer_name.get() and customer_city.get() and customer_working_area.get() and customer_country.get() and customer_grade.get() and opening_amount.get() and receive_amount.get() and customer_payment_amount.get() and customer_outstanding_amount.get() and agent_code.get() and phone_no.get(): # checking for all empty values in entry field
      #   if customer_code.get(): # checking for Customer code
             if (re.match("^[A-Za-z]*$",customer_name.get())):# Check for Customer Name
                 if(re.match('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', customer_city.get())):
                     if(re.match('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', customer_working_area.get())):
                             if(re.match('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', customer_country.get())):
                                 if(re.match('^[0-9 .]+$',customer_grade.get())):
                                     if (amount_validation(opening_amount.get())):
                                         if (amount_validation(receive_amount.get())):
                                             if (amount_validation(customer_payment_amount.get())):
                                                 if (amount_validation(customer_outstanding_amount.get())):
                                                     if (is_valid_phone(phone_no.get())):
                                                         if agent_code_validation(agent_code.get()):
                                                                 # if u enter in this block everything is fine just enter the values in database
                                                                 connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
                                                                 cursor = connection.cursor()
                                                                 insert_query = "INSERT INTO customer (CUST_CODE, CUST_NAME, CUST_CITY, WORKING_AREA, CUST_COUNTRY, GRADE,OPENING_AMT,RECEIVE_AMT,PAYMENT_AMT,OUTSTANDING_AMT,PHONE_NO,AGENT_CODE) VALUES('"+ customer_code + "', '"+ customer_name.get() + "', '"+ customer_city.get() +"', '"+ customer_working_area.get() + "', '"+ customer_country.get() + "' ,'" +customer_grade.get()+"' ,'"+ opening_amount.get() + "', '"+ receive_amount.get() + "', '"+ customer_payment_amount.get() + "', '"+ customer_outstanding_amount.get() + "', '"+ phone_no.get() + "', '"+ agent_code.get() + "');" # queries for inserting values
                                                                 cursor.execute(insert_query) # executing the queries
                                                                 connection.commit() # commiting the connection then closing it.
                                                                 connection.close() # closing the connection of the database
                                                                 Label(screen14, text="Registration Sucess", fg="green", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) # printing successful registration message
                                                             #    Button(screen14, text='Back ->', width=20, font=("Open Sans", 9,'bold'), bg='brown', fg='white',command=screen14.destroy).place(x=170, y=565) # button to navigate back to login page
                                                         else:
                                                             Label(screen14, text="Agent Code Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                                                             return                            
                                                     else:
                                                         Label(screen14, text="Phone Number Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                                                         return                              
                                                 else:
                                                     Label(screen14, text="Outstanding Amount Invaild", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
                                                     return
                                             else:
                                                 Label(screen14, text="Payment Amount Invaild", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                                                 return
                                         else:
                                            Label(screen14, text="Receive Amount Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                                            return
                                     else:
                                         Label(screen14, text="Opening Amount Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                                         return
                                 else:
                                     Label(screen14, text="Grade Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                                     return
                             else:
                                 Label(screen14, text="Customer Country Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                                 return
                     else:
                         Label(screen14, text="Working Area Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                         return
                                       
                 else:
                     Label(screen14, text="Customer City Invalid", fg="red",font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                     return
             else:
                 Label(screen14, text="Customer Name Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                 return
        # else:
         #    Label(screen14, text="Customer Code Invalid", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
          #   return
    else:
     Label(screen14, text="Please fill all the details", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
     return

            
   
def order_validation():
 connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
 cursor = connection.cursor()
 select_query = "SELECT AGENT_CODE FROM agents " ";" # queries for retrieving values
 cursor.execute(select_query) # executing the queries
 agent_record = cursor.fetchall()
 connection.commit() # commiting the connection then closing it.
 connection.close()
 if customer_code.get() and order_amount.get() and advance_amount.get() and year.get() and month.get() and date.get() and order_description.get() and order_agent_code.get(): # checking for all empty values in entry field
         order_date=year.get()+'-'+month.get()+'-'+date.get()
         global order_no
         order_no=get_order_no()
         order_num=str(order_no)
         if customer_code_validation(customer_code.get()): # checking for Customer code
             #if (re.match("^[0-9]+$",order_no.get())):# Check for Agent Name
                 if(amount_validation(order_amount.get())):
                     if((amount_validation(advance_amount.get()))):
                         if (advance_amount_validation()):
                             if (re.match('^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$',order_date)):
                                 if(re.match('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', order_description.get())):
                                     if (agent_code_validation(order_agent_code.get())):
                                         # if u enter in this block everything is fine just enter the values in database
                                         connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
                                         cursor = connection.cursor()
                                         insert_query = "INSERT INTO orders (ORD_NUM, ORD_AMOUNT, ADVANCE_AMOUNT, ORD_DATE, CUST_CODE, AGENT_CODE,ORD_DESCRIPTION) VALUES('"+ order_num + "', '"+ order_amount.get() + "', '"+ advance_amount.get() +"', '"+ order_date + "', '"+ customer_code.get() + "' ,'" +order_agent_code.get()+"', '"+ order_description.get() + "');" # queries for inserting values
                                         cursor.execute(insert_query) # executing the queries
                                         connection.commit() # commiting the connection then closing it.
                                         connection.close() # closing the connection of the database
                                         Label(screen16, text="Registration Sucess", fg="green", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) # printing successful registration message
                                        # Button(screen16, text='Back ->', width=20, font=("Open Sans", 9,'bold'), bg='brown', fg='white',command=screen16.destroy).place(x=170, y=565) # button to navigate back to login page
                                     else:
                                         Label(screen16, text="Agent Code Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                                         return
                                 else:
                                     Label(screen16, text="Order Description Invalid", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
                                     return                            
                             else:
                                 Label(screen16, text="Order Date Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                                 return                              
                         else:
                             Label(screen16, text="Advance Amount Greater than Order Amount", fg="red", font=("calibri", 11), width='40', anchor=W, bg='white').place(x=0, y=570)
                             return
                             
                     else:
                        Label(screen16, text="Advance Amount Invaild", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                        return
                 else:
                     Label(screen16, text="Order Amount Invalid", fg="red", font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
                     return
           #  else:
            #     Label(screen16, text="Order Number Invalid", fg="red",font=("calibri", 11), width='20', anchor=W, bg='white').place(x=0, y=570)
             #    return
         else:
             Label(screen16, text="Customer Code Invalid", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
             return
               
 else:
     Label(screen16, text="Please fill all the details", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
     return



def add_agent():
 global screen5, agent_name, working_area, commission,agent_phone,agent_country # making all entry field variable global
 #agent_code = StringVar()
 agent_name = StringVar()
 commission = StringVar()
 working_area=StringVar()
 agent_country = StringVar()
 agent_phone= StringVar()
 screen5 = Toplevel(screen)
 screen5.title("ADDING NEW AGENT")
 adjustWindow(screen5) # configuring the window
 Label(screen5, text="Agent Details", width='32', height="2", font=("Calibri", 22,'bold'), fg='black',bg="#dfe6e9").pack()
 Label(screen5, text="Agent Name:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=210)
 Entry(screen5, textvar=agent_name).place(x=650, y=210)
 Label(screen5, text="Commission:", font=("Open Sans", 11, 'bold'), fg='black', bg="#dfe6e9",anchor=W).place(x=500, y=260)
 Entry(screen5, textvar=commission).place(x=650, y=260)
 Label(screen5, text="Working Area:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=310)
 Entry(screen5, textvar=working_area).place(x=650, y=310)
 Label(screen5, text="Phone No:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=360)
 Entry(screen5, textvar=agent_phone).place(x=650, y=360)
 Label(screen5, text="Country:", font=("Open Sans", 11, 'bold'),fg='black' ,bg="#dfe6e9", anchor=W).place(x=500, y=410)
 Entry(screen5, textvar=agent_country).place(x=650, y=410)
 Button(screen5, text='Back ->', width=15, font=("Open Sans", 13,'bold'), bg='#84DCC6', fg='black',command=screen5.destroy).place(x=570, y=565)
 Button(screen5, text='Submit', width=15, font=("Open Sans", 13, 'bold'), bg='#173aa3',fg='white', command=agent_validation).place(x=570, y=490)

def display_agent():
    global screen12,agent_record
    screen12 = Toplevel(screen)
    screen12.title("AGENT DETAILS")
    adjustWindow(screen12)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT AGENT_CODE,AGENT_NAME,WORKING_AREA,COMMISSION,PHONE_NO FROM agents " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    agent_record = cursor.fetchall()
    Label(screen12, text="Agents Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen12,text="Agent Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen12,text="Agent Name",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen12,text="Working Area",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen12,text="Commission",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    Label(screen12,text="Phone number",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=4)
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
   
    if len(agent_record) > 0:
        for i in range(len(agent_record)): # this loop will display the information to the user
            for j in range(5):
                Label(screen12, text=agent_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+6,column=j, pady=(5,10))
    Button(screen12, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen12.destroy).place(x=370, y=700)


def add_company():
    global screen6,company_name,company_city
    #companyid=StringVar()
    company_name=StringVar()
    company_city=StringVar()
    screen6=Toplevel(screen)
    screen6.title('ADDING NEW COMPANY')
    adjustWindow(screen6) # configuring the window
    Label(screen6, text="Company Details", width='32', height="2", font=("Calibri", 22,'bold'), fg='black',bg="#dfe6e9").pack()
    #Label(screen6, text="", bg='#174873', width='50', height='17').place(x=45, y=120)
    #Label(screen6, text="Company ID:", font=("Open Sans", 11, 'bold'), fg='white',bg='#174873', anchor=W).place(x=650, y=160)
    #Entry(screen6, textvar=companyid).place(x=800, y=160)
    Label(screen6, text="Company Name:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=650, y=210)
    Entry(screen6, textvar=company_name).place(x=800, y=210)
    Label(screen6, text="Company City:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=650, y=260)
    Entry(screen6, textvar=company_city).place(x=800, y=260)
    Button(screen6, text='Submit', width=15, font=("Open Sans", 15, 'bold'), bg='#173aa3',fg='white', command=company_validation).place(x=650, y=500)
    Button(screen6, text='Back', width=15, font=("Open Sans", 15, 'bold'), bg='#84DCC6',fg='black', command=screen6.destroy).place(x=650, y=570)


def display_company():
    global screen13
    screen13 = Toplevel(screen)
    screen13.title("COMPANY DETAILS")
    adjustWindow(screen13)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT COMPANY_ID,COMPANY_NAME,COMPANY_CITY FROM company " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    company_record = cursor.fetchall()
    Label(screen13, text="Company Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen13,text="Company Id",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=4)
    Label(screen13,text="Company Name",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=5)
    Label(screen13,text="Company City",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=6)
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if len(company_record) > 0:
        for i in range(len(company_record)): # this loop will display the information to the user
            for j in range(3):
                Label(screen13, text=company_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+6,column=j+4, pady=(5,10))
    Button(screen13, text='Back ->', width=15, font=("Open Sans",15,'bold'), bg='#84DCC6', fg='black',command=screen13.destroy).place(x=370, y=665)


def add_customer():
    global screen14,customer_code,customer_name,customer_city,customer_working_area,customer_country,customer_grade,opening_amount,receive_amount,customer_payment_amount,customer_outstanding_amount,phone_no,agent_code
    customer_code=StringVar()
    customer_name=StringVar()
    customer_city=StringVar()
    customer_working_area=StringVar()
    customer_country=StringVar()
    customer_grade=StringVar()
    opening_amount=StringVar()
    receive_amount=StringVar()
    customer_payment_amount=StringVar()
    customer_outstanding_amount=StringVar()
    phone_no=StringVar()
    agent_code=StringVar()
    screen14=Toplevel(screen)
    screen14.title('ADDING NEW CUSTOMER')
    adjustWindow(screen14) # configuring the window
    Label(screen14, text="Customer Details", width='22', height="1", font=("Calibri", 15,'bold'), fg='black',bg="#dfe6e9").pack()
    customer_code=get_customer_code()
    Label(screen14, text="Customer Name:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=115)
    Entry(screen14, textvar=customer_name).place(x=670, y=115)
    Label(screen14, text="Customer City:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=500, y=155)
    Entry(screen14, textvar=customer_city).place(x=670, y=155)
    Label(screen14, text="Working Area:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=190)
    Entry(screen14, textvar=customer_working_area).place(x=670, y=190)
    Label(screen14, text="Customer Country:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=225)
    Entry(screen14, textvar=customer_country).place(x=670, y=225)
    Label(screen14, text="Grade:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=500, y=260)
    Entry(screen14, textvar=customer_grade).place(x=670, y=260)
    Label(screen14, text="Opening Amount:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=295)
    Entry(screen14, textvar=opening_amount).place(x=670, y=295)
    Label(screen14, text="Receive Amount:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=330)
    Entry(screen14, textvar=receive_amount).place(x=670, y=330)
    Label(screen14, text="Payment Amount:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=500, y=375)
    Entry(screen14, textvar=customer_payment_amount).place(x=670, y=375)
    Label(screen14, text="Outstanding Amount:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=500, y=410)
    Entry(screen14, textvar=customer_outstanding_amount).place(x=670, y=410)
    Label(screen14, text="Phone Number:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=500, y=445)
    Entry(screen14, textvar=phone_no).place(x=670, y=445)
    Label(screen14, text=" Agent Code:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=500, y=480)
    Entry(screen14, textvar=agent_code).place(x=670, y=480)
    Button(screen14, text='Submit', width=15, font=("Open Sans", 15, 'bold'), bg='#173aa3',fg='white', command=customer_validation).place(x=570, y=530)
    Button(screen14, text='Back', width=15, font=("Open Sans", 15, 'bold'), bg='#84DCC6',fg='black', command=screen14.destroy).place(x=570, y=600)


def display_customer():
    global screen15
    screen15 = Toplevel(screen)
    screen15.title("Welcome")
    adjustWindow(screen15)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT CUST_CODE,CUST_NAME,CUST_CITY,WORKING_AREA,CUST_COUNTRY,GRADE,OPENING_AMT,RECEIVE_AMT,PAYMENT_AMT,OUTSTANDING_AMT,AGENT_CODE FROM customer LIMIT 0,14 " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    customer_record = cursor.fetchall()
    Label(screen15, text="Customer Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen15,text="Cust Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen15,text="Cust Name",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen15,text="Cust City",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen15,text="Work Area",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    Label(screen15,text="Cust Country",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=4)
    Label(screen15,text="Grade",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=5)
    Label(screen15,text="Opening Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=6)
    Label(screen15,text="Recieving Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=7)
    Label(screen15,text="Payment Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=8)
    Label(screen15,text="Outstand Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=9)
    #Label(screen15,text="Phone no",font=("Open Sans", 15, 'bold')).grid(row=1,column=10)
    Label(screen15,text="Agent code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=10)
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if len(customer_record) > 0:
        for i in range(len(customer_record)): # this loop will display the information to the user
            for j in range(11):
                Label(screen15, text=customer_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+11,column=j, pady=(5,10))
    Button(screen15, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen15.destroy).place(x=170, y=700)
    Button(screen15, text='Next', width=15, font=("Open Sans", 15,'bold'), bg='#173aa3', fg='white',command=customer_display2).place(x=650, y=700)
    Button(screen15, text='Contact details', width=20, font=("Open Sans", 15,'bold'), bg='#173aa3', fg='white',command=customer_contact).place(x=950, y=700)

def customer_display2():
    global screen21
    screen21 = Toplevel(screen)
    screen21.title("Welcome")
    adjustWindow(screen21)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT CUST_CODE,CUST_NAME,CUST_CITY,WORKING_AREA,CUST_COUNTRY,GRADE,OPENING_AMT,RECEIVE_AMT,PAYMENT_AMT,OUTSTANDING_AMT,AGENT_CODE FROM customer LIMIT 14,28 " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    customer_record = cursor.fetchall()
    Label(screen21, text="Customer Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen21,text="Cust Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen21,text="Cust Name",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen21,text="Cust City",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen21,text="Work Area",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    Label(screen21,text="Cust Country",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=4)
    Label(screen21,text="Grade",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=5)
    Label(screen21,text="Opening Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=6)
    Label(screen21,text="Recieving Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=7)
    Label(screen21,text="Payment Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=8)
    Label(screen21,text="Outstand Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=9)
    #Label(screen15,text="Phone no",font=("Open Sans", 15, 'bold')).grid(row=1,column=10)
    Label(screen21,text="Agent code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=10)
    connection.commit() # commiting the connection then closing it.
    connection.close()
    if len(customer_record) > 0:
        for i in range(len(customer_record)): # this loop will display the information to the user
            for j in range(11):
                Label(screen21, text=customer_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+11,column=j, pady=(5,10))
    Button(screen21, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen21.destroy).place(x=170, y=700)
    Button(screen21, text='Contact Details', width=20, font=("Open Sans", 15,'bold'), bg='#173aa3', fg='white',command=customer_contact2).place(x=950, y=700)
    if (len(customer_record)>28):
            Button(screen21, text='Next', width=15, font=("Open Sans", 15,'bold'), bg='#173aa3', fg='white',command=customer_display3).place(x=650, y=700)

def customer_display3():
    global screen36
    screen36 = Toplevel(screen)
    screen36.title("Welcome")
    adjustWindow(screen36)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT CUST_CODE,CUST_NAME,CUST_CITY,WORKING_AREA,CUST_COUNTRY,GRADE,OPENING_AMT,RECEIVE_AMT,PAYMENT_AMT,OUTSTANDING_AMT,AGENT_CODE FROM customer LIMIT 28,42 " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    customer_record = cursor.fetchall()
    Label(screen36, text="Customer Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen36,text="Cust Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen36,text="Cust Name",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen36,text="Cust City",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen36,text="Work Area",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    Label(screen36,text="Cust Country",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=4)
    Label(screen36,text="Grade",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=5)
    Label(screen36,text="Opening Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=6)
    Label(screen36,text="Recieving Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=7)
    Label(screen36,text="Payment Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=8)
    Label(screen36,text="Outstand Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=9)
    #Label(screen15,text="Phone no",font=("Open Sans", 15, 'bold')).grid(row=1,column=10)
    Label(screen36,text="Agent code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=10)
    connection.commit() # commiting the connection then closing it.
    connection.close()
    if len(customer_record) > 0:
        for i in range(len(customer_record)): # this loop will display the information to the user
            for j in range(11):
                Label(screen36, text=customer_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+11,column=j, pady=(5,10))
    Button(screen36, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen36.destroy).place(x=170, y=700)
    Button(screen36, text='Contact Details', width=20, font=("Open Sans", 15,'bold'), bg='#173aa3', fg='white',command=customer_contact3).place(x=950, y=700)

def customer_contact():
    global screen22
    screen22 = Toplevel(screen)
    screen22.title("Welcome")
    adjustWindow(screen22)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT CUST_CODE,CUST_NAME,CUST_CITY,PHONE_NO FROM customer LIMIT 0,14 " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    customer_record = cursor.fetchall()
    Label(screen22, text="Contact Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen22,text="Cust Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen22,text="Cust Name",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen22,text="Cust City",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen22,text="Phone Number",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    connection.commit() # commiting the connection then closing it.
    connection.close()
    if len(customer_record) > 0:
        for i in range(len(customer_record)): # this loop will display the information to the user
            for j in range(4):
                Label(screen22, text=customer_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+4,column=j, pady=(5,10))
    Button(screen22, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen22.destroy).place(x=170, y=700)

def customer_contact2():
    global screen23
    screen23 = Toplevel(screen)
    screen23.title("Welcome")
    adjustWindow(screen23)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT CUST_CODE,CUST_NAME,CUST_CITY,PHONE_NO FROM customer LIMIT 14,28 " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    customer_record = cursor.fetchall()
    Label(screen23, text="Contact Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen23,text="Cust Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen23,text="Cust Name",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen23,text="Cust City",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen23,text="Phone Number",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    connection.commit() # commiting the connection then closing it.
    connection.close()
    if len(customer_record) > 0:
        for i in range(len(customer_record)): # this loop will display the information to the user
            for j in range(4):
                Label(screen23, text=customer_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+4,column=j, pady=(5,10))
    Button(screen23, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen23.destroy).place(x=170, y=700)
    

def customer_contact3():
    global screen37
    screen37 = Toplevel(screen)
    screen37.title("Welcome")
    adjustWindow(screen37)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT CUST_CODE,CUST_NAME,CUST_CITY,PHONE_NO FROM customer LIMIT 28,42 " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    customer_record = cursor.fetchall()
    Label(screen37, text="Contact Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen37,text="Cust Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen37,text="Cust Name",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen37,text="Cust City",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen37,text="Phone Number",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    connection.commit() # commiting the connection then closing it.
    connection.close()
    if len(customer_record) > 0:
        for i in range(len(customer_record)): # this loop will display the information to the user
            for j in range(4):
                Label(screen37, text=customer_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+4,column=j, pady=(5,10))
    Button(screen37, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen37.destroy).place(x=170, y=700)
   
   
def add_orders():
    global screen16,order_amount,advance_amount,order_date,order_description,year,month,date,customer_code,order_agent_code
    customer_code=StringVar()
   # order_no=StringVar()
    order_amount=StringVar()
    advance_amount=StringVar()
    order_date=StringVar()
    order_description=StringVar()
    year=StringVar()
    month=StringVar()
    date=StringVar()
    order_agent_code=StringVar()
    screen16=Toplevel(screen)
    screen16.title('ADDING NEW CUSTOMER')
    adjustWindow(screen16) # configuring the window
    Label(screen16, text="Order Details", width='32', height="2", font=("Calibri", 22,'bold'), fg='black',bg="#dfe6e9").pack()
    #Label(screen16, text="", bg='#174873', width='50', height='17').place(x=45, y=120)
    Label(screen16, text="Customer Code:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=160)
    Entry(screen16, textvar=customer_code).place(x=650, y=160)
   # Label(screen16, text="Order Number", font=("Open Sans", 11, 'bold'), fg='white',bg='#174873', anchor=W).place(x=500, y=210)
    #Entry(screen16, textvar=order_no).place(x=650, y=210)
    Label(screen16, text="Order Amount:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=500, y=210)
    Entry(screen16, textvar=order_amount).place(x=650, y=210)
    Label(screen16, text="Advance Amount:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=260)
    Entry(screen16, textvar=advance_amount).place(x=650, y=260)
    Label(screen16, text="Order Date:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=500, y=310)
    year_choices= list(range(2007,2020))
    Combobox(screen16, width=5, values =year_choices ,textvariable = year).place(x=650,y=310)
    month_choices= list(range(1,13))
    Combobox(screen16, width=5, values = month_choices ,textvariable = month).place(x=730,y=310)
    date_choices= list(range(1,32))
    Combobox(screen16, width=5, values = date_choices ,textvariable = date).place(x=810,y=310)
    Label(screen16, text=" Order Description:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=360)
    Entry(screen16, textvar=order_description).place(x=650, y=360)
    Label(screen16, text="Agent Code:", font=("Open Sans", 11, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=500, y=410)
    Entry(screen16, textvar=order_agent_code).place(x=650, y=410)
    Button(screen16, text='Submit', width=15, font=("Open Sans", 15, 'bold'), bg='#2159ff',fg='white', command=order_validation).place(x=570, y=490)
    Button(screen16, text='Back', width=15, font=("Open Sans", 15, 'bold'), bg='#84DCC6',fg='black', command=screen16.destroy).place(x=570, y=570)


def display_orders():
    global screen15
    screen15 = Toplevel(screen)
    screen15.title("Welcome")
    adjustWindow(screen15)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT ORD_NUM,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_DATE,CUST_CODE,AGENT_CODE,ORD_DESCRIPTION FROM orders LIMIT 0,17 " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    order_record = cursor.fetchall()
    Label(screen15, text="Order Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen15,text="Order Number",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen15,text="Order Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen15,text="Advance Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen15,text="Order Date",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    Label(screen15,text="Cust Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=4)
    Label(screen15,text="Agent Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=5)
    Label(screen15,text="Order Description",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=6)
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if len(order_record) > 0:
        for i in range(len(order_record)): # this loop will display the information to the user
            for j in range(7):
                Label(screen15, text=order_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+7,column=j, pady=(5,10))
    Button(screen15, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen15.destroy).place(x=900, y=700)
    Button(screen15, text='Next', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=display_order2).place(x=1100, y=700)
   
    

def display_order2():
    global screen19
    screen19 = Toplevel(screen)
    screen19.title("Welcome")
    adjustWindow(screen19)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT ORD_NUM,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_DATE,CUST_CODE,AGENT_CODE,ORD_DESCRIPTION FROM orders LIMIT 17,35 " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    order_record1 = cursor.fetchall()
    Label(screen19, text="Order Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen19,text="Order Number",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen19,text="Order Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen19,text="Advance Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen19,text="Order Date",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    Label(screen19,text="Cust Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=4)
    Label(screen19,text="Agent Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=5)
    Label(screen19,text="Order Description",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=6)
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if len(order_record1) > 0:
        for i in range(len(order_record1)): # this loop will display the information to the user
            for j in range(7):
                Label(screen19, text=order_record1[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+7,column=j, pady=(5,10))
    Button(screen19, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen19.destroy).place(x=900, y=700)
    Button(screen19, text='Next', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=display_order3).place(x=1100, y=700)


def display_order3():
    global screen20
    screen20 = Toplevel(screen)
    screen20.title("Welcome")
    adjustWindow(screen20)
    connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
    cursor = connection.cursor()
    select_query = "SELECT ORD_NUM,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_DATE,CUST_CODE,AGENT_CODE,ORD_DESCRIPTION FROM orders LIMIT 35,52 " ";" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    order_record = cursor.fetchall()
    Label(screen20, text="Order Details", height="2", font=("Calibri", 22, 'bold'), fg='black',bg="#dfe6e9").grid(row=0,sticky="N",columnspan=17)
    Label(screen20,text="Order Number",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=0)
    Label(screen20,text="Order Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=1)
    Label(screen20,text="Advance Amt",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=2)
    Label(screen20,text="Order Date",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=3)
    Label(screen20,text="Cust Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=4)
    Label(screen20,text="Agent Code",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=5)
    Label(screen20,text="Order Description",font=("Open Sans", 15, 'bold'),fg='black',bg="#dfe6e9").grid(row=1,column=6)
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if len(order_record) > 0:
        for i in range(len(order_record)): # this loop will display the information to the user
            for j in range(7):
                Label(screen20, text=order_record[i][j], font=("Open Sans", 11, 'bold'),fg='black',bg="#dfe6e9").grid(row=i+7,column=j, pady=(5,10))
    Button(screen20, text='Back ->', width=15, font=("Open Sans", 15,'bold'), bg='#84DCC6', fg='black',command=screen20.destroy).place(x=900, y=700)


def agent_func():
    global screen3
    screen3 = Toplevel(screen)
    screen3.title("Welcome")
    adjustWindow(screen3)
    Button(screen3, text='ADD AGENT', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=add_agent).place(x=600, y=100)
    Button(screen3, text='DISPLAY AGENT', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=display_agent).place(x=600, y=150)
    Button(screen3, text='Back ->', width=13, font=("Roboto",15,'bold'), bg='#84DCC6', fg='black',command=screen3.destroy).place(x=600, y=265) # button to navigate back to login page

   
       
def company_func():
    global screen7
    screen7 = Toplevel(screen)
    screen7.title("Welcome")
    adjustWindow(screen7)
    Button(screen7, text='ADD COMPANY', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=add_company).place(x=600, y=100)
    Button(screen7, text='DISPLAY COMPANY', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=display_company).place(x=600, y=150)
    Button(screen7, text='Back ->', width=13, font=("Roboto", 15,'bold'), bg='#84DCC6', fg='black',command=screen7.destroy).place(x=600, y=265)
   
def customer_func():
    global screen10
    screen10 = Toplevel(screen)
    screen10.title("Welcome")
    adjustWindow(screen10)
    Button(screen10, text='ADD CUSTOMER', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=add_customer).place(x=600, y=100)
    Button(screen10, text='DISPLAY CUSTOMERS', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=display_customer).place(x=600, y=150)
    Button(screen10, text='Back ->', width=13, font=("Roboto", 15,'bold'), bg='#84DCC6', fg='black',command=screen10.destroy).place(x=600, y=265)  
   
#def orders_func():
#    global screen11
#    screen11 = Toplevel(screen)
#    screen11.title("Welcome")
 #   adjustWindow(screen11)
 #   Button(screen11, text='ADD ORDER', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=add_orders).place(x=600, y=100)
 #   Button(screen11, text='DISPLAY ORDERS', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=display_orders).place(x=600, y=150)
 #   Button(screen11, text='Back ->', width=13, font=("Roboto", 15,'bold'), bg='#84DCC6', fg='black',command=screen11.destroy).place(x=600, y=265)

def tables():
    global screen11
    screen11 = Toplevel(screen)
    screen11.title("Welcome")
    adjustWindow(screen11)
    Button(screen11, text='ADD AGENT', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=add_agent).place(x=100, y=200)
    Button(screen11, text='DISPLAY AGENT', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=display_agent).place(x=100, y=250)
    Button(screen11, text='ADD COMPANY', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=add_company).place(x=400, y=200)
    Button(screen11, text='DISPLAY COMPANY', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=display_company).place(x=400, y=250)
    Button(screen11, text='ADD CUSTOMER', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=add_customer).place(x=700, y=200)
    Button(screen11, text='DISPLAY CUSTOMERS', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=display_customer).place(x=700, y=250)
    Button(screen11, text='ADD ORDER', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=add_orders).place(x=1000, y=200)
    Button(screen11, text='DISPLAY ORDERS', width=20, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=display_orders).place(x=1000, y=250)
    Button(screen11, text='Back ->', width=13, font=("Roboto", 15,'bold'), bg='#84DCC6', fg='black',command=screen11.destroy).place(x=600, y=500)
    

def welcome_page():
 global screen2
 screen2 = Toplevel(screen)
 screen2.title("Welcome")
 adjustWindow(screen2) # configuring the window
 Label(screen2, text="WELCOME TO SUNVILLE PROPERTIES", width="500", height="2",font=("Roboto", 22, 'bold'), fg='black', bg='#84DCC6').pack()
 photo2 = PhotoImage(file="C:\\Users\\Rudresh\\Desktop\\BWimage2.png") # opening right side image - Note: If
 Label2 = Label(screen2, image=photo2, text="") # attaching image to the label
 Label2.place(x=0, y=73)
 Label2.image = photo2
 #Button(screen2, text='ADD & DISPLAY AGENTS', width=25, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=agent_func).place(x=450, y=150)
 #Button(screen2, text='ADD & DISPLAY COMPANIES', width=25, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=company_func).place(x=450, y=220)
 #Button(screen2, text='ADD & DISPLAY CUSTOMERS', width=25, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=customer_func).place(x=450, y=290)
 Button(screen2, text='ADD & DISPLAY TABLES', width=45, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=tables).place(x=500, y=220)
 Button(screen2, text='COMPANY INFORMATION AND STATISTICS', width=45, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black', command=company_insights).place(x=500, y=430)
 Button(screen2, text='SEARCH ORDER', width=25, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=module2).place(x=400, y=290)
 Button(screen2, text='BALANCE REPORT', width=25, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black',command=report_info).place(x=400, y=360)
 Button(screen2, text='MOST REGISTERED COUNTRY', width=25, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black', command=module4).place(x=800, y=290)
 Button(screen2, text='VIEWPOINT', width=25, font=("Roboto", 13, 'bold'),bg='#E0ACD5', fg='black', command=viewpoint).place(x=800, y=360)
 #Button(screen2, text='MAXIMUM LEASED AREA', width=20, font=("Open Sans", 13, 'bold'),bg='brown', fg='white', command=ans_b).place(x=270, y=350)
 
 
def register_user():
 if fullname.get() and email.get() and password.get() and repassword.get() and gender.get(): # checking for all empty values in entry field
         if tnc.get(): # checking for acceptance of agreement
             if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email.get()):
                 # validating the email
                 if password.get() == repassword.get(): # checking both password match or not
                     # if u enter in this block everything is fine just enter the values in database
                     gender_value = 'male'
                     if gender.get() == 2:
                         gender_value = 'female'
                     connection = pymysql.connect(host="localhost",port=3308, user="root",passwd="", database="project") # database connection
                     cursor = connection.cursor()
                     insert_query = "INSERT INTO login_details (fullname, email, password,gender) VALUES('"+ fullname.get() + "', '"+ email.get() + "', '"+ password.get() +"', '"+ gender_value + "' );" # queries for inserting values
                     cursor.execute(insert_query) # executing the queries
                     connection.commit() # commiting the connection then closing it.
                     connection.close() # closing the connection of the database
                     Label(screen38, text="Registration Sucess", fg="green", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570) # printing successful registration message
                     Button(screen38, text='Proceed to Login ->', width=20, font=("Open Sans", 9,'bold'), bg='brown', fg='white',command=screen38.destroy).place(x=170, y=565) # button to navigate back to login page
                 else:
                     Label(screen38, text="Password does not match", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
                     return
             else:
                 Label(screen38, text="Please enter valid email id", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
                 return
         else:
             Label(screen38, text="Please accept the agreement", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
             return
 else:
     Label(screen38, text="Please fill all the details", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
     return 
 
def register():
    global screen38, fullname, email, password, repassword, gender, tnc # making all entry field variable global
    fullname = StringVar()
    email = StringVar()
    password = StringVar()
    repassword = StringVar()
    gender = IntVar()
    tnc = IntVar()
    screen38 = Toplevel(screen)
    screen38.title("Registration")
    adjustWindow(screen38) # configuring the window
    Label(screen38, text="Registration Form",  width="500", height="2",font=("Roboto", 22, 'bold'), fg='black', bg='#84DCC6').pack()
    Label(screen38, text="Full Name:", font=("Roboto",13, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=520, y=160)
    Entry(screen38, textvar=fullname).place(x=650, y=160)
    Label(screen38, text="Email ID:",font=("Roboto",13, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=520, y=210)
    Entry(screen38, textvar=email).place(x=650, y=210)
    Label(screen38, text="Gender:", font=("Roboto",13, 'bold'), fg='black',bg="#dfe6e9",anchor=W).place(x=520, y=260)
    Radiobutton(screen38, text="Male", variable=gender, value=1,bg="#dfe6e9").place(x=650, y=260)                         
    Radiobutton(screen38, text="Female", variable=gender, value=2,bg="#dfe6e9").place(x=720, y=260)
    Label(screen38, text="Password:", font=("Roboto",13, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=520, y=360)
    Entry(screen38, textvar=password, show="*").place(x=650, y=360)
    Label(screen38, text="Re-Password:",font=("Roboto",13, 'bold'), fg='black',bg="#dfe6e9", anchor=W).place(x=520, y=410)
    entry_4 = Entry(screen38, textvar=repassword, show="*")
    entry_4.place(x=650, y=410)
    Checkbutton(screen38, text="I accept all terms and conditions", variable=tnc,bg="#dfe6e9", font=("Roboto",13, 'bold'), fg='black').place(x=520, y=480)
    Button(screen38, text='Submit', bg="#2159ff", width=15, height=1, font=("Roboto",13, 'bold'), fg='black', command=register_user).place(x=600, y=550)

 
     
def login_verify():
 global companyID 
 connection = pymysql.connect(host="localhost",port=3308, user="root", passwd="",database="project")  # database connection
 cursor = connection.cursor()
 select_query = "SELECT * FROM login_details where email = '" +username.get() + "' AND password = '" + password.get() + "';" # queries forretrieving values
 cursor.execute(select_query) # executing the queries 
 login_info = cursor.fetchall()
 connection.commit() # commiting the connection then closing it.
 connection.close() # closing the connection of the database
 if login_info:
     messagebox.showinfo("Congratulation", "Login Succesfull") # displaying message for successful login
     #studentID = login_info[0][0]
     welcome_page() # opening welcome window
 else:
     messagebox.showerror("Error", "Invalid Username or Password") # displaying message for invalid details
     


def main_screen():
 global screen,username,password
 screen = Toplevel() # initializing the t
 username=StringVar()
 password=StringVar()
 screen.title("SUNVILLE PROPERTIES") # mentioning title of the window
 adjustWindow(screen) # configuring the window
 Label(screen, text="SUNVILLE PROPERTIES", width="500", height="2",font=("Roboto", 22, 'bold'), fg='black', bg='#84DCC6').pack()
 photo1 = PhotoImage(file="C:\\Users\\Rudresh\\Desktop\\BWimage2.png") # opening right side image - Note: If
 Label1 = Label(screen, image=photo1, text="") # attaching image to the label
 Label1.place(x=0, y=73)
 Label1.image = photo1
 Label(screen, text="Username * ", font=("Roboto", 13, 'bold'),fg='black').place(x=620,y=225)    
 Entry(screen, textvar=username).place(x=620,y=255)
 Label(screen, text="").pack() # for leaving a space in between
 Label(screen, text="Password * ", font=("Roboto", 13, 'bold'),fg='black').place(x=620,y=285)
 Entry(screen, textvar=password,show='*').place(x=620,y=315)
 Button(screen, text="LOGIN", bg="#2159ff", width=15, height=1, font=("Roboto",13, 'bold'), fg='white', command=login_verify).place(x=620,y=425)
 Button(screen, text="New User? Register Here", height="1", width="30", bg='#2159ff',font=("Roboto",13, 'bold'), fg='white', command=register).place(x=550,y=500)

 screen.mainloop()
main_screen()