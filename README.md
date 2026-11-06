# 🥕 AproveitaJá

Sistema web para **controle de validade e reaproveitamento de alimentos em mercados**. O sistema avisa quais produtos estão vencidos ou vão vencer nos próximos 3 dias e registra para onde cada item foi (promoção, doação, reaproveitamento ou descarte). Assim o mercado reduz o desperdício e acompanha os resultados em um relatório.

Projeto Integrador Transdisciplinar em Engenharia de Software II, feito por **Marcos Sieber Ribeiro de Paula** (RGM 34816810).
Alinhado aos ODS 3 (Saúde e Bem-Estar) e 12 (Consumo e Produção Responsáveis).

---

## Funcionalidades

| Módulo | O que faz |
|---|---|
| Autenticação | Cadastro e login de usuários (senhas com hash) |
| Produtos | Cadastrar, editar, excluir, buscar por nome e filtrar por situação |
| Painel | Indicadores de vencidos, vencendo em até 3 dias e dentro da validade, com a lista do que precisa de atenção |
| Destinação | Registra promoção, doação, reaproveitamento ou descarte e dá baixa no estoque |
| Relatório | Percentual de aproveitamento, valor recuperado em promoções e histórico |
| Dicas | Receitas de reaproveitamento integral de alimentos |

## Tecnologias

- **Back-end:** Python 3 + Flask 3, no padrão **MVC**
- **Front-end:** HTML5 (templates Jinja2), CSS3 responsivo e JavaScript
- **Banco de dados:** SQLite (script em `database/schema.sql`)
- **Testes:** pytest (48 testes unitários e de integração)
- **Execução:** local, com o servidor do Flask (publicação no Render prevista)

## Estrutura do repositório

```
aproveitaja/
├── app/
│   ├── models/          # M: acesso ao banco e regras de negócio
│   ├── controllers/     # C: rotas e fluxo das requisições
│   ├── views/           # V: templates HTML
│   └── static/          # CSS e JavaScript
├── database/schema.sql  # projeto físico do banco
├── tests/               # testes automatizados (pytest)
├── docs/
│   ├── situacao-1-planejamento/       # requisitos, modelagem UML, dicionário de dados
│   ├── situacao-2-desenvolvimento/    # arquitetura MVC e manual de uso
│   └── situacao-3-testes-validacao/   # plano/relatório de testes, formulário, feedbacks, laudo, evidências
├── run.py               # inicia o servidor
├── seed.py              # cria dados de demonstração
└── requirements.txt
```

## Como rodar no VS Code

Pré-requisitos: [Python 3.10+](https://www.python.org/downloads/) e [VS Code](https://code.visualstudio.com/) com a extensão **Python**.

1. Abra a pasta `aproveitaja` no VS Code (**File > Open Folder**).
2. Abra o terminal (**Terminal > New Terminal**) e crie o ambiente virtual:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   **Linux / macOS**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. (Opcional) Crie os dados de demonstração:
   ```bash
   python seed.py
   ```
5. Inicie o sistema:
   ```bash
   python run.py
   ```
6. Acesse **http://127.0.0.1:5000** no navegador.
   Login de demonstração: `demo@aproveitaja.com`, senha `demo123`.

> O banco (`instance/aproveitaja.db`) é criado automaticamente na primeira execução.

## Como rodar os testes

```bash
python -m pytest -v
```

Resultado esperado: **48 passed**.

## Como publicar no GitHub

```bash
git init
git add .
git commit -m "AproveitaJá: versão final com testes e documentação"
git branch -M main
git remote add origin https://github.com/MarcosSieber/aproveitaja.git
git push -u origin main
```

## Hospedagem (opcional, Render)

1. Crie uma conta em https://render.com e clique em **New > Web Service**, conectando este repositório.
2. **Build command:** `pip install -r requirements.txt`
3. **Start command:** `gunicorn "app:create_app()"`
4. Em **Environment**, defina `SECRET_KEY` com um valor aleatório.

> No plano gratuito o disco é temporário, então o banco SQLite é recriado quando o serviço reinicia. Para produção, a evolução prevista é migrar para PostgreSQL.

## Links

- Repositório: https://github.com/MarcosSieber/aproveitaja
- Vídeo 1, solução completa (narrado): https://drive.google.com/file/d/1XlTw_M7EjpF0pJ7CqO-5bIEIwupcpVZU/view?usp=sharing
- Vídeo 2, solução atualizada após os testes: https://drive.google.com/file/d/1Jsq6Tsu6S1nfDdKq0REKQt8DtKVUpmEE/view?usp=sharing
