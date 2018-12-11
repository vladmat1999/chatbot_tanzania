# chatbot_tanzania
# Database
Baza de date este hostuita pe serverul db4free.net. Daca vreti sa va jucati pe ea puteti.

Ca sa va conectati la ea trebuie sa folositi MySQLdb pentru Python. Puteti sa il luati cu 

pip install mysql

Daca nu merge, incercati asta

pip install --only-binary :all: mysqlclient

Un modul basic pentru baza de date. Pentru a-l folosi, trebuie sa aveti instalat MySQLdb si sa importati modulul.

from database import *

Functiile disponibile sunt:

getUser(ID) - returneaza user-ul
insertUser(ID, Name, Weight, Height) - insereaza un user cu argumentele specificate
modifyUser(Id, Name, Weight, Height) - modifica un user deja inserat
setNul(ID, Name, Weight, Height) - seteaza campurile specificate ale user-ului Null
userExists(ID) - returneaza true/false daca user-ul exista

