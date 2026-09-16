import os
import re
import requests
from datetime import datetime

def gerar_estatisticas(usuario):
    # Fazendo a requisição para a API do GitHub
    url = f"https://api.github.com/users/{usuario}"
    resposta = requests.get(url)
    
    # Verificando se a requisição deu certo (código 200)
    if resposta.status_code == 200:
        dados = resposta.json()
        repositorios = dados.get("public_repos", 0)

        url_repos = f"https://api.github.com/users/{usuario}/repos?per_page=100"
        resposta_repos = requests.get(url_repos)
        estrelas = 0
        if resposta_repos.status_code == 200:
            repos_dados = resposta_repos.json()
            estrelas = sum(repo.get("stargazers_count", 0) for repo in repos_dados if isinstance(repo, dict))

        hoje = datetime.now().strftime("%Y-%m-%d")

#texto que vai pro readme
        return (
            "\nAtualizado diariamente por GitHub Actions.\n\n"
            "```shell\n"
            f"$ {usuario.lower()} --status\n"
            f"repositórios ...... {repositorios}\n"
            f"estrelas .......... {estrelas}\n\n"
            f"última atualização  {hoje} · auto via GitHub Actions\n"
            "```\n\n"
            "![Gráfico de Contribuições](assets/graph_dijkstra.svg)\n"
        )
        

    else:
        print(f"Erro ao acessar API: {resposta.status_code}")
        return "<!-- Erro ao carregar as estatísticas -->"

def atualizar_readme():
    caminho_readme = 'README.md'
    meu_usuario = "Boynic3" 
    
    # 1. Ler o README atual
    with open(caminho_readme, 'r', encoding='utf-8') as file:
        readme_conteudo = file.read()

    # 2. Buscar as novas estatísticas na API
    novas_stats = gerar_estatisticas(meu_usuario)

    # 3. Substituir o conteúdo entre os marcadores
    padrao = r'(<!-- START_STATS -->).*?(<!-- END_STATS -->)'
    novo_conteudo = re.sub(
        padrao, 
        lambda m: f"{m.group(1)}{novas_stats}{m.group(2)}", 
        readme_conteudo, 
        flags=re.DOTALL
    )

    # 4. Salvar o README atualizado
    with open(caminho_readme, 'w', encoding='utf-8') as file:
        file.write(novo_conteudo)

if __name__ == "__main__":
    atualizar_readme()
    print("README atualizado com sucesso usando dados reais da API!")