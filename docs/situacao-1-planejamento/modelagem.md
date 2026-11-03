# Situação 1: Modelagem UML e de dados

> Os diagramas usam Mermaid, que o GitHub desenha automaticamente.

## Diagrama de casos de uso (resumo)
```mermaid
flowchart LR
    U((Usuário do mercado))
    U --> UC1[Cadastrar-se / Fazer login]
    U --> UC2[Gerenciar produtos]
    U --> UC3[Consultar painel de validade]
    U --> UC4[Registrar destinação]
    U --> UC5[Consultar relatório]
    U --> UC6[Ver dicas de reaproveitamento]
    UC4 -. inclui .-> UC7[Baixar estoque]
```

## Diagrama de classes (persistência)
```mermaid
classDiagram
    class Usuario {
        +int id
        +str nome
        +str email
        +str senha_hash
        +datetime criado_em
    }
    class Produto {
        +int id
        +str nome
        +str categoria
        +float quantidade
        +str unidade
        +date data_validade
        +float preco
        +status_validade() str
    }
    class Destinacao {
        +int id
        +str tipo
        +float quantidade
        +str observacao
        +datetime data
    }
    Usuario "1" --> "0..*" Produto : possui
    Produto "1" --> "0..*" Destinacao : recebe
```

## Diagrama de sequência: registrar destinação
```mermaid
sequenceDiagram
    actor U as Usuário
    participant V as View (destinar.html)
    participant C as ProdutoController
    participant M as DestinacaoModel
    participant DB as SQLite
    U->>V: Informa tipo e quantidade
    V->>C: POST /produtos/{id}/destinar
    C->>M: validar(dados, estoque)
    alt dados inválidos
        M-->>C: lista de erros
        C-->>V: formulário com mensagens (400)
    else dados válidos
        C->>M: registrar(produto_id, dados)
        M->>DB: INSERT destinacoes + UPDATE produtos (transação)
        C-->>U: redireciona ao painel com mensagem de sucesso
    end
```

## Modelo entidade-relacionamento (lógico, 3FN)
```mermaid
erDiagram
    USUARIOS ||--o{ PRODUTOS : possui
    PRODUTOS ||--o{ DESTINACOES : recebe
    USUARIOS {
        int id PK
        text nome
        text email UK
        text senha_hash
        text criado_em
    }
    PRODUTOS {
        int id PK
        int usuario_id FK
        text nome
        text categoria
        real quantidade
        text unidade
        text data_validade
        real preco
        text criado_em
    }
    DESTINACOES {
        int id PK
        int produto_id FK
        text tipo
        real quantidade
        text observacao
        text data
    }
```

O projeto físico está em [`database/schema.sql`](../../database/schema.sql).
