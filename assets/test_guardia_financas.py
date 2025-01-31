import pytest
import pandas as pd
from datetime import datetime
from app import extrair_valor, identificar_categoria, salvar_despesa, interpretar_intencao, listar_despesas

file_path = "dados/financas.csv"
df = pd.read_csv(file_path, encoding='utf-8-sig')

@pytest.mark.parametrize("valor, categoria, descricao", [
    (50.00, "alimentação", "Almoço"),
    (120.00, "transporte", "Tanque cheio"),
    (3.0, "alimentação", "Café"),
])

def test_salvar_despesa(valor, categoria, descricao):
    salvar_despesa(valor, categoria, descricao)
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    assert not df.empty
    assert df.iloc[-1]["Valor"] == valor
    assert df.iloc[-1]["Categoria"] == categoria
    assert df.iloc[-1]["Descrição"] == descricao

@pytest.mark.parametrize("mensagem, valor_esperado", [
    ("Comprei um lanche por 25,50", 25.50),
    ("Paguei R$ 100 no mercado", 100.00),
    ("Gasolina 75,9", 75.90),
    ("Remédio 3", 3.00),
    ("Sem valor especificado", None),
])
def test_extrair_valor(mensagem, valor_esperado):
    assert extrair_valor(mensagem) == valor_esperado

@pytest.mark.parametrize("descricao, categoria_esperada", [
    ("Fui ao supermercado", "alimentação"),
    ("Peguei um Uber", "transporte"),
    ("Fui ao cinema", "lazer"),
    ("Consulta médica", "saúde"),
    ("Gastei com algo desconhecido", "Outros"),
])
def test_identificar_categoria(descricao, categoria_esperada):
    assert identificar_categoria(descricao) == categoria_esperada

@pytest.mark.parametrize("mensagem, resposta_esperada", [
    ("Liste minhas despesas", "📌 **Lista de Despesas:**\n"),
    ("Quero um relatório do mês passado",  "📌 **Lista de Despesas:**\n"),
    ("Registrar um gasto de 30 reais com farmácia", "Despesa registrada"),
    ("Mudar categoria para lazer", "Não consegui entender sua solicitação. Tente reformular."),
    ("liste", "📌 **Lista de Despesas:**\n"),
])

def test_interpretar_intencao(mensagem, resposta_esperada):
    resposta = interpretar_intencao(mensagem)
    assert any(expected in resposta for expected in resposta_esperada)