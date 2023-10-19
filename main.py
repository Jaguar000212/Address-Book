# Module Imports
try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter.font import Font
    from tkinter.filedialog import askopenfile
    from PIL import ImageTk, Image
except ModuleNotFoundError:
    print("Required modules, Tkinter and Pillow, aren't installed.\nTry running installer.py or install them using pip.")
    input("Press Enter to exit")
    quit()
try:
    from backend.backend import *
except ModuleNotFoundError:
    print("Backend files are missing. Re-extract the source code or run the command line in same folder as this file.")
    input("Press Enter to exit")
    quit()


# Tkinter object
root = Tk()
root.geometry("900x700")  # setting Window size
root.resizable(False, False)  # Configuring window to unresizeable for frames
root.title('Address Book')  # Window title
root.configure(bg="#f9ca74")  # Window backgroud colour
root.iconphoto(False, PhotoImage(file='./assets/book.png'))  # For window icon


# Required functions
def reset():
    # to reset all fields to defaults
    global search_entry
    search_entry.config(text="")
    search_query.set("Select Contact")
    FName.set('')
    LName.set('')
    Contact.set('')
    Address.set('')
    Email.set('')
    Profile.set('')
    Gender.set('Select Gender')
    profile_pic.pack_forget()
    view_frame3.pack_forget()
    profile_image.pack_forget()
    new_profile_image.pack_forget()


def reset_confirm():
    # reset fields with a confirmation
    if messagebox.askokcancel("Confirm", "Are you sure want to reset all fields?\nData might not be saved."):
        reset()


def destroy(up, down):
    # pack and unpack frames for cordination
    try:
        down.pack_forget()
        up.pack(pady=10)
        up.focus()
    except Exception as e:
        messagebox.showerror("Error", f"{e}")


def update_view():
    # update contact list
    try:
        fetch = database.execute("select SNo, FName from AddressBook")
        clist.clear()

        for record in fetch.fetchall():
            clist.append(f"{record[0]} {record[1]}")

        if not clist:
            clist.append('Select Contact')

        search['values'] = clist
    except Exception as e:
        messagebox.showerror("Error", f"{e}")


def upload_file(profile):
    # to upload file and dispaly it
    try:
        global img
        f_types = [('Image Files', ('*.jpg', '*.png'))]
        filename = filedialog.askopenfilename(
            filetypes=f_types, title="Select profile image")
        Profile.set(filename)
        img = Image.open(filename)
        img = img.resize((75, 100))
        img = ImageTk.PhotoImage(img)
        profile.pack(side=RIGHT, padx=10)
        profile.config(image=img)
        profile.image = img
    except AttributeError:
        # raised if upload dialog was opened but no image selected
        pass
    except Exception as e:
        messagebox.showerror("Error", f"{e}")


def view_data(profile):
    # view contact info
    try:
        index = [int(word)
                 for word in search_query.get().split() if word.isdigit()]
        profile.image = ""
        global search_entry
        search_entry.config(text=retrieve_data(str(index[0])))
        view_frame3.pack(pady=10)

        filename = (retrieve_data(index[0], pfp=True))[1]
        photo = Image.open(filename)
        photo = photo.resize((75, 100))
        photo = ImageTk.PhotoImage(photo)
        profile.pack(side=RIGHT, padx=10)
        profile.config(image=photo)
        profile.image = photo
    except AttributeError:
        # raised if no image path in databse
        profile.config(image="")
        profile.config(text="No Picture")
        profile.pack(side=RIGHT)
    except FileNotFoundError:
        # raised if data present but cannot be found
        messagebox.showerror(
            "File not found", "Profile image not found.\nMight have moved or renamed.")
    except IndexError:
        # raised if nothing is passed to search
        messagebox.showerror("Failed", "Empty search query.")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")


def delete_data():
    # delete data from database
    try:
        if messagebox.askokcancel("Confirm", "Are you sure want to delete?"):
            index = [
                int(word) for word in search_query.get().split() if word.isdigit()
            ]
            delete_record(str(index[0]))
            messagebox.showinfo("Done", "Contact successfully deleted")
            update_view()
            reset()
            view_frame3.pack_forget()
            profile_pic.pack_forget()
    except Exception as e:
        messagebox.showerror("Error", f"{e}")


def edit_data(profile):
    # edit data in database
    try:
        index = [int(word)
                 for word in search_query.get().split() if word.isdigit()]
        profile.image = ""
        data = retrieve_all_data(index[0])
        FName.set(data[1])
        LName.set(data[2])
        Gender.set(data[3])
        Email.set(data[4])
        Contact.set(data[5])
        Address.set(data[6])
        Profile.set(data[7])
        filename = data[7]
        photo = Image.open(filename)
        photo = photo.resize((75, 100))
        photo = ImageTk.PhotoImage(photo)
        profile.pack(side=RIGHT)
        profile.config(image=photo)
        profile.image = photo
    except AttributeError:
        # raised if no image path in databse
        profile.config(image="")
        profile.config(text="No Picture")
        profile.pack(side=RIGHT)
    except FileNotFoundError:
        # raised if data present but cannot be found
        messagebox.showerror(
            "File not found", "Profile image not found.\nMight have moved or renamed.")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")


def about():
    # info about the program
    with open('Readme.txt') as f:
        lines = f.read()
    messagebox.showinfo("About", lines)


# Menu bar
menu = Menu(root)
menu.add_cascade(label="About", command=lambda: about())  # add about option
menu.add_cascade(label="Exit", command=root.quit)  # add exit option
root.config(menu=menu)


# Required variables
FName = StringVar()  # carries First Name input
LName = StringVar()  # carries Last Name input
Contact = StringVar()  # carries contact no. input
Address = StringVar()  # carries address input
Email = StringVar()  # carries email input
Profile = StringVar()  # carries path to profile image input
Gender = StringVar()  # carries gender input
search_query = StringVar()  # carries search input
clist = []  # contact list

# Tabs
# define welcome frame for welcome panel
welcome_tab = Frame(root, bg="#f9ca74")
home_tab = Frame(root, bg="#f9ca74")  # define home frame for home tab
add_tab = Frame(root, bg="#f9ca74")  # define add frame for add contact panel
# define view frame for view contact panel
view_tab = Frame(root, bg="#f9ca74")
# define edit frame for edit contact panel
edit_tab = Frame(root, bg="#f9ca74")

# Welcome panel
welcome_tab.pack()
welcome_tab.focus()  # frame focus to take input
welcome_image = Image.open("./assets/Welcome.png")  # image selection
welcome_image = welcome_image.resize((900, 700))
welcome_image = ImageTk.PhotoImage(welcome_image)
panel = Label(welcome_tab, image=welcome_image)  # label to add pic to
panel.image = welcome_image
panel.pack()
# left mouse click to start with home tab
panel.bind('<Button-1>', lambda up: destroy(home_tab, welcome_tab))

# Home tab
Label(home_tab,
      text="The Address Book",
      font=Font(size=48, slant='italic', underline=True), bg="#f9ca74").pack(anchor='center',
                                                                             pady=100)

Button(home_tab,
       text='View Contact',
       font=Font(size=30),
       bd='5', bg="#be7d53",
       command=lambda: [destroy(view_tab, home_tab),
                        update_view()]).pack(anchor='center')
Button(home_tab,
       text='New Contact',
       font=Font(size=30),
       bd='5', bg="#be7d53",
       command=lambda: [destroy(add_tab, home_tab),
                        reset()]).pack(anchor='center')

# Add contact tab
add_frame = Frame(add_tab, bg="#f9ca74")
add_frame.pack(pady=10)

add_frame0 = Frame(add_tab, bg="#f9ca74")
add_frame0.pack(pady=10)

add_frame1 = Frame(add_tab, bg="#f9ca74")
add_frame1.pack(pady=10)

add_frame2 = Frame(add_tab, bg="#f9ca74")
add_frame2.pack(pady=10)

add_frame3 = Frame(add_tab, bg="#f9ca74")
add_frame3.pack(pady=10)

add_frame4 = Frame(add_tab, bg="#f9ca74")
add_frame4.pack(pady=10)

add_frame5 = Frame(add_tab, bg="#f9ca74")
add_frame5.pack(pady=10)

add_frame6 = Frame(add_tab, bg="#f9ca74")
add_frame6.pack(pady=10)

add_frame7 = Frame(add_tab, bg="#f9ca74")
add_frame7.pack(pady=10)

Label(add_frame, text="Add Contact", font=Font(size=38,
                                               underline=True), bg="#f9ca74").pack(pady=10)

# Vacant spaces here and in some of the folowing labels have no syntactical use but for symmetry and good appearance
Label(add_frame0, text='First Name', bg="#f9ca74",
      justify="right", width=15).pack(side=LEFT)
Entry(add_frame0, textvariable=FName, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Label(add_frame1, text='Last Name', bg="#f9ca74",
      justify="right", width=15).pack(side=LEFT)
Entry(add_frame1, textvariable=LName, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Label(add_frame2, text='Phone No.', bg="#f9ca74",
      justify="right", width=15).pack(side=LEFT)
Entry(add_frame2, textvariable=Contact, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Label(add_frame3, text='Address', bg="#f9ca74",
      justify="right", width=15).pack(side=LEFT)
Entry(add_frame3, textvariable=Address, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Label(add_frame4, text='E-Mail', bg="#f9ca74",
      justify="right", width=15).pack(side=LEFT)
Entry(add_frame4, textvariable=Email, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Gender.set("Select Gender")
Label(add_frame5, text='Gender', bg="#f9ca74",
      justify="right", width=15).pack(side=LEFT)
# option menu to prevent data from being different than expected
gender_menu = OptionMenu(add_frame5, Gender, "Male", "Female")
gender_menu.pack(side=RIGHT, pady=5)
gender_menu.config(background="#be7d53")

profile_image = Label(add_frame6, bg="#f9ca74")
Button(add_frame6, text='Upload Profile Picture', bg="#be7d53",
       command=lambda: upload_file(profile_image)).pack(side=LEFT)


Button(add_frame7,
       text="Add", bg="#be7d53",
       command=lambda: update_data(FName.get(), LName.get(), Gender.get(
       ), Address.get(), Email.get(), Contact.get(), Profile.get())).pack(
           side=LEFT)
Button(add_frame7, text="Reset", bg="#be7d53",
       command=reset_confirm).pack(side=LEFT)
Button(add_frame7, text="Home", bg="#be7d53",
       command=lambda: destroy(home_tab, add_tab)).pack(side=LEFT)

# View contact tab
view_frame = Frame(view_tab, bg="#f9ca74")
view_frame.pack(pady=10)

view_frame0 = Frame(view_tab, bg="#f9ca74")
view_frame0.pack(pady=10)

view_frame1 = Frame(view_tab, bg="#f9ca74")
view_frame1.pack(pady=10)

view_frame2 = Frame(view_tab, bg="#f9ca74")
view_frame2.pack(pady=10)

view_frame3 = Frame(view_tab, bg="#f9ca74")

Label(view_frame, text="View Contact", font=Font(size=38,
                                                 underline=True), bg="#f9ca74").pack(pady=10)
search_query.set("Select Contact")
search = ttk.Combobox(view_frame0,
                      textvariable=search_query,
                      width=50,
                      values=clist)  # combobox with ability to take text input and search along with list selection
search.config(font=Font(size=15), background="#be7d53")
search.pack(side=RIGHT)

search_entry = Label(view_frame2, text="", font=Font(
    size=15), justify="left", bg="#f9ca74")
search_entry.pack(side=LEFT)
profile_pic = Label(view_frame2, bg="#be7d53")

Button(view_frame1, text="Search", bg="#be7d53",
       command=lambda: view_data(profile_pic)).pack(side=LEFT)
Button(view_frame1, text="Clear", bg="#be7d53", command=reset).pack(side=LEFT)
Button(view_frame1, text="Home", bg="#be7d53",
       command=lambda: destroy(home_tab, view_tab)).pack(side=LEFT)

Button(view_frame3, text="Delete", bg="#be7d53",
       command=lambda: delete_data()).pack(side=LEFT)
Button(view_frame3, text="Edit", bg="#be7d53",
       command=lambda: [destroy(edit_tab, view_tab), edit_data(new_profile_image)]).pack(side=LEFT)

# Edit contact tab
edit_frame = Frame(edit_tab, bg="#f9ca74")
edit_frame.pack(pady=10)

edit_frame0 = Frame(edit_tab, bg="#f9ca74")
edit_frame0.pack(pady=10)

edit_frame1 = Frame(edit_tab, bg="#f9ca74")
edit_frame1.pack(pady=10)

edit_frame2 = Frame(edit_tab, bg="#f9ca74")
edit_frame2.pack(pady=10)

edit_frame3 = Frame(edit_tab, bg="#f9ca74")
edit_frame3.pack(pady=10)

edit_frame4 = Frame(edit_tab, bg="#f9ca74")
edit_frame4.pack(pady=10)

edit_frame5 = Frame(edit_tab, bg="#f9ca74")
edit_frame5.pack(pady=10)

edit_frame6 = Frame(edit_tab, bg="#f9ca74")
edit_frame6.pack(pady=10)

edit_frame7 = Frame(edit_tab, bg="#f9ca74")
edit_frame7.pack(pady=10)

Label(edit_frame, text="Edit Contact", font=Font(size=38,
                                                 underline=True), bg="#f9ca74").pack(pady=10)

# Vacant spaces here and in some of the folowing labels have no syntactical use but for symmetry and good appearance
Label(edit_frame0, text='First Name', bg="#f9ca74", width=15).pack(side=LEFT)
Entry(edit_frame0, textvariable=FName, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Label(edit_frame1, text='Last Name', bg="#f9ca74", width=15).pack(side=LEFT)
Entry(edit_frame1, textvariable=LName, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Label(edit_frame2, text='Phone No.', bg="#f9ca74", width=15).pack(side=LEFT)
Entry(edit_frame2, textvariable=Contact, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Label(edit_frame3, text='Address', bg="#f9ca74", width=15).pack(side=LEFT)
Entry(edit_frame3, textvariable=Address, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Label(edit_frame4, text='E-Mail', bg="#f9ca74", width=15).pack(side=LEFT)
Entry(edit_frame4, textvariable=Email, width=50,
      bg="#9bab98").pack(side=RIGHT, pady=5)

Gender.set("Select Gender")
Label(edit_frame5, text='Gender', bg="#f9ca74", width=15).pack(side=LEFT)
gender_menu = OptionMenu(edit_frame5, Gender, "Male", "Female")
gender_menu.pack(side=RIGHT, pady=5)
gender_menu.config(background="#be7d53")

new_profile_image = Label(edit_frame6, bg="#be7d53")
Button(edit_frame6, text='Upload Picture',  bg="#be7d53",
       command=lambda: upload_file(new_profile_image)).pack(side=LEFT, padx=10)


Button(edit_frame7,
       text="Save", bg="#be7d53",
       command=lambda: [edit_record(FName.get(), LName.get(), Gender.get(), Email.get(), Contact.get(), Address.get(), Profile.get(), ([int(word) for word in search_query.get().split() if word.isdigit()])[0]), reset(), destroy(view_tab, edit_tab), update_view()]).pack(
           side=LEFT)
Button(edit_frame7, text="Discard", bg="#be7d53",
       command=lambda: destroy(view_tab, edit_tab)).pack(side=LEFT)

# running the tk window
root.mainloop()
