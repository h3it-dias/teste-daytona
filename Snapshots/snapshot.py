"""
Cria um snapshot do Daytona com a classe CreateSnapshotParams, passando algumas informações como parametro:
- name: Um identicador do nosso snapshot
- image: imagem base para o snapshot, deve incluir uma tag ou um digest (ex.: ubuntu:22.04); as tags latest/lts/stable não são suportadas
"""

from daytona import Daytona, CreateSnapshotParams

daytona = Daytona()
snapshot = daytona.snapshot.create(
    CreateSnapshotParams(name="my-awesome-snapshot", image="ubuntu:22.04"),
)