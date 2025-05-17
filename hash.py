from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Adgangskoden, du ønsker at hashe
password = 'admin'

# Hash adgangskoden
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

print(f"Hashed Password: {hashed_password}")