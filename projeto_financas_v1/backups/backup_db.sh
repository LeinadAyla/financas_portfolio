#!/bin/bash

# --- CONFIGURAÇÕES COM CAMINHOS ABSOLUTOS ---
CONTAINER_NAME="projeto_financas_v1-db-1"
DB_USER="dev_user"
DB_NAME="financas_db"
BACKUP_PATH="/home/kali/projetos/financas_portfolio/projeto_financas_v1/backups"
DATE=$(date +%Y-%m-%d_%Hh%M)
FILENAME="backup_${DB_NAME}_${DATE}.sql"

echo "--- Início do Backup: $(date) ---"

# Verifica se o container está rodando antes de começar
if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME 2>/dev/null)" != "true" ]; then
    echo "❌ ERRO: O container $CONTAINER_NAME não está rodando!"
    exit 1
fi

echo "🚀 Iniciando dump do banco de dados..."
if docker exec $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME > $BACKUP_PATH/$FILENAME; then
    echo "📦 Dump concluído. Compactando arquivo..."
    gzip -f $BACKUP_PATH/$FILENAME
    echo "✅ Backup finalizado com sucesso: $FILENAME.gz"
else
    echo "❌ ERRO: Falha ao gerar o dump."
    exit 1
fi

echo "🧹 Limpando backups com mais de 7 dias..."
find $BACKUP_PATH -type f -name "*.gz" -mtime +7 -delete
echo "--- Fim do Processo: $(date) ---"