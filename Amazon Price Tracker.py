# Amazon Price Tracker

import requests
import time
import smtplib
import os
import sys
from bs4 import BeautifulSoup
from tkinter import *


headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
email_sent = False
# Amazon Main Function


def amazon_main():
    URL = amazon_URL.get()
    sel_price = float(amazon_sel_price.get())
    email = amazon_email.get()
    # amazon_password.get()
    time_Checker = amazon_time.get(ACTIVE)
    if time_Checker == '30 seconds':
        time_Checker = 30
    elif time_Checker == '1 minute':
        time_Checker = 60
    elif time_Checker == '10 minutes':
        time_Checker = 600
    elif time_Checker == '30 minutes':
        time_Checker = 1800
    elif time_Checker == '1 hour':
        time_Checker = 3600
    elif time_Checker == '12 hours':
        time_Checker = 43200
    elif time_Checker == '1 day':
        time_Checker = 86400
    else:
        time_Checker = 3600

    # Make Labels and Buttons Dissapear
    amazon_URL_Label.pack_forget()
    amazon_URL.pack_forget()
    amazon_sel_price_label.pack_forget()
    amazon_sel_price.pack_forget()
    amazon_email_label.pack_forget()
    amazon_email.pack_forget()
    # amazon_password_label.pack_forget()
    # amazon_password.pack_forget()
    amazon_time_label.pack_forget()
    amazon_time.pack_forget()
    amazon_Submit_Button.pack_forget()

    # page = requests.get(URL, headers=headers)
    # #Parse Page
    # soup1 = BeautifulSoup(page.content, 'html.parser')
    # soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    # #Finds Name of Product on Page
    # title = soup2.find(id="productTitle").get_text().strip()
    # URL = 'https://www.amazon.in/Sony-MDR-ZX110A-Stereo-Headphones-without/dp/B00KGZZ824/ref=sr_1_1?dchild=1&keywords=sony+headphones&qid=1630693925&sr=8-1'

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    # Finds the price of the Product on Page and converts it from string to number
    try:
        price = soup.find(id="priceblock_ourprice").get_text()
    except:
        # Accounts for amazon products with deals
        price = soup.find(id="priceblock_dealprice").get_text()
    converted_price = price[1:-3]
    for r in (("-", ""), ("₹", ""), (" ", ""), ("-", ""), (',', '')):
        converted_price = converted_price.replace(*r)
    converted_price = float(converted_price)

    def check_price():

        if converted_price <= sel_price:
            global email_sent
            if not email_sent:
                send_mail()
                #Loops in tkinter
                root.after(int(time_Checker*1000), check_price)
        else:
            text = title + ' is not equal to or below ' + str(sel_price)
            nochange_Label = Label(root, text=text)
            nochange_Label.pack()
            #Loops in tkinter
            root.after(int(time_Checker*1000), check_price)

    def send_mail():
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        sender_email = 'yadavyogesh404@gmail.com'
        sender_password = 'wdinfqxzuvtwqmqy'
        server.login(sender_email, sender_password)

        subject = title + 'price has dropped to Rs.' + price[1:] + '!'
        body = '\nCheck out the amazon link: ' + URL

        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(
            sender_email,
            email,
            msg
        )

        trigger_Label = Label(root, text='An email has been sent!', fg='green')
        trigger_Label.pack()

        server.quit()

        global email_sent
        email_sent = True

    # Creates ScrollBar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)
    check_price()

# Amazon Click Function


def amazon_Click():
    amazon_Button.pack_forget()

    try:
        global amazon_URL_Label
        amazon_URL_Label = Label(root, text='Enter an Amazon link:')
        amazon_URL_Label.pack()
        global amazon_URL
        amazon_URL = Entry(root, width=50)
        amazon_URL.pack()
        global amazon_sel_price_label
        amazon_sel_price_label = Label(
            root, text='Enter a trigger price for the email:')
        amazon_sel_price_label.pack()
        global amazon_sel_price
        amazon_sel_price = (Entry(root, width=5))
        amazon_sel_price.pack()
        global amazon_email_label
        amazon_email_label = Label(root, text='Enter your email:')
        amazon_email_label.pack()
        global amazon_email
        amazon_email = Entry(root, width=30)
        amazon_email.pack()
        # global amazon_password_label
        # amazon_password_label = Label(root, text='Enter your email password')
        # amazon_password_label.pack()
        # global amazon_password
        # amazon_password = Entry(root, width=30)
        # amazon_password.pack()
        global amazon_time_label
        amazon_time_label = Label(
            root, text='Select the time interval to check the price:')
        amazon_time_label.pack()
        global amazon_time
        amazon_time = Listbox()
        amazon_time.insert(1, '30 seconds')
        amazon_time.insert(2, '1 minute')
        amazon_time.insert(3, '10 minutes')
        amazon_time.insert(4, '30 minutes')
        amazon_time.insert(5, '1 hour')
        amazon_time.insert(6, '12 hours')
        amazon_time.insert(7, '1 day')
        amazon_time.pack()
        # submit button - add command to button later:
        global amazon_Submit_Button
        amazon_Submit_Button = Button(
            root, text='Submit', width=30, activebackground='white', command=amazon_main)
        amazon_Submit_Button.pack()
    except ValueError:
        valueerror_label = Label(root, text='ValueError was raised')
        valueerror_label.pack()
    except:
        error_label = Label(root, text='Error try again')
        error_label.pack()

# restarts the program:


def restart():
    os.execv(sys.executable, [sys.executable, '"' +
                              sys.argv[0] + '"'] + sys.argv[1:])


# Main window screen
root = Tk(screenName=None,  baseName=None,
          className=' Product Price Tracker',  useTk=1)
header = Label(root, text="PRODUCT PRICE TRACKER",
               font='Helvetica 18 bold', pady=20)
header.pack()
# Amazon Button
amazon_Button = Button(root, text='Amazon', width=30, activebackground='white',
                       bg='yellow', font='Helvetica 12 bold', command=amazon_Click)
amazon_Button.pack()
# Restart Button:
restart_Button = Button(root, text='Restart', width=10,
                        activebackground='white', bg='red', command=restart)
restart_Button.pack()
root.wm_geometry("800x800")
root.mainloop()
