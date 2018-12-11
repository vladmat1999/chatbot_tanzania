Un modul basic pentru baza de date. Pentru a-l folosi, trebuie sa aveti instalat MySQLdb si sa importati modulul.

from database import *

Functiile disponibile sunt:

getUser(ID) - returneaza user-ul
insertUser(ID, Name, Weight, Height) - insereaza un user cu argumentele specificate
modifyUser(Id, Name, Weight, Height) - modifica un user deja inserat
setNul(ID, Name, Weight, Height) - seteaza campurile specificate ale user-ului Null
userExists(ID) - returneaza true/false daca user-ul exista
