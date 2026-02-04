import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Meu Grok Pessoal", layout="wide")

# Conecta com a API do Grok (usa sua chave salva em segredo)
client = OpenAI(api_key=st.secrets["XAI_API_KEY"], base_url="https://api.x.ai/v1")

st.title("💬 Meu Grok Pessoal - Teste Simples")

# Guarda as mensagens da conversa (memória básica por agora)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra mensagens antigas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite aqui e converse comigo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando como seu Grok pessoal..."):
            try:
                response = client.chat.completions.create(
                    model="grok-beta",  # Use "grok-4" se você tiver acesso liberado
                    messages=[
                        {"role": "system", "content": "Você é meu assistente pessoal. Fale em português brasileiro natural, amigável e útil. Responda tudo que eu perguntar."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=800,
                    temperature=0.8
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Ops, deu um erro: {str(e)}. Verifique se a API key está certa no secrets.toml.")
