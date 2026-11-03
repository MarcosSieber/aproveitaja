# Situação 1: Requisitos (versão revisada)

## Problema
Mercados de bairro perdem frutas, legumes, pães e laticínios por falta de controle de validade. Esses produtos poderiam ir para promoção, doação ou reaproveitamento antes de vencer. Hoje o controle é feito no papel ou "de olho", e o descarte não é medido.

## Objetivo
Oferecer um sistema web simples que mostre o que está vencendo, registre a destinação de cada item e meça o quanto deixou de ir para o lixo.

## Requisitos funcionais
| ID | Requisito | Prioridade (MoSCoW) |
|---|---|---|
| RF01 | Cadastrar usuário (mercado) com nome, e-mail e senha | Must |
| RF02 | Autenticar usuário (login/logout) | Must |
| RF03 | Cadastrar, editar e excluir produtos com categoria, quantidade, unidade, validade e preço | Must |
| RF04 | Classificar produtos em vencido, atenção (até 3 dias) ou ok | Must |
| RF05 | Exibir painel com indicadores e lista de produtos em alerta | Must |
| RF06 | Registrar destinação (promoção, doação, reaproveitamento, descarte) e dar baixa no estoque | Must |
| RF07 | Exibir relatório de aproveitamento e histórico | Should |
| RF08 | Buscar produto por nome e filtrar por situação | Should *(incluído após a validação por pares)* |
| RF09 | Exibir dicas de reaproveitamento de alimentos | Could |
| RF10 | Enviar notificação de produtos vencendo por e-mail/WhatsApp | Won't (backlog) |
| RF11 | Ler código de barras pela câmera | Won't (backlog) |
| RF12 | Exportar relatório em PDF | Won't (backlog) |

## Requisitos não funcionais
| ID | Requisito |
|---|---|
| RNF01 | Interface responsiva (computador e celular) |
| RNF02 | Senhas armazenadas com hash (Werkzeug/PBKDF2) |
| RNF03 | Cada usuário só acessa os próprios produtos |
| RNF04 | Arquitetura MVC em Python/Flask |
| RNF05 | Banco de dados relacional (SQLite) |
| RNF06 | Cobertura dos fluxos principais por testes automatizados |

## Histórias de usuário
- **HU01**: Como gerente do mercado, quero ver logo ao entrar quais produtos vencem nos próximos dias, para agir antes da perda.
- **HU02**: Como repositor, quero cadastrar um produto com a validade, para que o sistema acompanhe o prazo.
- **HU03**: Como gerente, quero registrar que um produto foi doado ou colocado em promoção, para manter o estoque correto.
- **HU04**: Como dono do mercado, quero ver quanto deixamos de desperdiçar, para medir o resultado da iniciativa.
- **HU05**: Como funcionário, quero dicas de receitas com sobras, para reaproveitar alimentos na produção.

## Critérios de aceitação (exemplos)
- HU01: um produto com validade em até 3 dias aparece no painel com o selo "Atenção"; um produto vencido aparece com o selo "Vencido".
- HU02: não é possível cadastrar validade no passado, quantidade menor ou igual a zero ou categoria inexistente.
- HU03: não é possível destinar quantidade maior que o estoque; após a destinação o estoque diminui.
