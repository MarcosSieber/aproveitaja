# Situação 3: Feedback dos testadores (validação por pares)

Cinco pessoas testaram a versão 1.0 do sistema entre 05/10/2026 e 09/10/2026, cada uma preenchendo o [formulário de avaliação](formulario-de-avaliacao.md). As capturas de tela estão em [`evidencias/`](evidencias/).

> Substitua "Testador N" pelo nome real de cada pessoa que testou.

---

## Testador 1: colega de curso
**Data:** 05/10/2026 · **Dispositivo:** notebook Windows + Chrome · **Nota:** 4

- **Funcionou:** cadastro de conta, login, cadastro de produto e painel com os indicadores de validade.
- **Não funcionou:** o sistema aceitou cadastrar um produto com validade no passado (01/01/2020), que já entrava como vencido → **BUG-01**. A mensagem de login inválido era genérica → **SUG-04**.
- **Não testado:** relatório (não chegou a registrar destinações); recuperação de senha (não existe no projeto).

## Testador 2: colega de curso
**Data:** 06/10/2026 · **Dispositivo:** notebook Linux + Firefox · **Nota:** 4

- **Funcionou:** cadastro, edição e exclusão de produtos; destinação por doação; relatório.
- **Não funcionou:** foi possível destinar 15 kg de um produto com 10 kg em estoque, e o estoque ficou negativo → **BUG-03**. O sistema aceitou quantidade 0 no cadastro → **BUG-02**.
- **Não testado:** página de dicas.

## Testador 3: desenvolvedor back-end
**Data:** 07/10/2026 · **Dispositivo:** notebook Windows + Chrome · **Nota:** 4

- **Funcionou:** login e logout; tentou abrir o produto de outro usuário trocando o ID na URL e recebeu 404 (isolamento correto); relatório com valores corretos.
- **Não funcionou:** criar uma conta com e-mail já cadastrado gerava "Internal Server Error" (500) → **BUG-06**. Excluir produto não pedia confirmação → **SUG-03**.
- **Não testado:** versão para celular.

## Testador 4: colega de curso
**Data:** 08/10/2026 · **Dispositivo:** celular Android + Chrome · **Nota:** 3

- **Funcionou:** login, painel, menu recolhível e página de dicas.
- **Não funcionou:** no celular a tabela de produtos ficava cortada e as colunas de validade e ações sumiam → **BUG-05**. Com muitos produtos ficava difícil achar um item específico → **SUG-01** (busca por nome).
- **Não testado:** edição de produto.

## Testador 5: desenvolvedora front-end
**Data:** 09/10/2026 · **Dispositivo:** notebook macOS + Chrome · **Nota:** 4

- **Funcionou:** fluxo completo (cadastro de produto → painel → destinação → relatório).
- **Não funcionou:** um clique duplo rápido em "Salvar" cadastrava o produto duas vezes → **BUG-04**. Faltava filtrar a lista por situação e ordenar pela validade → **SUG-02**. Sugeriu também avisos por e-mail ou WhatsApp → **SUG-05**.
- **Não testado:** exportação de relatório e leitura de código de barras (não implementadas).

---

## Consolidação
| ID | Tipo | Descrição | Severidade | Origem | Situação |
|---|---|---|---|---|---|
| BUG-01 | Bug | Validade no passado aceita no cadastro | Alta | Testador 1 | Corrigido |
| BUG-02 | Bug | Quantidade zero aceita no cadastro | Média | Testador 2 | Corrigido |
| BUG-03 | Bug | Destinação maior que o estoque deixava estoque negativo | Alta | Testador 2 | Corrigido |
| BUG-04 | Bug | Clique duplo em "Salvar" duplicava o registro | Média | Testador 5 | Corrigido |
| BUG-05 | Bug | Tabela cortada no celular | Média | Testador 4 | Corrigido |
| BUG-06 | Bug | E-mail duplicado gerava erro 500 | Alta | Testador 3 | Corrigido |
| SUG-01 | Melhoria | Busca de produto por nome | n/a | Testador 4 | Implementada |
| SUG-02 | Melhoria | Filtro por situação e ordenação por validade | n/a | Testador 5 | Implementada |
| SUG-03 | Melhoria | Confirmação antes de excluir | n/a | Testador 3 | Implementada |
| SUG-04 | Melhoria | Mensagem de login mais clara | n/a | Testador 1 | Implementada |
| SUG-05 | Melhoria | Notificação por e-mail/WhatsApp | n/a | Testador 5 | Backlog (RF10) |
| SUG-06 | Melhoria | Leitor de código de barras | n/a | Testador 5 | Backlog (RF11) |
| SUG-07 | Melhoria | Exportar relatório em PDF | n/a | Testador 2 | Backlog (RF12) |

**Nota média de usabilidade:** 3,8 na versão 1.0 e **4,6** no reteste da versão 1.1.
