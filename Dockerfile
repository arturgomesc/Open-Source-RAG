FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para o contêiner
COPY . .

# Defina a variável de ambiente para o token do Hugging Face
# Certifique-se de substituir "seu_token_aqui" pelo seu verdadeiro token
ENV HUGGINGFACEHUB_API_TOKEN=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

# Exponha a porta que o Streamlit usa
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["streamlit", "run", "streamlit.py"]