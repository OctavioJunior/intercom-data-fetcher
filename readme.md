
# **Intercom Data Fetcher**

Este projeto automatiza o processo de busca de conversas de uma api, enriquece os dados dos contatos e os salva em arquivos CSV e JSON para subir para o Google Drive.

## **Sobre o Projeto**

O **Intercom Data Fetcher** é um script Python projetado para facilitar a extração e armazenamento de conversas e dados de clientes a partir da API do Intercom. Ele permite que você busque conversas baseadas em um intervalo de datas, obtenha detalhes dos contatos relacionados a essas conversas e armazene os resultados em arquivos CSV e JSON para fazer upload para o um drive.

Este projeto foi desenvolvido para ser rodado tanto como um script Python quanto como um executável independente, o que facilita a automação e agendamento de tarefas no seu sistema operacional.

## **Funcionalidades**

- **Busca de Conversas**: Busca todas as conversas na api da Intercom para um intervalo de datas especificado.
- **Enriquecimento de Dados**: Recupera detalhes sobre os contatos envolvidos nas conversas.
- **Exportação**: Salva os dados em formatos CSV e JSON.
- **Automação**: Possibilidade de agendar o script para rodar automaticamente, por exemplo, com integração ao Agendador de Tarefas do Windows.
- **Upload dos Arquivos**: Faz o uploaad dos arquivos para o Google Drive.
- **Autenticação Segura**: Carrega o token da API e url's de forma segura a partir de um arquivo `.env`.

## **Tecnologias Utilizadas**

- **Python 3.7+**
- **PyInstaller** (para criar executáveis)
- **requests** (para interagir com a API do Intercom)
- **dotenv** (para carregar variáveis de ambiente)
- **Pandas** (para manipulação e exportação de dados)
- **Logging** (para monitoramento e registro de eventos)
- **Google Drive API** (para upload dos arquivos)

## **Instalação**

### Requisitos

1. Python 3.7 ou superior.
2. Acesso à API da Intercom (token de autenticação e url's).
3. Acesso à API do Google Drive (token de autenticação).

### Passos para Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/OctavioJunior/intercom-data-fetcher.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd intercom-data-fetcher
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   INTERCOM_TOKEN=token_para_acesso_a_api
   API_URL_CONVERSATION=url_para_pegar_as_conversas
   API_URL_CONTACTS=url_para_buscar_dados_dos_contatos
   API_URL_AUTH=url_para_verificar_token
   RESULTS_PER_PAGE=de_20_a_150_registros_por_pagina
   ```

## **Como Usar**

1. **Rodar o Script Manualmente**:
   Para rodar o script manualmente, basta executar o arquivo `main.py`:

   ```bash
   python main.py
   ```

2. **Gerar Executável**:
   Se você deseja rodar o script como um executável, você pode gerar o arquivo com o comando do PyInstaller:

   ```bash
   pyinstaller --onefile --add-data ".env;." main.py --name "intercom_data_fetcher"
   ```

   Isso irá criar o arquivo executável `intercom_data_fetcher.exe` na pasta `dist`.

3. **Agendar o Script para Rodar Automaticamente**:
   Você pode usar o **Agendador de Tarefas do Windows** para rodar o script diariamente ou conforme necessário. Ao agendar, lembre-se de apontar para o caminho correto do executável ou do script Python.

   Para rodar o script diariamente, adicione uma nova tarefa e configure a frequência e o comando de execução:

   - **Comando**: `C:\path\to\intercom_data_fetcher.exe` ou `python C:\path\to\main.py`
   - **Argumentos**: `C:\path\to\.env_file`

## **Estrutura do Projeto**

```
intercom-data-fetcher/
│
├── .env               # Arquivo com as variáveis de ambiente
├── main.py            # Arquivo principal para execução do script
├── auth.py            # Funções para autenticação na API do Intercom
├── api_intercom.py    # Funções para buscar conversas e contatos na API
├── save_file.py       # Funções para salvar os dados em CSV e JSON
├── fetch_clients.py   # Funções para buscar clientes na API
├── upload_to_drive.py # Funções para fazer upload dos arquivos para o Google Drive
├── csv_converter.py   # Funções para converter dados em CSV
├── requirements.txt   # Lista de dependências do projeto
├── README.md          # Documentação do projeto
├── logging_config.py  # Configuração do logging
├── date_utils.py      # Funções para manipulação de datas
├── credentials.json   # Arquivo de credenciais para autenticação na API do Google Drive
├── tokenn.pickle      # Arquivo para armazenar o token de autenticação
├── .gitignore         # Arquivo para ignorar arquivos e diretórios específicos no Git
```

## **Exemplo de Execução**

Ao rodar o script, você verá o seguinte processo sendo executado:

1. O script buscará as conversas na Intercom para o intervalo de datas de ontem.
2. Ele buscará detalhes de cada contato envolvido nas conversas.
3. Os dados serão salvos em arquivos `<data>_conversations.csv` e `<data>_conversations.json`.
4. Os arquivos serão enviados para o Google Drive.
5. Logs serão gerados para indicar o progresso e qualquer erro ocorrido.

## **Contribuindo**

Se você deseja contribuir para o projeto, fique à vontade para fazer um **fork** do repositório, criar uma branch, realizar as modificações e enviar um **pull request**. 

Certifique-se de seguir as convenções de código e adicionar testes, se necessário.

## **Licença**

Este projeto é licenciado sob a [MIT License](LICENSE).

---