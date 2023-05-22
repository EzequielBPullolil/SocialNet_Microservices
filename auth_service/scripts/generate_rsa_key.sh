# Generar una clave privada RSA de 2048 bits
openssl genrsa -out private_key.pem 2048

# Extraer la clave pública correspondiente de la clave privada
openssl rsa -in private_key.pem -pubout -out public_key.pem