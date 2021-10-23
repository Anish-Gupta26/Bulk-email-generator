from django import http
import smtplib, ssl
from django.shortcuts import render,HttpResponse
import pandas as pd
import re
from .models import FileUpload

#Global variable
dict={}         #Stores matching pairs of placeholders
size_Pholder=0  #Size/ Number of placeholder in .txt file
col_head=[]     #Stores column header of excel file
output=[]       #List of Final output strings with data from excel
txt_data=""     #String with data of .txt file
df=""           #Data Frame object of pandas

def send_mail(request):     #Function to send mail 
    if request.method == "POST":
        s_email = request.POST.get("e-mail")  #Extracting data from excel file
        s_passwsord = request.POST.get('password')
        subject = request.POST.get('subject')
        email_col = request.POST.get('email_col')
        for i in range(len(output)):
            port = 587  # For starttls
            smtp_server = "smtp.gmail.com"
            sender_email = s_email
            receiver_email = df.loc[df.index[i],email_col]
            password = s_passwsord
            message = 'Subject: {}\n\n{}'.format(subject, output[i])
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  
                server.starttls(context=context)
                server.ehlo() 
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
    return render(request,'output.html')    

def matching(request):
    if request.method == "POST":
        global dict,txt_data,output
        for i in range(size_Pholder):
            p = str(i)
            s = str(1000+i)
            x = request.POST.get(p)       #Extracting Placeholders using name attribute of HTML
            y = request.POST.get(s)
            dict[x] = y                   #Mapping of placeholders
        
        output=[]
        for i in range(len(df)):          #Making string list using row data of data frames
            temp=txt_data
            for keys in dict:
                data = df.loc[df.index[i],dict[keys]]    #data extraction
                temp = temp.replace(keys, str(data))     #replacing placeholder with excel data
            output.append(temp)
    return render(request,'details.html',{'col_head':col_head}) #INput user email and password

def home(request):
    if request.method == "POST":
        excel_file = request.FILES["excel-file"]  #Extracting data from excel file
        text_file = request.FILES['text-file']    #Extracting data from .txt file
        #Checking for valid file format
        valid_excel = (".xls",".xlsx",".xlsm" ,".xlsb",".odf" ,".ods","odt")
        if text_file.name.endswith('.txt')==False or excel_file.name.endswith(valid_excel)==False:
             return HttpResponse("Oops! Please provide right file format")
        
        global df, txt_data,size_Pholder,col_head
        df=""
        txt_data=""
        csv = pd.read_excel(excel_file) 
        df = pd.DataFrame(csv)
        col_head = []                    #Headers of excel file
        for col in csv.columns:
            col_head.append(col)
        
        for x in text_file:             #text file data
            txt_data+=x.decode()
        
        text_Pholder = re.findall('\%.*?\%', txt_data) #Placeholders of .txt file using regex
        text_Pholder_set = set(text_Pholder)                   #For unique placeholders
        text_Pholder.clear()
        text_Pholder = list(text_Pholder_set)
        size_Pholder = len(text_Pholder_set)               #Total placeholders
        return render(request,'index.html',{'something':True,'text_Pholder':text_Pholder,'excel_Pholder':col_head,'range':range(size_Pholder), 'count':1000})
    return render(request,'home.html')

def upload(request):
    return render(request,"fileupload.html")

