<p align="center">
<img 
    src="./assets/cover.png"
    width="200"  
/>
</p>

# Guardiã das Finanças - Chatbot de Controle Financeiro

> ℹ️ **NOTE:** Este é o repositório desenvolvido para o projeto *Guardiã das Finanças*, um chatbot de assistência financeira desenvolvido com assistência do ChatGPT como parte do bootcamp *Coding The Future Caixa - IA Generativa com Microsoft Copilot* da [DIO](https://www.dio.me/bootcamp/coding-the-future-ia-generativa-microsoft-copilot).

O *Guardiã das Finanças* é um chatbot que auxilia usuárias no registro e organização de despesas financeiras, utilizando processamento de linguagem natural (*NLP*) para categorização automática de transações.

## 💻 Tecnologias utilizadas no projeto

- [ChatGPT](https://openai.com/index/chatgpt/)
- [MidJourney](https://www.midjourney.com/home)
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [spaCy](https://spacy.io/)
- [Twilio](https://www.twilio.com/)
- [Pandas](https://pandas.pydata.org/)

## 🚀 Funcionalidades

- Registro de despesas via WhatsApp.
- Identificação automática de categorias de gastos usando *NLP*.
- Gera relatórios financeiros simplificados.
- Permite revisão e edição de categorias registradas.

## 📚 Estrutura do Projeto

```
/
├── assets/
    ├── cover.png        # Imagem de capa
├── outputs/
│   ├── financas.csv     # Arquivo onde são armazenadas as despesas registradas
│   ├── app.py           # Arquivo principal do chatbot
└── README.md            # Documentação do projeto

```

## 🛠️ Como executar o projeto

1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/guardia-financas.git
   ```
2. Acesse a pasta do projeto:
   ```sh
   cd guardia-financas
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Execute o chatbot:
   ```sh
   python app.py
   ```

## 📢 Como usar

1. Envie uma mensagem via WhatsApp para o chatbot informando sua despesa. Exemplo:
   > "Comprei arroz no mercado por R$ 25,90."

2. O chatbot irá automaticamente categorizar a despesa e salvar a informação.

3. Para visualizar seu histórico de gastos, envie:
   > "Listar despesas."

## 🤖 Exemplo de funcionamento

- Entrada do usuário:
  > "Almocei no restaurante por R$ 50."

- Resposta do chatbot:
  > "Despesa registrada: *Alimentação* - R$ 50,00."

## 📷 Inspiração Visual

A representação visual da *Guardiã das Finanças* foi inspirada no conceito de uma heroína digital, refletindo a missão do projeto de empoderar usuárias no controle financeiro.

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Feito com 💙 para apoiar mulheres na organização de suas finanças. 💪
