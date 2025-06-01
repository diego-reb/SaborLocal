from werkzeug.security import generate_password_hash
from extension import db
from models import Vendedor 
from flask import request

password = "dzgr10806"  
hashed_password = generate_password_hash(password)
print(hashed_password) 

print(generate_password_hash("abuelo"))
