# Situação 2: Arquitetura e desenvolvimento

## Padrão MVC
| Camada | Pasta | Responsabilidade |
|---|---|---|
| **Model** | `app/models/` | Acesso ao SQLite e regras de negócio: validações, status de validade, cálculo do relatório |
| **View** | `app/views/` | Templates HTML (Jinja2) que exibem os dados |
| **Controller** | `app/controllers/` | Rotas Flask (Blueprints) que recebem a requisição, chamam o Model e escolhem a View |

```
Navegador ──HTTP──> Controller ──chama──> Model ──SQL──> SQLite
    ^                   │
    └──── HTML ◄── View ◄┘
```

## Rotas
| Método | Rota | Controller | Descrição |
|---|---|---|---|
| GET/POST | `/cadastro` | auth | Criar conta |
| GET/POST | `/login` | auth | Entrar |
| GET | `/logout` | auth | Sair |
| GET | `/painel` | dashboard | Indicadores e alertas |
| GET | `/relatorio` | dashboard | Relatório de aproveitamento |
| GET | `/dicas` | dashboard | Dicas de reaproveitamento |
| GET | `/produtos/` | produtos | Lista com busca e filtro |
| GET/POST | `/produtos/novo` | produtos | Cadastrar |
| GET/POST | `/produtos/<id>/editar` | produtos | Editar |
| POST | `/produtos/<id>/excluir` | produtos | Excluir |
| GET/POST | `/produtos/<id>/destinar` | produtos | Registrar destinação |

## Decisões técnicas
- **Flask** pela simplicidade e boa documentação; **SQLite** porque não exige servidor de banco e é popular e fácil de manter.
- **Modo de codificação:** tradicional (código escrito à mão, sem ferramentas low-code ou no-code).
- **Segurança:** senhas com hash, sessão assinada com `SECRET_KEY`, consultas parametrizadas (contra SQL injection) e verificação de dono em todas as rotas de produto (devolve 404 para produtos de outro usuário).
- **Erros tratados:** formulários inválidos voltam com status 400 e mensagens claras; e-mail duplicado e login inválido têm mensagens próprias; existe uma página 404 personalizada.
