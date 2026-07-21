from daytona import Daytona, CreateSandboxFromImageParams, CreateSnapshotParams

daytona = Daytona()

# 1. Tenta deletar o snapshot antigo se ele já existir na conta
try:
    daytona.snapshot.delete("my-awesome-snapshot")
except Exception:
    pass

print("Criando a sandbox com a imagem do Python 3.11...")
# 2. Usa a classe CreateSandboxFromImageParams para definir a imagem
sandbox = daytona.create(
    CreateSandboxFromImageParams(image="python:3.11-slim")
)

print("Criando o arquivo run.py dentro da sandbox...")
codigo_run_py = """import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--shard', type=int)
args = parser.parse_args()

print(f'Shard {args.shard} processado com sucesso!')
"""

# Faz o upload do arquivo run.py
sandbox.fs.upload_file(codigo_run_py.encode('utf-8'), "/root/run.py")

print("Gerando o novo snapshot...")
# 3. Cria o snapshot a partir da sandbox com a imagem do Python
snapshot = daytona.snapshot.create(
    CreateSnapshotParams(
        name="my-awesome-snapshot",
        image="python:3.11-slim",
        sandbox_id=sandbox.id
    )
)

print(f"Snapshot '{snapshot.name}' criado com sucesso!")

# 4. Deleta a sandbox temporária
sandbox.delete()