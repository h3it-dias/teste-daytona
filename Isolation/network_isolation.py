"""
Cria um sandbox com algumas limitações no isolamento do sandbox com relação ao tráfego de saída do sandbox:
- Bloqueando todas as saídas (network_block_all: Booleano)
- Permitindo apenas domínios específicos  (domain_allow_list: lista de string)
"""

from daytona import CreateSandboxFromSnapshotParams, Daytona

daytona = Daytona()

# Bloqueia todas as saídas
sandbox = daytona.create(CreateSandboxFromSnapshotParams(
    network_block_all=True,
))

# Ou permite apenas domínios específicos
sandbox = daytona.create(CreateSandboxFromSnapshotParams(
    domain_allow_list="example.com,*.daytona.io",
))