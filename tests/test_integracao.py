"""Testes de integração: rotas (Controller) + banco de dados (Model) + templates (View)."""
from conftest import cadastrar, criar_produto, dia


# ---------- Autenticação ----------
def test_cadastro_redireciona_para_o_painel(client):
    resposta = cadastrar(client)
    assert resposta.status_code == 200
    assert "Conta criada com sucesso" in resposta.get_data(as_text=True)


def test_bug06_email_duplicado_mostra_mensagem_e_nao_erro_500(client):
    cadastrar(client)
    client.get("/logout")
    resposta = cadastrar(client)
    assert resposta.status_code == 400
    assert "já está cadastrado" in resposta.get_data(as_text=True)


def test_login_e_logout(client):
    cadastrar(client)
    client.get("/logout")
    resposta = client.post("/login", data={"email": "teste@mercado.com", "senha": "senha123"}, follow_redirects=True)
    assert "Olá, Mercado Teste" in resposta.get_data(as_text=True)


def test_login_com_senha_errada(client):
    cadastrar(client)
    client.get("/logout")
    resposta = client.post("/login", data={"email": "teste@mercado.com", "senha": "errada"})
    assert resposta.status_code == 401
    assert "E-mail ou senha incorretos" in resposta.get_data(as_text=True)


def test_rota_protegida_exige_login(client):
    resposta = client.get("/produtos/")
    assert resposta.status_code == 302 and "/login" in resposta.headers["Location"]


# ---------- Produtos ----------
def test_cadastrar_produto_aparece_na_lista(logado):
    resposta = criar_produto(logado, nome="Alface crespa")
    texto = resposta.get_data(as_text=True)
    assert "cadastrado com sucesso" in texto and "Alface crespa" in texto


def test_bug01_rota_rejeita_validade_no_passado(logado):
    resposta = logado.post("/produtos/novo", data={
        "nome": "Leite", "categoria": "Laticínios", "quantidade": "3",
        "unidade": "L", "data_validade": dia(-2), "preco": "4.50"})
    assert resposta.status_code == 400
    assert "não pode estar no passado" in resposta.get_data(as_text=True)


def test_editar_produto(logado):
    criar_produto(logado)
    logado.post("/produtos/1/editar", data={
        "nome": "Banana nanica", "categoria": "Hortifrúti", "quantidade": "7",
        "unidade": "kg", "data_validade": dia(5), "preco": "4.99"})
    assert "Banana nanica" in logado.get("/produtos/").get_data(as_text=True)


def test_excluir_produto(logado):
    criar_produto(logado, nome="Produto Temporario")
    resposta = logado.post("/produtos/1/excluir", follow_redirects=True)
    assert "excluído" in resposta.get_data(as_text=True)
    assert "Nenhum produto encontrado" in logado.get("/produtos/").get_data(as_text=True)


def test_usuario_nao_acessa_produto_de_outro(client):
    cadastrar(client, email="a@mercado.com")
    criar_produto(client)
    client.get("/logout")
    cadastrar(client, email="b@mercado.com")
    assert client.get("/produtos/1/editar").status_code == 404
    assert client.post("/produtos/1/excluir").status_code == 404


def test_sug01_busca_por_nome(logado):
    criar_produto(logado, nome="Maçã gala")
    criar_produto(logado, nome="Pão de forma", categoria="Padaria")
    texto = logado.get("/produtos/?busca=maçã").get_data(as_text=True)
    assert "Maçã gala" in texto and "Pão de forma" not in texto


def test_sug02_filtro_por_situacao(logado):
    criar_produto(logado, nome="Iogurte", data_validade=dia(1))
    criar_produto(logado, nome="Arroz", data_validade=dia(200))
    texto = logado.get("/produtos/?status=atencao").get_data(as_text=True)
    assert "Iogurte" in texto and "Arroz" not in texto


def test_painel_lista_produtos_em_alerta(logado):
    criar_produto(logado, nome="Pão francês", data_validade=dia(0))
    criar_produto(logado, nome="Feijão", data_validade=dia(90))
    texto = logado.get("/painel").get_data(as_text=True)
    assert "Pão francês" in texto and "Vence hoje" in texto and "Feijão" not in texto


# ---------- Destinação e relatório ----------
def test_destinar_baixa_o_estoque(logado):
    criar_produto(logado, quantidade="10")
    logado.post("/produtos/1/destinar", data={"tipo": "doacao", "quantidade": "4"})
    assert "6 kg" in logado.get("/produtos/").get_data(as_text=True)


def test_bug03_rota_rejeita_destinacao_acima_do_estoque(logado):
    criar_produto(logado, quantidade="2")
    resposta = logado.post("/produtos/1/destinar", data={"tipo": "doacao", "quantidade": "5"})
    assert resposta.status_code == 400
    assert "2 kg" in logado.get("/produtos/").get_data(as_text=True)


def test_produto_zerado_sai_da_lista(logado):
    criar_produto(logado, nome="Kiwi", quantidade="1")
    logado.post("/produtos/1/destinar", data={"tipo": "promocao", "quantidade": "1"})
    assert "Kiwi" not in logado.get("/produtos/").get_data(as_text=True)


def test_relatorio_calcula_percentual_de_aproveitamento(logado):
    criar_produto(logado, quantidade="10", preco="2.00")
    logado.post("/produtos/1/destinar", data={"tipo": "promocao", "quantidade": "6"})
    logado.post("/produtos/1/destinar", data={"tipo": "descarte", "quantidade": "2"})
    texto = logado.get("/relatorio").get_data(as_text=True)
    assert "75%" in texto          # 6 aproveitados de 8 destinados
    assert "R$ 12,00" in texto     # 6 x R$ 2,00 recuperados em promoção


def test_paginas_principais_respondem(logado):
    for rota in ["/painel", "/produtos/", "/produtos/novo", "/relatorio", "/dicas"]:
        assert logado.get(rota).status_code == 200


def test_pagina_inexistente_retorna_404(logado):
    assert logado.get("/nao-existe").status_code == 404
