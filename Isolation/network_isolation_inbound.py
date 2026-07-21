"""
Cria um sandbox com algumas limitações no isolamento do sandbox com relação ao tráfego de entrada do sandbox:
- Criando um arquivo html no sandbox e subindo um servidor HTTP
- Gerando um link de preview para acessar as informações
"""

from daytona import Daytona

daytona = Daytona()
sandbox = daytona.create()

# 1. Cria um arquivo index.html de teste na sandbox
sandbox.process.exec("echo '<h1>Conexão com a Sandbox deu certo!</h1>' > index.html")

# 2. Sobe o servidor HTTP do Python na porta 3000 em background
sandbox.process.exec("nohup python3 -m http.server 3000 > /dev/null 2>&1 &")

# 3. Gera o link de preview
preview = sandbox.get_preview_link(3000)

print(f"URL: {preview.url}")
print(f"Token: {preview.token}")
print(f'\nComando para testar:')
print(f'curl -i -H "x-daytona-preview-token: {preview.token}" {preview.url}')