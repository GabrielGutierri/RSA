import json
from socket import *
import random

# Função para criptografar utilizando a cifra de César
def cifra_de_cesar(texto, deslocamento):
    resultado = ""
    for char in texto:
        novo_char = chr((ord(char) + deslocamento) % 256)
        resultado += novo_char
    return resultado

# Função para descriptografar utilizando a cifra de César
def descriptografar_cifra_de_cesar(texto, deslocamento):
    return cifra_de_cesar(texto, -deslocamento)

# Funções RSA
# Gerar um número aleatório de 2048 bits
def generate_random_2048_bit_number():
    return random.getrandbits(2048) | (1 << 2047) | 1

# Teste de primalidade (Miller-Rabin)
def miller_rabin(n, k=40):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Gerar um número primo de 2048 bits
def generate_prime_2048_bit():
    while True:
        num = generate_random_2048_bit_number()
        if miller_rabin(num):
            return num

# Calcula o totiente de N
def calcular_totiente(p, q):
    return (p - 1) * (q - 1)

# Algoritmo Euclidiano para encontrar o GCD
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Escolher um número primo coprimo com o totiente
def escolher_primo(totiente):
    while True:
        candidate = random.randint(2, totiente - 1)
        if gcd(candidate, totiente) == 1:
            return candidate

# Função para calcular o inverso modular
def escolha_d(e, totiente):
    t, new_t = 0, 1
    r, new_r = totiente, e
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError("O número não possui inverso modular")
    return t % totiente

# Gerar chaves públicas e privadas RSA
def generate_rsa_keys():
    p = generate_prime_2048_bit()
    q = generate_prime_2048_bit()
    while p == q:
        q = generate_prime_2048_bit()
    N = p * q
    totiente = calcular_totiente(p, q)
    e = escolher_primo(totiente)
    d = escolha_d(e, totiente)
    public_key = (e, N)
    private_key = (d, N)
    return public_key, private_key

# Função para criptografar mensagem usando RSA
def encrypt(message, public_key):
    e, N = public_key
    message_int = int.from_bytes(message.encode(), 'big')
    return pow(message_int, e, N)

# Função para descriptografar mensagem usando RSA
def decrypt(ciphertext, private_key):
    d, N = private_key
    message_int = pow(ciphertext, d, N)
    return message_int.to_bytes((message_int.bit_length() + 7) // 8, 'big').decode()

# Defina o servidor e a porta
serverName = "10.1.70.5"
serverPort = 1300

# Conecta ao servidor
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Gera as chaves RSA para o cliente
public_key, private_key = generate_rsa_keys()
print("Chave pública (e, N):", public_key)

# Envia a chave pública para o servidor em formato JSON
clientSocket.send(json.dumps(public_key).encode())

# Recebe a chave pública do servidor e a converte de volta para a tupla
server_public_key = json.loads(clientSocket.recv(65000).decode())
print("Chave pública do servidor:", server_public_key)

# Solicita a entrada do usuário
sentence = input("Input sentence: ")

# Criptografa a mensagem usando a chave pública RSA
encrypted_message = encrypt(sentence, server_public_key)

# Envia a mensagem criptografada com RSA
clientSocket.send(bytes(str(encrypted_message), "utf-8"))

# Recebe a resposta do servidor
modifiedSentence = clientSocket.recv(65000)
text = str(modifiedSentence, "utf-8")

# Descriptografa a mensagem usando a chave privada do cliente
decrypted_text = decrypt(int(text), private_key)

# Exibe a resposta do servidor após a descriptografia
print("Received from server (decrypted):", decrypted_text)

# Fecha o socket
clientSocket.close()
