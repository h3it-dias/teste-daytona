"""
Estabelece uma relação linked entre sandboxes, criando uma sandbox parent e uma child (vinculada ao parent criado).
Tudo isso é feito usando a rede interna do próprio Daytona: ao vincularmos a child ao parent pelo parâmetro linked_sandbox, 
iniciamos um servidor HTTP no parent e executamos uma requisição curl a partir da child para o servidor do parent.
"""

from daytona import CreateSandboxFromSnapshotParams, Daytona
import time

daytona = Daytona()

parent = daytona.create()

parent.process.exec("python3 -m http.server 3000 --bind 0.0.0.0 &")

child = daytona.create(
    CreateSandboxFromSnapshotParams(
        linked_sandbox=parent.id,
        ephemeral=True,
    )
)


# The link network registers each sandbox under its name as a DNS alias
response = child.process.exec(f"curl http://{parent.name}:3000/")

print(response)