"""
Cria um sandbox apartir da classe CreateSandboxFromSnapshotParams, que possui um padrão de snapshots a qual podemos usar, usando então o 
daytona-vm-small que cria um sandbox do tipo VM Linux
"""

from daytona import Daytona, CreateSandboxFromSnapshotParams

daytona = Daytona()
sandbox = daytona.create(
    CreateSandboxFromSnapshotParams(snapshot="daytona-vm-small")
)