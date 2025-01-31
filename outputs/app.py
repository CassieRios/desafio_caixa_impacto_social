from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
from datetime import datetime, timedelta
import os
import re
import spacy

# Inicializando o Flask e o spaCy
app = Flask(__name__)
nlp = spacy.load("pt_core_news_lg") # Modelo de linguagem em português

# Caminho do diretório e do arquivo
dir_path = "dados"
file_path = os.path.join(dir_path, "financas.csv")

# Criar diretório se não existir
os.makedirs(dir_path, exist_ok=True)

# Criar arquivo se não existir
if not os.path.exists(file_path):
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write('Data,Valor,Categoria,Descrição\n')

# Lista de categorias e preposições
CATEGORIAS = {
    "alimentação": ["supermercado", "compras", "mercado"],
    "transporte": ["uber", "99" "ônibus", "metrô", "combustível", "trem", "gasolina"],
    "lazer": ["cinema", "show", "jantar", "passeio"],
    "moradia": ["aluguel", "luz", "água", "internet","gás"],
    "saúde": ["farmácia", "médico", "remédio", "consulta", "internação", "suplemento"],
    "eletrônicos": ["tv", "geladeira", "computador", "ps5"],
}

PREPOSICOES = {"a", "ante", "após", "até", "com", "contra", "de", "desde", "em", "entre",
               "para", "perante", "por", "sem", "sob", "sobre", "trás"}

VERBOS_MUDAR = ["mudar", "alterar", "modificar", "atualizar"]

def similaridade_palavra(descricao):
    """Identifica a categoria mais provável comparando a média dos vetores."""
    descricao_doc = nlp(descricao.lower())

    melhor_categoria = None
    melhor_similaridade = 0

    for categoria, palavras_chave in CATEGORIAS.items():
        palavras_chave_doc = [nlp(palavra) for palavra in palavras_chave]
        media_vetor_categoria = sum([palavra.vector for palavra in palavras_chave_doc]) / len(palavras_chave_doc)

        similaridade = descricao_doc.vector @ media_vetor_categoria / (descricao_doc.vector_norm * (sum(media_vetor_categoria ** 2) ** 0.5))

        if similaridade > melhor_similaridade:
            melhor_similaridade = similaridade
            melhor_categoria = categoria

    return melhor_categoria if melhor_similaridade > 0.5 else None  # Define um limite mínimo de similaridade

def extrair_valor(texto):
    # Divide a mensagem em palavras
    palavras = texto.split()

    # Filtra apenas os números
    numeros = [p for p in palavras if re.fullmatch(r"\d+[\.,]?\d*", p)]

    if not numeros:
        return None  # Nenhum número encontrado

    if len(numeros) == 1:
        return float(numeros[0].replace(',', '.'))  # Retorna o único número encontrado

    # Se houver mais de um número, tenta identificar o valor correto
    for i, palavra in enumerate(palavras):
        if palavra in numeros:
            # Verifica se a palavra anterior é 'R$', 'por', ou outra indicação de valor
            if i > 0 and palavras[i - 1].lower() in ['r$', 'por', 'de']:
                return float(palavra.replace(',', '.'))

    # Se não encontrar um contexto claro, retorna o último número da mensagem
    return float(numeros[-1].replace(',', '.'))

def identificar_categoria(descricao):
    """Identifica a categoria mais provável usando lemas e similaridade semântica."""
    doc = nlp(descricao.lower())
    lemas = {token.lemma_ for token in doc}

    # Verificação por lemas primeiro (caso tenha correspondência exata)
    for categoria, palavras_chave in CATEGORIAS.items():
        if any(lemma in palavras_chave for lemma in lemas):
            return categoria
    
    # Se não encontrou por lemas, usa a similaridade semântica
    categoria_nova = similaridade_palavra(descricao)
    if categoria_nova:
        return categoria_nova

    return "Outros"

def salvar_despesa(valor, categoria, descricao):
    """Salva a despesa no arquivo CSV."""
    data_atual = datetime.now().strftime("%d/%m/%Y")
    nova_despesa = pd.DataFrame([[data_atual, valor, categoria, descricao]], columns=["Data", "Valor", "Categoria", "Descrição"])
    nova_despesa.to_csv(file_path, mode='a', header=False, index=False, encoding='utf-8-sig')
    return f"Despesa registrada: {descricao} - R$ {valor:.2f} ({categoria})."

def listar_despesas():
    """Gera uma listagem formatada das despesas registradas."""
    despesas = pd.read_csv(file_path, encoding='utf-8-sig')

    if despesas.empty:  # Correção aqui
        return "Nenhuma despesa registrada ainda."

    lista_formatada = ["📌 *Lista de Despesas:*\n"]
    
    for _, despesa in despesas.iterrows():  # Iterar corretamente sobre as linhas
        data = despesa.get("Data", "N/A")
        descricao = despesa.get("Descrição", "Sem descrição")
        valor = despesa.get("Valor", 0.0)
        categoria = despesa.get("Categoria", "Outros")

        lista_formatada.append(f"- *{data}* | {descricao} | R$ {valor:.2f} | *{categoria}*")

    return "\n".join(lista_formatada)

def interpretar_intencao(mensagem):
    """Identifica a intenção do usuário e executa a ação correspondente."""
    doc = nlp(mensagem.lower())
    palavras = [token.lemma_ for token in doc]

    # Verificar se é uma solicitação de listagem de despesas
    lista = "listar" in palavras

    if "listar" in palavras or "relatório" in palavras:
        return listar_despesas()

    # Caso de registro de despesa
    valor = extrair_valor(mensagem)
    if valor:
        categoria = identificar_categoria(mensagem)
        descricao = re.sub(r"(\d+(?:[\.,]\d{2})?)\s?(R\$\s?|\$|real|reais)?", "", mensagem).strip()
        if descricao and categoria:
            salvar_despesa(valor, categoria, descricao)
            return f"Despesa registrada: {categoria} - R$ {valor:.2f}."

    return "Não consegui entender sua solicitação. Tente reformular."

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    msg_in = request.form.get("Body")
    response = MessagingResponse()
    msg_out = response.message()

    if not msg_in:
        msg_out.body("Mensagem vazia. Por favor, envie algo válido.")
        return str(response)

    try:
        resposta = interpretar_intencao(msg_in)
        msg_out.body(resposta)
    except Exception as e:
        msg_out.body(f"Erro ao processar sua solicitação: {str(e)}")

    return str(response)

if __name__ == "__main__":
    app.run(port=5000)
