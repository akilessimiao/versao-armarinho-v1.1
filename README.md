# Versão Armarinho v1.1 - Sistema de Vendas

Sistema de vendas (PDV) simples e funcional para armarinhos/lojas pequenas, desenvolvido em **Python + Flask + SQLite**. Inspirado em necessidades reais de controle de vendas rápidas, com emissão de cupom, backups automáticos e proteção administrativa.

![Screenshot do Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Sistema+de+Vendas)  
*(Adicione uma screenshot real aqui depois – tire print do dashboard logado como operador/admin)*

## Funcionalidades Implementadas

- **Login com níveis de acesso** (admin / operador)
- **Dashboard diferenciado** por perfil:
  - Admin: Configuração de APIs de pagamento, backups, relatórios
  - Operador: Consulta de produtos, emissão de cupom, nova venda
- **Backup automático e manual** (diário às 23:00, histórico, restauração, exportação JSON)
- **Leitura Z** (relatório fiscal simplificado: totais do dia, sangrias, top 10 produtos, export PDF)
- **Emissão de cupom fiscal/não fiscal** (layout otimizado para impressora térmica 80mm, reimpressão)
- **Proteção administrativa** (senha para ações sensíveis como exclusão – padrão: *java1814*)
- **Pesquisa de vendas** (por número de cupom, cliente ou horário – segunda via)
- **Interface responsiva** com atalhos de teclado e notificações
- **Configuração de API de pagamentos** (Mercado Pago PIX/cartão – em andamento)

**Funcionalidades planejadas / em desenvolvimento**:
- Integração PIX/Cartão (Mercado Pago, PagSeguro)
- Envio automático de cupom via WhatsApp (Twilio ou API oficial)
- Carrinho de vendas completo (adicionar/remover itens, selecionar cliente)
- Geração de PDF profissional para cupom (com reportlab)
- Cadastro de produtos e clientes
- Gráficos no dashboard (vendas diárias/mensais)

## Tecnologias Utilizadas

- **Backend**: Python 3 + Flask + SQLAlchemy (SQLite)
- **Frontend**: HTML5 + CSS3 + Jinja2 (templates)
- **Outras bibliotecas**:
  - reportlab (PDF)
  - twilio (WhatsApp futuro)
  - mercadopago (pagamentos)
  - schedule (backups automáticos)

Veja a lista completa em [`requirements.txt`](requirements.txt).

## Como Instalar e Executar (Localmente)

1. **Clone o repositório**
   ```bash
   git clone https://github.com/akilessimiao/versao-armarinho-v1.1.git
   cd versao-armarinho-v1.1

Crie e ative o ambiente virtual (recomendado)Bashpython -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
Instale as dependênciasBashpip install -r requirements.txt
Execute o sistemaBashpython app.py
Acesse no navegador: http://127.0.0.1:5000/

Credenciais iniciais
Admin: usuário admin / senha admin
Operador: usuário operador / senha operador123
Senha administrativa para ações sensíveis: java1814


Atenção: O banco de dados é SQLite local (sistema_vendas.db). Faça backup antes de testes pesados!
Como Usar (Principais Fluxos)

Login → Escolha admin ou operador
Operador → Consulta produtos + Iniciar nova venda/emissão de cupom
Admin → Configurar API pagamentos + Backup + Pesquisar vendas
Cupom → Após finalizar venda, gera cupom com nome da empresa (configurável)
Backup → Automático diário ou manual via botão

Para impressora térmica: configure o navegador para impressão sem margens/cabeçalho (layout 80mm).
Contribuição
Sinta-se à vontade para abrir issues ou pull requests! Ideias bem-vindas:

Integração WhatsApp
Suporte a múltiplos usuários
Relatórios avançados
Deploy em nuvem (Railway, Render, Heroku)

Licença
MIT License – Veja LICENSE (crie o arquivo se não existir).
Desenvolvido por LDT NET – Natal/RN – 2026
Qualquer dúvida: abra uma issue aqui no GitHub!
text### Dicas para melhorar ainda mais

- **Adicione imagens reais**:
  - Tire prints do login, dashboard operador/admin, tela de cupom.
  - Suba para o repositório (ex: crie pasta `docs/screenshots/`) e atualize os links no README (ex: `![Dashboard](docs/screenshots/dashboard.png)`).
- **Crie um LICENSE**: No GitHub, clique em "Add file" → "Create new file" → nome `LICENSE` → escolha MIT.
- **Atualize a descrição do repositório** (no GitHub, em "About"):  
  "Sistema de vendas/PDV para armarinhos em Flask/Python – cupons, backups, leitura Z e mais."
- **Adicione badges** (opcional, fica bonito):
  ```markdown
  [![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Flask-3.0-orange)](https://flask.pal   