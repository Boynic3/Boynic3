import os
import re
import requests
from datetime import datetime

# Configurações
USUARIO = "Boynic3"
ARQUIVO_SVG = "assets/terminal_stats.svg"
ARQUIVO_README = "README.md"

def buscar_dados_avancados(token):
    # Usando a API GraphQL do GitHub para dados mais precisos
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}"}
    
    query = """
    query {
      user(login: "%s") {
        repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
          totalCount
        }
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          totalCount
          nodes {
            stargazers {
              totalCount
            }
          }
        }
      }
    }
    """ % USUARIO

    resposta = requests.post(url, json={'query': query}, headers=headers)
    
    if resposta.status_code == 200:
        dados = resposta.json()['data']['user']
        
        # Extraindo os dados
        repos = dados['repositories']['totalCount']
        commits = dados['contributionsCollection']['totalCommitContributions'] + dados['contributionsCollection']['restrictedContributionsCount']
        contribuicoes = dados['repositoriesContributedTo']['totalCount']
        estrelas = sum(node['stargazers']['totalCount'] for node in dados['repositories']['nodes'])
        
        # Nota: Linhas de código (LOC) exige chamadas complexas para cada repositório.
        # Estamos simulando um valor aqui. Para o cálculo real, seria necessário
        # implementar um sistema de cache igual ao arquivo cache/loc_cache.json do Daniel.
        loc_estimado = (commits * 45) + 1200 
        
        return repos, commits, estrelas, contribuicoes, loc_estimado
    else:
        print("Erro na API GraphQL. Verifique seu Token.")
        return 0, 0, 0, 0, 0

def gerar_svg(repos, commits, estrelas, contribuicoes, loc):
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    # Template do SVG imitando um terminal Bash
    svg = f"""<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" rx="8" fill="#0D1117" stroke="#30363D" stroke-width="1"/>
    
    <!-- Botões da Janela -->
    <circle cx="20" cy="20" r="6" fill="#FF5F56" />
    <circle cx="40" cy="20" r="6" fill="#FFBD2E" />
    <circle cx="60" cy="20" r="6" fill="#27C93F" />
    
    <!-- Texto do Terminal -->
    <g font-family="Courier New, monospace" font-size="14">
        <text x="20" y="65" fill="#58A6FF" font-weight="bold">$ {USUARIO.lower()} --status</text>
        
        <text x="20" y="95" fill="#C9D1D9">repositórios ...... <tspan fill="#79C0FF">{repos}</tspan></text>
        <text x="20" y="120" fill="#C9D1D9">commits ........... <tspan fill="#79C0FF">{commits}</tspan></text>
        <text x="20" y="145" fill="#C9D1D9">estrelas .......... <tspan fill="#79C0FF">{estrelas}</tspan></text>
        <text x="20" y="170" fill="#C9D1D9">contribuiu em ..... <tspan fill="#79C0FF">{contribuicoes} projetos</tspan></text>
        <text x="20" y="195" fill="#C9D1D9">linhas de código .. <tspan fill="#79C0FF">~{loc}</tspan></text>
        
        <text x="20" y="235" fill="#8B949E" font-size="12">última atualização  {hoje} · auto via GitHub Actions</text>
    </g>
</svg>"""

    with open(ARQUIVO_SVG, "w", encoding="utf-8") as file:
        file.write(svg)

def atualizar_readme():
    with open(ARQUIVO_README, 'r', encoding='utf-8') as file:
        readme = file.read()

    # Substitui a sessão antiga pela chamada da imagem SVG
    novo_conteudo = "\n<p align=\"center\">\n  <img src=\"assets/terminal_stats.svg\" alt=\"Estatísticas do GitHub\" />\n</p>\n"
    
    padrao = r'(<!-- START_STATS -->).*?(<!-- END_STATS -->)'
    readme_atualizado = re.sub(
        padrao, 
        lambda m: f"{m.group(1)}{novo_conteudo}{m.group(2)}", 
        readme, 
        flags=re.DOTALL
    )

    with open(ARQUIVO_README, 'w', encoding='utf-8') as file:
        file.write(readme_atualizado)

if __name__ == "__main__":
    # O script busca o token configurado nas variáveis de ambiente do Actions
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("Erro: Token do GitHub não encontrado.")
        exit(1)
        
    print("Buscando dados avançados...")
    repos, commits, estrelas, contribuicoes, loc = buscar_dados_avancados(token)
    
    print("Gerando SVG...")
    gerar_svg(repos, commits, estrelas, contribuicoes, loc)
    
    print("Atualizando README...")
    atualizar_readme()
    print("Sucesso!")