"""
Cria um sandbox apartir da classe CreateSandboxFromSnapshotParams, que possui um padrão de snapshots a qual podemos usar
"""

from daytona import Daytona, CreateSandboxFromSnapshotParams
import os 

daytona = Daytona()
sandbox = daytona.create(
    CreateSandboxFromSnapshotParams(
        snapshot="daytona-small",
    )
)