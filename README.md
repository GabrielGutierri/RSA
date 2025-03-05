Este projeto implementa um sistema de comunicação seguro entre um cliente e um servidor utilizando criptografia RSA e a Cifra de César. A comunicação é feita via sockets TCP.

## Visão Geral
O sistema possui duas partes principais:
1. **Cliente (`Simple_tcpClient.py`)**: Gera chaves RSA, envia sua chave pública para o servidor e recebe a chave pública do servidor. Depois, criptografa uma mensagem usando a chave do servidor, envia ao servidor e recebe uma resposta criptografada de volta.
2. **Servidor (`Simple_tcpServer.py`)**: Gera suas próprias chaves RSA, recebe a chave pública do cliente e utiliza essa chave para responder mensagens de forma criptografada.

---

## Funcionalidades Implementadas
- **Geração de números primos de 4096 bits** para criação das chaves RSA.
- **Criação e gerenciamento de chaves RSA** para criptografia e decriptografia segura.
- **Criptografia e decriptografia utilizando RSA** para garantir comunicação segura.
- **Cifra de César** como método alternativo de criptografia.
- **Comunicação via sockets TCP** entre cliente e servidor.

---

## Como Funciona?

### 1. Geração de Chaves RSA
Ambos os arquivos (cliente e servidor) geram um par de chaves RSA composto por:
- **Chave pública** `(e, N)`: usada para criptografar mensagens.
- **Chave privada** `(d, N)`: usada para descriptografar mensagens.

Os números primos necessários para as chaves são gerados através de:
- **Teste de Miller-Rabin** para verificar primalidade.
- **Filtragem por pequenos primos** para descartar números compostos rapidamente.
- **Escolha de um número `e` coprimo ao totiente de `N`**.
- **Cálculo do inverso modular `d`** para obter a chave privada.

### 2. Estabelecimento de Conexão
1. O **servidor** abre um socket e aguarda conexões na porta 1300.
2. O **cliente** se conecta ao servidor.
3. O **cliente e o servidor trocam suas chaves públicas** via socket.

### 3. Comunicação Segura
1. O **cliente solicita uma entrada do usuário** e criptografa a mensagem com a chave pública do servidor.
2. O **cliente envia a mensagem criptografada** para o servidor.
3. O **servidor recebe e descriptografa a mensagem** com sua chave privada.
4. O **servidor processa a mensagem** (converte para maiúsculas, por exemplo).
5. O **servidor criptografa a resposta** usando a chave pública do cliente e a envia.
6. O **cliente descriptografa a resposta** com sua chave privada e exibe no console.

### 4. Implementação da Cifra de César
Além da criptografia RSA, os arquivos incluem funções para criptografar e descriptografar mensagens usando a Cifra de César, deslocando os caracteres com base em um valor pré-definido.

---

## Estrutura do Código

### Cliente (`Simple_tcpClient.py`)
1. **Gera as chaves RSA**.
2. **Estabelece conexão com o servidor** via socket TCP.
3. **Envia sua chave pública** para o servidor e recebe a chave pública do servidor.
4. **Solicita uma mensagem ao usuário** e a criptografa usando RSA.
5. **Envia a mensagem criptografada para o servidor**.
6. **Recebe a resposta criptografada do servidor** e a descriptografa com sua chave privada.
7. **Exibe a resposta descriptografada** e encerra a conexão.

### Servidor (`Simple_tcpServer.py`)
1. **Gera as chaves RSA**.
2. **Aguarda conexões de clientes** na porta 1300.
3. **Aceita a conexão do cliente** e recebe sua chave pública.
4. **Envia sua chave pública para o cliente**.
5. **Recebe a mensagem criptografada do cliente** e a descriptografa com sua chave privada.
6. **Processa a mensagem** (converte para maiúsculas).
7. **Criptografa a resposta com a chave pública do cliente** e a envia de volta.
8. **Fecha a conexão após a troca de mensagens**.
