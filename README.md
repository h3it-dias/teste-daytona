# Daytona Labs & Architecture Playground

Este repositório é uma suíte de testes, experimentos e documentação técnica sobre o **Daytona SDK (Python)**. O objetivo é mapear na prática os padrões de arquitetura, segurança, isolamento de rede e computação distribuída efêmera oferecidos pela plataforma.

---

## Estrutura do Repositório

```text
TESTE-DAYTONA/
└── teste-daytona/
    ├── Isolation/
    │   ├── network_isolation_inbound.py    # Controle e restrição de tráfego de entrada
    │   └── network_isolation_outbound.py   # Restrição de tráfego de saída (Egress Control)
    ├── sandbox/
    │   └── linked_sandbox.py               # Comunicação e encadeamento entre sandboxes
    ├── Snapshots/
    │   ├── sandbox_apartir_snapshot.py     # Criação individual de sandbox via snapshot
    │   ├── sandbox_vm_linux.py             # Instanciação de ambiente Linux completo
    │   ├── snapshot_configuracao_alternativa.py # Setup da imagem e publicação do Snapshot base
    │   ├── snapshot_fan_out.py             # Execução paralela em massa (Fan-out Pattern)
    │   └── snapshot.py                     # Ciclo de vida básico e gerenciamento de snapshots
    ├── .env                                # Variáveis de ambiente e API Keys
    ├── .gitignore                          # Arquivos ignorados pelo Git
    ├── main.py                             # Script de testes gerais / entrypoint
    └── README.md                           # Documentação central do projeto
```

---

## Módulos e Conceitos Chave Explorados

### 1. Isolamento e Segurança de Rede (`Isolation/`)
Explora as capacidades de controle refinado de tráfego para ambientes que exigem alta segurança e execução de código não confiável (Zero Trust).

* **Inbound Isolation (`network_isolation_inbound.py`):** Restringe portas e protocolos que podem receber conexões externas, bloqueando acessos não autorizados vindo de fora para dentro da sandbox.
* **Outbound Isolation (`network_isolation_outbound.py`):** Controla o tráfego de saída (*Egress Control*), impedindo exfiltração de dados ou acessos indevidos a APIs externas a partir do código executado na sandbox.

---

### 2. Sandboxes Conectadas (`sandbox/`)
Demonstra o encadeamento e a comunicação direta entre múltiplas sandboxes (`linked_sandbox.py`).

* Permite arquiteturas estilo **Microserviços**, onde uma sandbox atua como processador/worker e outra como banco de dados ou serviço dependente.
* Permite criar ambientes onde tarefas complexas são quebradas em etapas e passadas de uma sandbox para outra em um pipeline isolado.

---

### 3. Snapshots e Computação Distribuída (`Snapshots/`)

#### A. O Padrão "Snapshot Fan-out" (`snapshot_fan_out.py`)
Utiliza o cliente assíncrono (`AsyncDaytona`) combinado com `asyncio.gather` para disparar $N$ sandboxes efêmeras em paralelo a partir de um único Snapshot base.

```text
                     ┌─> Sandbox Efêmera (Shard 0) ──> [Sucesso] ──> Destroy
                     ├─> Sandbox Efêmera (Shard 1) ──> [Sucesso] ──> Destroy
[AsyncDaytona] ──Fan-out──> Sandbox Efêmera (Shard 2) ──> [Sucesso] ──> Destroy
                     ├─> ...
                     └─> Sandbox Efêmera (Shard N) ──> [Sucesso] ──> Destroy
```

* **Criação da Imagem Base (`snapshot_configuracao_alternativa.py`):** Prepara um ambiente pré-configurado com a imagem oficial do Python (`python:3.11-slim`), eliminando gargalos de instalação durante a execução.
* **Efemeridade (`ephemeral=True`):** As sandboxes nascem, executam sua fatia de trabalho (*shard*) e são destruídas imediatamente ao encerrar, liberando a cota de recursos.

#### B. Gestão de Snapshots e VMs Linux (`sandbox_vm_linux.py`, `snapshot.py`)
* Demonstra como manipular o ciclo de vida dos Snapshots (criar, listar e deletar).
* Permite instanciar sistemas Linux completos com controle direto sobre o ambiente de execução e terminal.

---

## Exemplo Prático: Executando o Fan-out Distribuído

### 1. Registrando o Snapshot Base
```bash
python3 Snapshots/snapshot_configuracao_alternativa.py
```

### 2. Disparando o Processamento Paralelo
```python
import asyncio
from daytona import AsyncDaytona, CreateSandboxFromSnapshotParams

SCRIPT_PYTHON = """import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--shard', type=int)
args = parser.parse_args()

print(f'Shard {args.shard} processado com sucesso!')
"""

async def run_task(daytona: AsyncDaytona, shard: int) -> str:
    # 1. Instancia a sandbox efêmera em milissegundos
    sandbox = await daytona.create(
        CreateSandboxFromSnapshotParams(
            snapshot="my-awesome-snapshot", 
            ephemeral=True
        )
    )
    
    # 2. Injeta e executa o código usando caminho absoluto
    await sandbox.fs.upload_file(SCRIPT_PYTHON.encode('utf-8'), "/root/run.py")
    response = await sandbox.process.exec(f"python3 /root/run.py --shard {shard}")
    
    # 3. Encerra e destrói o ambiente
    await sandbox.stop()
    return response.result

async def main():
    async with AsyncDaytona() as daytona:
        results = await asyncio.gather(*(run_task(daytona, i) for i in range(10)))
        for res in results:
            print(res.strip())

asyncio.run(main())
```

---

## Lições Aprendidas & Boas Práticas

1. **Uso de Caminhos Absolutos (`sandbox.fs`):**
   Sempre especifique caminhos completos ao interagir com o sistema de arquivos do container (ex: `/root/run.py` em vez de `run.py`) para garantir a consistência independente do diretório de trabalho padrão.

2. **Otimização via Snapshots:**
   Nunca execute comandos pesados como `apt-get install` ou `pip install` durante a rotina do Fan-out. Todo o ambiente e bibliotecas devem vir embarcados no **Snapshot** para garantir inicialização abaixo de 1 segundo.

3. **Segurança por Padrão:**
   A combinação de **Isolamento de Rede Outbound** com **Sandboxes Efêmeras** garante o ambiente ideal para execução segura de *code interpreter*, processamento de dados sensíveis e testes de scripts de terceiros.

---

## Como Iniciar

1. Clone este repositório e ative seu ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install daytona-sdk
   ```

2. Configure a variável de ambiente no seu `.env`:
   ```bash
   DAYTONA_API_KEY="seu-token-aqui"
   ```

3. Execute qualquer um dos módulos de teste:
   ```bash
   python3 Snapshots/snapshot_fan_out.py
   python3 Isolation/network_isolation_outbound.py
   ```
