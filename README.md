## Este código realiza o processamento de linguagem natural para identificar a intenção do usuário a partir de perguntas.

### Primeiro, os dados das conversas anteriores são carregados de um arquivo JSON. 
### Em seguida, um vetorizador e um modelo de agrupamento são inicializados. 
### As colunas para pergunta e resposta são criadas a partir dos dados carregados. 
### O vetor das perguntas é criado usando o vetorizador e o modelo é ajustado aos dados. 
### Uma função é definida para identificar a intenção do usuário com base no cluster da pergunta. 
### A remoção de stopwords e o stemming em português são aplicados à pergunta original do usuário. 
### A intenção do usuário é identificada com base na semelhança da pergunta com as conversas anteriores. 
### Se nenhuma resposta for encontrada, uma função para tratar perguntas incomuns é chamada para identificar as palavras-chave na pergunta original e procurar por respostas relacionadas às palavras-chave. 
### Por fim, a pergunta original e sua resposta são salvas em um arquivo JSON.

# Para melhorias futuras

Ajeitar arquivo json, o codigo ao executar muda a estrutura do arquivo conversation.json que no caso não era para mudar e sim para manter a estrutura sem alterar do arquivo Estrutura.json.
