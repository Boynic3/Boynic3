import os
import re

def gerar_estatisticas():
    # Aqui você pode usar a biblioteca 'requests' para buscar dados reais de APIs.
    # Por enquanto, vamos retornar um texto de exemplo.
    return """
    🎯 **Estatísticas do GitHub**
    * Repositórios: 15
    * Commits este ano: 342
    
    ![Gráfico](assets/graph_dijkstra.svg)
    """

def atualizar_readme():
    caminho_readme = 'README.md'
    
    # 1. Ler o README atual
    with open(caminho_readme, 'r', encoding='utf-8') as file:
        readme_conteudo = file.read()

    # 2. Gerar as novas estatísticas
    novas_stats = gerar_estatisticas()

    # 3. Substituir o conteúdo entre os marcadores
    # Lembre-se de colocar <!-- START_STATS --> e <!-- END_STATS --> no seu README!
    padrao = r'(<!-- START_STATS -->).*?(<!-- END_STATS -->)'
    novo_conteudo = re.sub(padrao, rf'\1\n{novas_stats}\n\2', readme_conteudo, flags=re.DOTALL)

    # 4. Salvar o README atualizado
    with open(caminho_readme, 'w', encoding='utf-8') as file:
        file.write(novo_conteudo)

if __name__ == "__main__":
    atualizar_readme()
    print("README atualizado com sucesso!")