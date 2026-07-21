"""
Cria um snapshot do Daytona com a classe CreateSnapshotParams, passando algumas informações como parametro:
- name: Um identicador do nosso snapshot
- image: imagem base para o snapshot, deve incluir uma tag ou um digest (ex.: ubuntu:22.04); as tags latest/lts/stable não são suportadas
"""

from daytona import Daytona, CreateSnapshotParams

daytona = Daytona()

# 1. Cria a sandbox de preparação
sandbox = daytona.create()

print("Instalando o Python 3 na sandbox...")
sandbox.process.exec("sudo apt-get update && sudo apt-get install -y python3")

# 2. Cria o arquivo run.py
codigo_run_py = """import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--shard', type=int)
args = parser.parse_args()

print(f'Shard {args.shard} processado com sucesso!')
"""

sandbox.fs.upload_file(codigo_run_py.encode('utf-8'), "run.py")

print("Gerando o snapshot...")
snapshot = daytona.snapshot.create(
    CreateSnapshotParams(
        name="my-awesome-snapshot",
        image="ubuntu:22.04",
        sandbox_id=sandbox.id
    )
)

print(f"Snapshot '{snapshot.name}' criado com sucesso!")

# 4. Limpa a sandbox temporária
sandbox.delete()