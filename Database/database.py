import MySQLdb

#Creeaza o conexiune la baza de date si un cursor nou pentru conexiune
conn = MySQLdb.connect(
                        host = "localhost",
                        user = "root",
                        passwd = "",
                        database = "chatbot_database")

cursor = conn.cursor()

#Functii pentru a initializa conexiunea

def initConnection():
    conn = MySQLdb.connect(
                        host = "localhost",
                        user = "root",
                        passwd = "",
                        database = "chatbot_database")

    cursor = conn.cursor()
    return cursor

#Functii pentru a lua si a pune date

#Ia un user si returneaza datele despre el
def getUser(ID):
    '''
    Returneaza un tuple care contine informatii despre user-ul curent. Daca nici
    un user nu a fost gasit, returneaza None.
    De asemenea, la orice alta exceptie returneaza None.
    
    :param str/int ID - ID-ul userului pe care vrei sa-l iei

    :return tuple informatiile user-ului daca exista
            None daca nu exista
    '''
    try:
        cursor.execute("SELECT * FROM users_info WHERE Id = %s", (int(ID),))
        return cursor.fetchall()[0]
    except IndexError:
        print("IndexError - probabil nu a fost gasit user-ul sau a fost o problema \
                cu fetch-ul")
        return None
    except:
        print("A aparut o eroare")
        return None

#Insereaza un user in tabel
def insertUser(ID, Name=None, Weight=None, Height=None):
    '''
    Insereaza un user in tabel. Id-ul user-ului este obligatoriu, iar celelalte
    argumente sunt optionale. Daca nu sunt definite, vor lua valuarea None.
    Daca inserarea a reusit returneaza true.
    Daca user-ul este deja inserat va printa o eroare si returneaza false. Daca\
    vrei sa modifici un user deja definit, foloseste functia modifyUser.

    :param ID required str/int - Id-ul userului\
    :param Name optional str - Numele user-ului\
    :param Weight optional int/double - Greutatea\
    :param Height optional int/double - Inaltimea\

    :return true daca inserarea a avut succes\
            false daca a esuat
    '''

    try:
        cursor.execute("INSERT INTO users_info VALUES (%s, %s, %s, %s)", (int(ID), Name, Weight, Height))
        conn.commit()
        return True
    except MySQLdb.IntegrityError:
        print("User-ul deja exista")
        return False
    except:
        return False

#Modifica un user care se afla in tabel
def modifyUser(ID, Name=None, Weight=None, Height=None):
    '''
    Modifica un user care se alfa deja in tabel. Daca user-ul nu exista, returneaza false.
    Daca user-ul exista, va inlocui doar parametrii speciicati. Daca un paramentru nu este
    specificat va lua valoarea None si nu va fi inlocuit. Asa ca daca vreti sa inlocuiti un
    camp cu valoarea None, nu va fi posibil. Pentru ast folositi functia setNone.
    Daca inlocuirea nu a reusit, returneaza false.

    :param ID required str/int - Id-ul user-ului care trebuie modificat
    :param Name optional str - numele user-ului
    :param Weight optional double/int - greutatea
    :param Height optinal double/int - inaltimea

    :return true - modificarea a reusit
            false - modificarea nu a reusit
    '''

    insertString = ""
    insert = []
    
    if(Name != None):
        insertString += "Name = %s "
        insert.append(Name)
    if(Weight != None):
        if(len(insertString) == 0):
            insertString += "Weight = %s "
        else:
            insertString += ", Weight = %s "
        insert.append(Weight)
    if(Height != None):
        if(len(insertString) == 0):
            insertString += "Height = %s "
        else:
            insertString += ", Height = %s "
        insert.append(Height)

    if(insertString == ""):
        return True
    
    insert.append(int(ID))

    try:
        cursor.execute("UPDATE users_info SET " + insertString + "WHERE Id = %s", tuple(insert))
        conn.commit()
        return True
    except:
        print("A avut loc o eroare")
        return False

#Seteaza campurile user-ului Null
def setNull(ID, Name=False, Weight=False, Height=False):
    '''
    Seteaza campurile userului respectiv la None. Daca setarea a reusit,
    returneaza true, altfel returneaza false.
    Daca user-ul nu exista va returna true.
    Pentru a seta valoarea unui camp la null, se seteaza la true numele campului
    din lista de argumente.

    :param ID required str/int - Id-ul user-ului
    :param Name optional boolean - Numele user-ului
    :param Weight optinal boolean - Greutatea user-ului
    :param Height optinal boolean - Inaltimea user-ului

    :return true - Modificarea a reusit sau user-ul nu exista
            false - Modificarea nu a reusit
    '''

    insertString = ""
    insert = []
    
    if(Name):
        insertString += "Name = %s "
        insert.append(None)
    if(Weight):
        if(len(insertString) == 0):
            insertString += "Weight = %s "
        else:
            insertString += ", Weight = %s "
        insert.append(None)
    if(Height):
        if(len(insertString) == 0):
            insertString += "Height = %s "
        else:
            insertString += ", Height = %s "
        insert.append(None)

    insert.append(int(ID))

    if(insertString == ""):
        return True
   
    try:
        cursor.execute("UPDATE users_info SET " + insertString + "WHERE Id = %s", tuple(insert))
        conn.commit()
        return True
    except:
        print("A avut loc o eroare")
        return False

#Verifica daca un user exista
def userExists(ID):
    '''
    Practic getUser() dar modificat sa returneze true/false daca user-ul exista
    sau nu exista.
    La orice exceptie returneaza false.
    
    :param str/int ID - ID-ul userului pe care vrei sa-l iei

    :return true daca user-ul exista
            false daca user-ul nu exista
    '''
    try:
        cursor.execute("SELECT * FROM users_info WHERE Id = %s", (int(ID),))
        if(len(cursor.fetchall()) > 0):
            return True
        return False
    except:
        print("A aparut o eroare")
        return False
    


    
    

    

