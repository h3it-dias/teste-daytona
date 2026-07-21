"""
Cria uma execução do Snapshot Fan-Out, na qual temos uma snapshot já existente e a criação de diversos sandboxes apartir dessa snapshot, sendo eles
efemeros. 
Informações do processo:
- Processos assincronos de execução executados com um cliente assincrono do Daytona -> AsyncDaytona
- O asyncio.gather dispara 9 execuções de forma paralela dos ambientes sandboxes
- Os sandboxes são criados apartir da snapshot já existente e definidos como ephemeral=True
- Depois o SCRIPT_PYTHON é subido no filesystem do dos sandboxes
- Em seguida é executado passando um número (shard) para aquele ambiente
"""

import asyncio
from daytona import AsyncDaytona, CreateSandboxFromSnapshotParams

SCRIPT_PYTHON = """import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--shard', type=int)
args = parser.parse_args()

print(f'Shard {args.shard} processado com sucesso!')
"""

# Esta função é a rotina de CADA UMA das 20 tarefas
async def run_task(daytona: AsyncDaytona, shard: int) -> str:
    # 1. Cria uma sandbox baseada no snapshot que você já deixou preparado ("my-env-snapshot")
    #    O parâmetro 'ephemeral=True' garante que ela será DELETADA quando parar.
    sandbox = await daytona.create(
        CreateSandboxFromSnapshotParams(
            snapshot="my-awesome-snapshot", 
            ephemeral=True
        )
    )

    await sandbox.fs.upload_file(SCRIPT_PYTHON.encode('utf-8'), "/root/run.py")
    
    # 2. Executa o script dentro dessa sandbox passando o número do lote/fatia (shard)
    response = await sandbox.process.exec(f"python3 /root/run.py --shard {shard}")
    
    # 3. Para a sandbox (como ela é efêmera, o Daytona já a destrói e libera os recursos)
    await sandbox.stop()
    
    # 4. Retorna a resposta/resultado da execução
    return response.result


async def main():
    # Abre o cliente assíncrono do Daytona
    async with AsyncDaytona() as daytona:
        
        # O asyncio.gather executa 'run_task' 20 vezes EM PARALELO (de shard 0 até 19).
        # É aqui que o "Fan-out" (a explosão de sandboxes em leque) acontece na prática!
        results = await asyncio.gather(*(run_task(daytona, i) for i in range(9)))
        
        # Exibe a lista com os resultados de todas as 20 sandboxes
        print(results)

# Inicia a execução do loop assíncrono
asyncio.run(main())