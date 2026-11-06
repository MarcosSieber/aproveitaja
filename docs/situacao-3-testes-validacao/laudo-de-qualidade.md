# Situação 3: Laudo de qualidade

**Sistema:** AproveitaJá, versão 1.1 · **Responsável:** Marcos Sieber Ribeiro de Paula · **Data:** 16/10/2026

## 1. Resumo
A validação por pares, com 5 testadores, encontrou **6 bugs** (3 de severidade alta e 3 média) e gerou **7 sugestões**. Os 6 bugs foram corrigidos e cobertos por testes de regressão. Das sugestões, 4 foram implementadas e 3 foram para o backlog. A suíte automatizada terminou com **48 de 48 testes aprovados**.

## 2. Erros encontrados e correções
| ID | Erro | Correção aplicada | Arquivo | Teste de regressão | Evidência |
|---|---|---|---|---|---|
| BUG-01 | Validade no passado aceita | Validação da data no cadastro (a edição continua permitida para registrar produtos já vencidos) | `app/models/produto_model.py` | `test_bug01_*` (2) | `04-bug01-validade-passada-corrigido.png` |
| BUG-02 | Quantidade zero aceita | Exigência de quantidade > 0 | `app/models/produto_model.py` | `test_produto_campo_invalido[quantidade-0]` | n/a |
| BUG-03 | Estoque negativo na destinação | Bloqueio de quantidade acima do estoque, e destinação + baixa do estoque na mesma transação | `app/models/destinacao_model.py` | `test_bug03_*` (2) | `05-destinar.png` |
| BUG-04 | Clique duplo duplicava o registro | O botão é desabilitado após o primeiro envio | `app/static/js/app.js` | manual (reteste) | n/a |
| BUG-05 | Tabela cortada no celular | Contêiner com rolagem horizontal e layout responsivo | `app/static/css/style.css` | manual (reteste) | `08-bug05-celular-corrigido.png` |
| BUG-06 | Erro 500 com e-mail duplicado | Tratamento de `IntegrityError` com mensagem amigável | `app/models/usuario_model.py` | `test_bug06_*` | n/a |

## 3. Melhorias implementadas
- **SUG-01** busca por nome e **SUG-02** filtro por situação com ordenação por validade (`03-produtos.png`)
- **SUG-03** confirmação antes de excluir
- **SUG-04** mensagem de login clara

## 4. Resultado dos testes
| Rodada | Testes automatizados | Aprovados | Bugs altos em aberto |
|---|---|---|---|
| Versão 1.0 (antes da validação por pares) | 38 | 38 (100%) | 3 (não cobertos pelos testes) |
| Versão 1.1 (após as correções) | 48 | **48 (100%)** | **0** |

A rodada 1.0 passou em 100% dos testes mesmo com 3 bugs graves. Isso mostra que os testes não cobriam cenários de uso real e confirma o valor da validação por pares. Os 10 testes novos cobrem exatamente esses cenários.

## 5. Limitações conhecidas (não escondidas)
- Não há recuperação de senha.
- Os bugs BUG-04 e BUG-05 envolvem o comportamento do navegador e foram validados por reteste manual, não por teste automatizado. A evolução prevista é adicionar testes E2E com Playwright.
- O sistema ainda não está publicado em um servidor na internet: ele roda localmente, seguindo o README. Para publicar em produção, o recomendado é usar o Render com PostgreSQL.

## 6. Parecer
O sistema **atende aos requisitos Must e Should** e está apto para uso piloto em mercados de bairro.
