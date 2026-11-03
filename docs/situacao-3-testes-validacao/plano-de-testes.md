# Situação 3: Plano de testes

## Objetivo
Comprovar que o AproveitaJá tem o comportamento esperado:
- **Verificação**: o sistema foi construído corretamente, conforme os requisitos.
- **Validação**: o sistema atende às necessidades de quem vai usá-lo.

## Estratégia
| Nível | Ferramenta | O que cobre | Arquivo |
|---|---|---|---|
| Unitário | pytest | Regras do Model: status de validade, validações de produto, usuário e destinação | `tests/test_unitarios.py` |
| Integração | pytest + Flask test client | Rotas + banco + templates: login, CRUD, isolamento entre usuários, destinação, relatório | `tests/test_integracao.py` |
| Sistema / aceitação | 5 testadores (validação por pares) | Uso real do sistema no navegador e no celular | `feedback-dos-testadores.md` |
| Regressão | pytest | Um teste para cada bug corrigido (nomes `test_bugXX_...`) | ambos |

## Ambiente
- Python 3.12, Flask 3.0.3, pytest 8.3.3, SQLite 3
- Navegadores: Chrome (Windows), Firefox (Linux) e Chrome Android (celular)
- Cada teste automatizado usa um banco temporário próprio (fixture `app` em `tests/conftest.py`)

## Casos de teste principais
| ID | Caso | Resultado esperado |
|---|---|---|
| CT01 | Cadastro com dados válidos | Conta criada, redireciona ao painel |
| CT02 | Cadastro com e-mail já existente | Mensagem "já está cadastrado" (sem erro 500) |
| CT03 | Login com senha errada | Mensagem de erro, status 401 |
| CT04 | Acessar página sem login | Redireciona ao login |
| CT05 | Cadastrar produto válido | Aparece na lista |
| CT06 | Cadastrar produto com validade no passado | Rejeitado com mensagem |
| CT07 | Quantidade zero, negativa ou não numérica | Rejeitado |
| CT08 | Editar e excluir produto | Alteração refletida na lista |
| CT09 | Acessar produto de outro usuário pela URL | 404 |
| CT10 | Classificação vencido / atenção (0 a 3 dias) / ok | Selo correto |
| CT11 | Destinar quantidade válida | Estoque reduzido |
| CT12 | Destinar mais que o estoque | Rejeitado, estoque intacto |
| CT13 | Relatório | Percentual e valor recuperado corretos |
| CT14 | Busca por nome e filtro por situação | Somente os itens correspondentes |
| CT15 | Tela de produtos no celular | Tabela legível, com rolagem horizontal |

## Critério de aceite da entrega
100% dos testes automatizados aprovados e nenhum bug de severidade alta em aberto.
