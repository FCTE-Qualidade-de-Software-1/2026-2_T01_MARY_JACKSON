# Ambiente Docker do draw.io

O arquivo [`compose.yaml`](../../compose.yaml) permite que cada integrante execute localmente a mesma versão do draw.io usada no planejamento: `32.2.0`. Cada pessoa precisa ter Docker Desktop (Windows/macOS) ou Docker Engine e Docker Compose v2 instalados e iniciados.

## Iniciar pela primeira vez

Abra um terminal na raiz do repositório e execute:

```bash
docker compose pull
docker compose up -d
```

A imagem é publicada no Docker Hub como `jgraph/drawio:32.2.0`. Quando o contêiner estiver ativo, acesse <http://localhost:8080/?offline=1>. O parâmetro `offline=1` desativa a integração com armazenamento em nuvem.

## Operações do contêiner

| Ação                             | Comando                         |
| -------------------------------- | ------------------------------- |
| Ver estado e porta               | `docker compose ps`             |
| Acompanhar logs                  | `docker compose logs -f drawio` |
| Parar sem remover                | `docker compose stop`           |
| Iniciar novamente                | `docker compose start`          |
| Reiniciar                        | `docker compose restart`        |
| Remover contêiner e rede         | `docker compose down`           |
| Baixar novamente a imagem fixada | `docker compose pull`           |

`docker compose down` remove o contêiner e a rede do Compose, mas mantém a imagem baixada. Os diagramas são abertos e baixados pelo navegador; este Compose não configura armazenamento persistente no servidor.

## Solução de problemas

- Se o comando informar que o daemon não está disponível, inicie o Docker Desktop e repita o comando.
- Se a porta 8080 já estiver ocupada, altere o mapeamento em `compose.yaml` para `"8081:8080"` e acesse <http://localhost:8081/?offline=1>.
- Se ainda existir um contêiner criado manualmente com o nome `drawio-v32-2-0` ocupando a porta, pare-o com `docker stop drawio-v32-2-0` antes de executar `docker compose up -d`.

Cada integrante executa o serviço na própria máquina. `localhost` não disponibiliza o contêiner aos demais integrantes; para acesso remoto seria necessário hospedar o serviço em um servidor compartilhado.
