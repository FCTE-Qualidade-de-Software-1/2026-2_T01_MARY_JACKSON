"""Gera as cinco cargas sinteticas de Eficiencia de Desempenho (Dupla 2).

Cada arquivo .drawio tem N retangulos iguais, sem conectores, imagens ou
estilos extras, com ids v0001, v0002, ... e rotulos "Rotulo 0001", ...
A saida e deterministica: rodar de novo gera arquivos identicos (mesmo SHA-256).

Uso: python gerar_cargas.py [pasta_de_saida]
"""
import hashlib
import sys
from pathlib import Path

PORTES = [50, 300, 1000, 2000, 5000]
COLUNAS = 50
LARGURA, ALTURA = 120, 60
PASSO_X, PASSO_Y = 160, 100
ESTILO = "rounded=0;whiteSpace=wrap;html=1;"


def gerar_xml(n: int) -> str:
    linhas = [
        '<mxfile host="gerar_cargas.py">',
        f'  <diagram id="carga-{n:05d}" name="Carga {n}">',
        '    <mxGraphModel dx="1000" dy="1000" grid="1" gridSize="10" guides="1" '
        'tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" '
        'pageWidth="850" pageHeight="1100" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0" />',
        '        <mxCell id="1" parent="0" />',
    ]
    for i in range(1, n + 1):
        col, lin = (i - 1) % COLUNAS, (i - 1) // COLUNAS
        x, y = 20 + col * PASSO_X, 20 + lin * PASSO_Y
        linhas.append(
            f'        <mxCell id="v{i:04d}" value="Rotulo {i:04d}" style="{ESTILO}" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{LARGURA}" height="{ALTURA}" '
            f'as="geometry" /></mxCell>'
        )
    linhas += ['      </root>', '    </mxGraphModel>', '  </diagram>', '</mxfile>', '']
    return "\n".join(linhas)


def main() -> None:
    saida = Path(sys.argv[1] if len(sys.argv) > 1 else "cargas")
    saida.mkdir(parents=True, exist_ok=True)
    print(f"{'Arquivo':<22}{'Formas':>8}  SHA-256")
    for n in PORTES:
        conteudo = gerar_xml(n).encode("utf-8")
        arquivo = saida / f"carga-{n:05d}.drawio"
        arquivo.write_bytes(conteudo)  # bytes: mesmo resultado no Windows e no Linux
        print(f"{arquivo.name:<22}{n:>8}  {hashlib.sha256(conteudo).hexdigest()}")


if __name__ == "__main__":
    main()