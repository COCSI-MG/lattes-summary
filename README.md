## Inicializar aplicação

### Pré-requisitos
- **Docker** e **Docker Compose** instalados
- Porta **8501** livre no host

### Subir a aplicação
No diretório do projeto:

```bash
# subir e construir a imagem (modo interativo)
docker compose up --build

# opcional: subir em segundo plano (detached)
docker compose up -d --build

# acompanhar logs se estiver em segundo plano
docker compose logs -f
```

Para parar os contêineres:

```bash
docker compose down
```

Notas:
- O serviço mapeia a porta `8501:8501` (definido em `docker-compose.yml`).
- Os diretórios `src`, `scriptLattes` e `tmp` são montados como volumes; os resultados ficam em `./tmp` no host.

---

## Acessar a interface (Streamlit)
- Após subir os serviços, acesse: `http://localhost:8501`
- Na página inicial, clique em **“Ir para Filtro Lattes”** para abrir a tela de busca.

---

## Como usar: inserir IDs Lattes e selecionar filtros

### 1) Inserir IDs Lattes
- Na barra lateral (Sidebar), no campo **IDs Lattes**, insira um ID por linha, por exemplo:
  ```
  1234567890123456
  9876543210987654
  ```
- IDs duplicados são automaticamente ignorados (apenas IDs únicos são processados).

### 2) Configurações principais
- **Período**: defina **Ano inicial** e **Ano final**.
- **Itens por página**: número usado pelo script de coleta (valores maiores podem acelerar a coleta).
- **Diretório de saída**: por padrão `tmp`. Os arquivos gerados aparecem em `./tmp` no host.

### 3) Selecionar filtros e relatórios
Na barra lateral, expanda as seções e marque o que deseja incluir:
- **Relatórios de Produção**: artigos, livros, capítulos, trabalhos de congresso, etc.
- **Produções Técnicas**: software, produtos tecnológicos, processos, trabalhos técnicos, etc.
- **Produções Artísticas**.
- **Orientações em Andamento** e **Orientações Concluídas**.
- **Relatórios Adicionais**: projetos, prêmios, participação/organização de eventos.
- **Grafo de Colaborações**: habilite e selecione os tipos de produção a incluir no grafo.
- **Métricas**: inclui métricas e estatísticas nos resultados.

### 4) Executar a busca
- Clique em **“Buscar Currículos”** na barra lateral.
- Aguarde o processamento; ao concluir, será exibido um resumo com o diretório de saída.

### 5) Visualizar resultados
- Clique em **“Visualizar Resultados na Aplicação”** para abrir a página de análise dentro do Streamlit; ela lê os HTMLs gerados em `tmp` e mostra tabelas, métricas e opção de baixar CSV.
- Alternativamente, abra `tmp/index.html` no navegador para a visualização estática gerada pelo `scriptLattes`.

### 6) Limpar tudo (opcional)
- Use o botão **“Limpar Tudo (incluindo cache)”** na barra lateral para remover arquivos do diretório de saída (inclui cache). Há uma confirmação antes da remoção.

---

## Referências
- [scriptLattes](https://github.com/jpmenachalco/scriptLattes)
