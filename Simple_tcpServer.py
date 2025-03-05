# Código em Python para gerar dois números primos de 2048 bits sem bibliotecas externas
import random
from socket import *

#import random

# Lista dos primeiros 1000 primos para filtro rápido de compostos
SMALL_PRIMES = [
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331,
    337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457,
    461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
    601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733,
    739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877,
    881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021,
    1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151,
    1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283,
    1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429,
    1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549,
    1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667,
    1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811,
    1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973,
    1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089,
    2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243,
    2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377,
    2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531
] 

def generate_random_4096_bit_number():
    """Gera um número ímpar de 2048 bits que é congruente a 3 mod 4."""
    num = random.getrandbits(4096) | (1 << 4095) | 1  # Garante 2048 bits e ímpar
    return num | 3  # Faz com que seja congruente a 3 mod 4

def is_divisible_by_small_primes(n):
    """Verifica se n é divisível por pequenos primos para um descarte rápido."""
    for p in SMALL_PRIMES:
        if n % p == 0:
            return False
    return True

def miller_rabin(n, k=10):
    """Teste de primalidade de Miller-Rabin."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Representar n - 1 como 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Teste probabilístico
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

def generate_prime_4096_bit():
    
    num = generate_random_4096_bit_number()
    
    while True:
        if is_divisible_by_small_primes(num) and miller_rabin(num):
            return num
        num += 2  # Incrementa por 2 para manter o número ímpar

def calcular_totiente():
    totiente = (p - 1) * (q - 1)
    return totiente

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def escolher_primo(totiente):
    while True:
        candidate = random.randint(2, totiente - 1)
        if gcd(candidate, totiente) == 1:
            return candidate

def escolha_d(primoComum, totient):
    t, new_t = 0, 1
    r, new_r = totient, primoComum
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError("O número não possui inverso modular")
    return t % totient

def generate_rsa_keys():
    # Gerar dois primos distintos
    prime1 = generate_prime_4096_bit()
    prime2 = generate_prime_4096_bit()
    while prime2 == prime1:
        prime2 = generate_prime_4096_bit()

    # Calcular N e o totiente
    N = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)

    # Escolher o número coprimo e calcular o inverso modular
    e = escolher_primo(totient)
    d = escolha_d(e, totient)

    # Chaves pública e privada
    public_key = (e, N)
    private_key = (d, N)

    return public_key, private_key

# Gerar e exibir as chaves
public_key, private_key = generate_rsa_keys()
print("Chave pública (e, N):", public_key)
print("Chave privada (d, N):", private_key)

def encrypt(message, public_key):
    e, N = public_key
    message_int = int.from_bytes(message.encode(), 'big')
    return pow(message_int, e, N)

# Função para decriptografar uma mensagem usando a chave privada
def decrypt(ciphertext, private_key):
    d, N = private_key
    message_int = pow(ciphertext, d, N)
    return message_int.to_bytes((message_int.bit_length() + 7) // 8, 'big').decode()

def cifra_de_cesar(texto, deslocamento):
    resultado = ""
    for char in texto:
        novo_char = chr((ord(char) + deslocamento) % 256)
        resultado += novo_char
    return resultado

# Função para descriptografar usando a cifra de César
def descriptografar_cifra_de_cesar(texto, deslocamento):
    return cifra_de_cesar(texto, -deslocamento)

# Defina o servidor e a porta
serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)  # Espera até 5 conexões simultâneas

print("TCP Server aguardando conexão...\n")

# Aceita a conexão do cliente
connectionSocket, addr = serverSocket.accept()

# Geração das chaves públicas e privadas RSA
server_public_key, server_private_key = generate_rsa_keys()

# Envia a chave pública do servidor para o cliente
connectionSocket.send(bytes(str(server_public_key), "utf-8"))

# Recebe a chave pública do cliente
client_public_key_data = connectionSocket.recv(65000)
client_public_key = eval(client_public_key_data.decode())  # Converte a chave recebida de volta para tupla (e, N)

# Recebe a mensagem criptografada do cliente
sentence = connectionSocket.recv(65000)
received_message = str(sentence, "utf-8")
print("Mensagem recebida do cliente (criptografada): ", received_message)

# Descriptografa a mensagem recebida usando a chave privada do servidor
decrypted_message = decrypt(int(received_message), server_private_key)
print("Mensagem DECRIPTOGRAFADA do cliente: ", decrypted_message)

# Realiza o processamento da mensagem, neste caso, convertendo para maiúsculas
capitalized_sentence = decrypted_message.upper()

# Criptografa a resposta com a chave pública do cliente
response_encrypted = encrypt(capitalized_sentence, client_public_key)

# Envia a resposta criptografada de volta ao cliente
connectionSocket.send(bytes(str(response_encrypted), "utf-8"))
print("Resposta enviada de volta ao cliente (criptografada): ", response_encrypted)

# Fecha a conexão
connectionSocket.close()
