# RAG Document Manager

App desktop (Windows) para triagem e extração determinística de documentos
antes da etapa semântica (LLM), que fica fora deste app.

## Instalar

    pip install -r requirements.txt

## Rodar

    python main.py

## Como funciona

1. Escolha as extensões ativas na lista do topo (todas vêm marcadas por padrão).
2. Clique em "+ Adicionar documentos" (arquivos individuais) ou
   "+ Adicionar pasta" (varre subpastas, só pega as extensões marcadas).
3. O app classifica cada arquivo automaticamente:
   - **Nível 1**: processado automaticamente, sem ressalva.
   - **Nível 2**: processado automaticamente, mas com alerta registrado.
   - **Nível 3**: NÃO processado. O arquivo original é copiado para
     `revisao_manual/` e listado em `revisao_manual/log_pendencias.csv`
     para você tratar manualmente.
4. Nível 1 e 2 geram um `.json` em `resultado_final/`, com o texto extraído
   (por página, parágrafo, cue, linha ou slide, dependendo do formato).
5. `resultado_final/manifesto_triagem.json` registra todos os arquivos
   processados (usa hash SHA256 pra não duplicar reprocessamento).

## Pastas geradas automaticamente

    resultado_final/     -> JSON extraído (nível 1 e 2) + manifesto
    revisao_manual/       -> cópias dos arquivos nível 3 + log_pendencias.csv

## Formatos suportados

VTT, PDF, DOCX, XLSX, PPTX, TXT, MD

## O que este app NÃO faz

Não usa LLM em nenhuma etapa. Toda classificação e extração é determinística
(regras + bibliotecas). A organização semântica (blocos temáticos, tópicos,
citação) é uma etapa separada, que consome o `.json` gerado aqui.
