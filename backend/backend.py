import sqlite3
from tkinter import messagebox


class NullValues(Exception):
    pass


class InvalidData(Exception):
    pass


try:
    # connect to databse, will be created if not present
    database = sqlite3.connect(f'./backend/AddressBook.db')

    # create table if not present in database
    database.execute(
        "CREATE TABLE IF NOT EXISTS AddressBook (SNo integer primary key autoincrement, FName varchar(50) not null, LName varchar(50), Gender text, EMail text, Contact int not null, Address text, Profile text)"
    )
    database.commit()
except Exception as e:
    messagebox.showerror("Error", f"{e}")


def retrieve_data(SNo, pfp=False):
    # fetch data from database with SNo
    # if 'pfp' is False, profile is not returned
    data = ""
    fetch = database.execute("select * from AddressBook where SNo = ?",
                             (SNo, ))
    record = fetch.fetchone()
    # creating string from fetch data to used in label
    data += f"First Name - {record[1]}\nLast Name - {record[2]}\n     Gender - {record[3]}\n       E-Mail - {record[4]}\n Phone No. - {record[5]}\n    Address - {record[6]}\n"
    if pfp is False:
        return data
    else:
        return [data, record[7]]


def retrieve_all_data(SNo):
    # retrieve complete data as a tuple
    fetch = database.execute("select * from AddressBook where SNo = ?",
                             (SNo, ))
    return fetch.fetchone()


def update_data(FName, LName, Gender, Address, Email, Mobile, Profile):
    # insert data to table
    if Gender == "Select Gender":
        Gender = ""
    try:
        if FName == "" or Mobile == "":
            # check if required fields are empty
            raise NullValues("First Name and/or Contact is/are empty")
            # raise if required fields are empty
        try:
            # check if something other than numbers is passed in contact no.
            int(Mobile)
        except:
            raise InvalidData("Phone No. can only have numbers.")
            #  raises exception
        database.execute(
            "insert into AddressBook(FName, LName, Gender, EMail, Contact, Address, Profile) values(?,?,?,?,?,?,?)",
            (FName, LName, Gender, Email, Mobile, Address, Profile))
        database.commit()
        messagebox.showinfo("Done", "Contact successfully added.")
        database.commit()
    except Exception as e:
        messagebox.showerror("Error", f"{e}")


def delete_record(SNo):
    # delete record
    try:
        database.execute("delete from AddressBook where SNo = ?", (SNo, ))
        database.execute(
            "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='AddressBook';")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")


def edit_record(FName, LName, Gender, Email, Mobile, Address, Profile, SNo):
    # edit data
    try:
        if FName == "" or Mobile == "":
            raise NullValues("First Name and/or Contact is/are empty")
        try:
            int(Mobile)
        except:
            raise InvalidData("Phone No. can only have numbers.")
        database.execute("update AddressBook set FName = ?, LName = ?, Gender = ?, EMail = ?, Contact = ?, Address = ?, Profile = ? where SNo = ?",
                         (FName, LName, Gender, Email, Mobile, Address, Profile, SNo))
        database.commit()
        messagebox.showinfo("Done", "Contact saved succesfully.")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")
