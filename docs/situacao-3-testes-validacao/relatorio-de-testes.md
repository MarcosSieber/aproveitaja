# Situação 3: Relatório de execução dos testes automatizados

Comando: `python -m pytest -v`

## Resultado final (versão 1.1)
```
tests/test_integracao.py ...................      19 passed
tests/test_unitarios.py  .............................  29 passed
============================== 48 passed ==============================
```

## Distribuição
| Arquivo | Tipo | Quantidade |
|---|---|---|
| `tests/test_unitarios.py` | Unitário (Model) | 29 |
| `tests/test_integracao.py` | Integração (Controller + Model + View + banco) | 19 |
| **Total** | | **48** |

## Rastreabilidade: caso de teste → teste automatizado
| Caso | Teste(s) |
|---|---|
| CT01 | `test_cadastro_redireciona_para_o_painel` |
| CT02 | `test_bug06_email_duplicado_mostra_mensagem_e_nao_erro_500` |
| CT03 | `test_login_com_senha_errada` |
| CT04 | `test_rota_protegida_exige_login` |
| CT05 | `test_cadastrar_produto_aparece_na_lista` |
| CT06 | `test_bug01_cadastro_com_validade_no_passado_e_rejeitado`, `test_bug01_rota_rejeita_validade_no_passado` |
| CT07 | `test_produto_campo_invalido[quantidade-*]` |
| CT08 | `test_editar_produto`, `test_excluir_produto` |
| CT09 | `test_usuario_nao_acessa_produto_de_outro` |
| CT10 | `test_status_validade[*]`, `test_painel_lista_produtos_em_alerta` |
| CT11 | `test_destinar_baixa_o_estoque`, `test_produto_zerado_sai_da_lista` |
| CT12 | `test_bug03_*` |
| CT13 | `test_relatorio_calcula_percentual_de_aproveitamento` |
| CT14 | `test_sug01_busca_por_nome`, `test_sug02_filtro_por_situacao` |
| CT15 | Reteste manual (evidência `08-bug05-celular-corrigido.png`) |
