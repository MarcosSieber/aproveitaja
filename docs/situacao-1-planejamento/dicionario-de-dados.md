# Situação 1: Dicionário de dados

SGBD: **SQLite 3**. Chaves estrangeiras ativadas com `PRAGMA foreign_keys = ON`.

## Tabela `usuarios`
| Coluna | Tipo | Nulo | Restrição | Descrição |
|---|---|---|---|---|
| id | INTEGER | Não | PK, autoincremento | Identificador do usuário |
| nome | TEXT | Não | mín. 3 caracteres (aplicação) | Nome do responsável ou do mercado |
| email | TEXT | Não | UNIQUE | E-mail de login (minúsculo) |
| senha_hash | TEXT | Não | | Hash PBKDF2 da senha |
| criado_em | TEXT | Não | padrão: data/hora atual | Data de cadastro |

## Tabela `produtos`
| Coluna | Tipo | Nulo | Restrição | Descrição |
|---|---|---|---|---|
| id | INTEGER | Não | PK, autoincremento | Identificador do produto |
| usuario_id | INTEGER | Não | FK → usuarios.id, ON DELETE CASCADE | Dono do produto |
| nome | TEXT | Não | 2 a 100 caracteres (aplicação) | Nome do produto |
| categoria | TEXT | Não | lista fixa (aplicação) | Hortifrúti, Padaria, Laticínios, Carnes, Mercearia, Bebidas, Outros |
| quantidade | REAL | Não | CHECK ≥ 0 | Estoque atual |
| unidade | TEXT | Não | CHECK IN ('un','kg','L') | Unidade de medida |
| data_validade | TEXT | Não | formato AAAA-MM-DD | Data de validade |
| preco | REAL | Não | CHECK ≥ 0, padrão 0 | Preço unitário em R$ |
| criado_em | TEXT | Não | padrão: data/hora atual | Data de cadastro |

## Tabela `destinacoes`
| Coluna | Tipo | Nulo | Restrição | Descrição |
|---|---|---|---|---|
| id | INTEGER | Não | PK, autoincremento | Identificador |
| produto_id | INTEGER | Não | FK → produtos.id, ON DELETE CASCADE | Produto destinado |
| tipo | TEXT | Não | CHECK IN ('promocao','doacao','reaproveitamento','descarte') | Destino dado ao produto |
| quantidade | REAL | Não | CHECK > 0 | Quantidade destinada |
| observacao | TEXT | Sim | até 255 caracteres (aplicação) | Detalhe livre |
| data | TEXT | Não | padrão: data/hora atual | Data do registro |

## Índices
- `idx_produtos_usuario` (produtos.usuario_id)
- `idx_produtos_validade` (produtos.data_validade): acelera a ordenação por validade
- `idx_destinacoes_prod` (destinacoes.produto_id)
