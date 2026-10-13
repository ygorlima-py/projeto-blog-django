1. Separar o agente da CLI (`main` como serviço).
2. Configurar um checkpointer persistente.
3. Criar o Celery no `agent_app`.
4. Criar a task que executa o agente e o `astream`.
5. Integrar o envio das respostas ao Telegram no worker.
6. Criar a API/webhook Django para receber mensagens e enfileirar tasks.
7. Criar o fluxo de aprovação no Telegram e a task de `Command(resume=...)`.
8. Testar o fluxo completo e fazer o deploy.