# Gráficos para a análise:

# Import de bibliotecas

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# criando arquivo csv

music = pd.read_csv('/config/workspace/NexusSong-trabalho/NexusSong/VisualizacaoDadosMatplotlib/data/music_streaming.csv') # arquivo a ser modificado
music_origin = pd.read_csv('/config/workspace/NexusSong-trabalho/NexusSong/VisualizacaoDadosMatplotlib/data/music_streaming.csv') # arquivo sem modificações

# Histograma de popularidade (share_count) por gênero

def criar_hist():
    """
    Cria um histograma para mostrar a distribuição do número de compartilhamentos (share_count) por gênero musical.
    A visualização inclui uma curva de densidade (KDE) e a distribuição é empilhada para diferentes gêneros.
    """
    sns.set(style="whitegrid") # Configurações gerais para o estilo dos gráficos
    global music
    plt.figure(figsize=(12, 6))
    sns.histplot(data=music, x='share_count', hue='genre', multiple="stack", kde=True)
    plt.title("Distribuição de Compartilhamentos por Gênero")
    plt.xlabel("Número de Compartilhamentos")
    plt.ylabel("Frequência")
    plt.show()

# Boxplot de popularidade (share_count) por gênero para identificar outliers

def criar_boxplot():
    """
    Cria um boxplot para mostrar a distribuição de compartilhamentos (share_count) por gênero musical.
    O boxplot ajuda a identificar possíveis outliers na quantidade de compartilhamentos.
    """
    sns.set(style="whitegrid") # Configurações gerais para o estilo dos gráficos
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=music, x='genre', y='share_count')
    plt.xticks(rotation=45)
    plt.title("Distribuição de Compartilhamentos por Gênero (Boxplot)")
    plt.xlabel("Gênero")
    plt.ylabel("Número de Compartilhamentos")

    return plt.show()

# Gráfico de Barras: Distribuição de músicas por gênero
def criar_barras_genero():
    """
    Cria um gráfico de barras para mostrar a distribuição de músicas por gênero.
    O gráfico mostra quantas músicas existem em cada gênero.
    """
    sns.set(style="whitegrid")
    global music
    plt.figure(figsize=(10, 6))
    sns.countplot(data=music, x='genre', order=music['genre'].value_counts().index)
    plt.xticks(rotation=45)
    plt.title("Distribuição de Músicas por Gênero")
    plt.xlabel("Gênero")
    plt.ylabel("Número de Músicas")

    return plt.show()


# Gráfico de Pizza: Distribuição percentual de músicas por gênero
def criar_pizza():
    """
    Cria um gráfico de pizza para mostrar a distribuição percentual de músicas por gênero.
    A pizza apresenta a proporção de cada gênero na totalidade das músicas.
    """
    sns.set(style="whitegrid")
    genre_counts = music['genre'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Distribuição Percentual de Músicas por Gênero")

    return plt.show()

# Analisando a popularidade de cada música por gênero

def analisar_popularidade():
    """
    Analisa a popularidade de músicas por gênero com base na duração média dos streams.
    O gráfico de barras exibe a média de duração dos streams para cada gênero musical.
    """
    # Calcular a média de duração de streams por gênero
    genre_avg_streams = music.groupby('genre')['duration_seconds'].mean().sort_values(ascending=False)
    # Exibir o resultado
    plt.figure(figsize=(10, 6))
    plt.bar(genre_avg_streams.index, genre_avg_streams.values, color='skyblue')
    plt.title('Média de Duração dos Streams por Gênero')
    plt.xlabel('Gênero Musical')
    plt.ylabel('Duração Média dos Streams (segundos)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    return plt.show()

# Analisando as músicas de estilos muito ouvidos

def analisar_outliers():
    """
    Identifica e exibe outliers na duração dos streams das músicas.
    Outliers são definidos como valores que estão mais de 3 desvios padrão acima da média.
    """
    # Calcular a média e o desvio padrão da duração dos streams
    mean_duration = music['duration_seconds'].mean()
    std_duration = music['duration_seconds'].std()
    # Definir um limite para outliers (aqui, 3 desvios padrão acima da média)
    threshold = mean_duration + 3 * std_duration
    # Identificar outliers
    outliers = music[music['duration_seconds'] > threshold]
    # Plotar os dados com os outliers destacados
    plt.figure(figsize=(12, 6))
    plt.scatter(music.index, music['duration_seconds'], color='lightgray', label='Normal')
    plt.scatter(outliers.index, outliers['duration_seconds'], color='red', label='Outliers')
    plt.axhline(y=threshold, color='blue', linestyle='--', label='Limite de Outlier')
    plt.title('Identificação de Outliers na Duração dos Streams')
    plt.xlabel('Index da Música')
    plt.ylabel('Duração do Stream (segundos)')
    plt.legend()
    plt.tight_layout()

    return plt.show(), outliers

# Analisando os estilos mais ouvidos mês a mês

def analisar_sazolalidade_mes():
    """
    Analisa a popularidade de estilos musicais mês a mês, com base na duração média dos streams.
    O gráfico de linhas exibe a variação da popularidade de cada gênero ao longo dos meses.
    """
    global music
    # Converter a coluna de data para o formato datetime se necessário
    music['date'] = pd.to_datetime(music['date'])
    # Extrair o mês da data
    music['month'] = music['date'].dt.month
    # Calcular a média de streams por mês para cada gênero
    monthly_popularity_genre = music.groupby(['month', 'genre'])['duration_seconds'].mean().unstack()
    # Visualizar os resultados
    print("Popularidade Mensal por Gênero:")
    print(monthly_popularity_genre)
    # Configurar o gráfico de linhas
    plt.figure(figsize=(10, 6))
    for genre in monthly_popularity_genre.columns:
        plt.plot(monthly_popularity_genre.index, monthly_popularity_genre[genre], label=genre)
    # Adicionar títulos e rótulos
    plt.title("Popularidade Mensal por Gênero (Duração Média dos Streams)")
    plt.xlabel("Mês")
    plt.ylabel("Duração Média (segundos)")
    plt.legend(title="Gênero")
    plt.grid(True)

    return plt.show()

# Analisando os feriados mais importantes, sendo 3 internacionais, um mais forte nos EUA e outro mais forte no Brasil

# Criar uma coluna indicando se é um feriado específico
music['date'] = pd.to_datetime(music['date'])
music['is_christmas'] = music['date'].dt.month == 12
music['is_new_year'] = music['date'].dt.month == 1
music['is_halloween'] = music['date'].dt.month == 10
music['is_easter'] = music['date'].dt.month == 4
music['is_carnaval'] = music['date'].dt.month == 2

# Exemplo de cálculo da popularidade em feriados específicos
christmas_popularity = music[music['is_christmas']].groupby('genre')['duration_seconds'].mean()
new_year_popularity = music[music['is_new_year']].groupby('genre')['duration_seconds'].mean()
easter_popularity = music[music['is_easter']].groupby('genre')['duration_seconds'].mean()
halloween_popularity = music[music['is_halloween']].groupby('genre')['duration_seconds'].mean()
carnaval_popularity = music[music['is_carnaval']].groupby('genre')['duration_seconds'].mean()


def plot_holiday_popularity(data, holiday_column, month, holiday_name):
    """
    Cria um gráfico de linha para mostrar a popularidade diária dos gêneros durante um feriado específico.
    O gráfico exibe a média de duração dos streams por dia para o mês e feriado fornecido.

    ARGS -> data: DataFrame, holiday_column: str, month: int, holiday_name: str
    Returns: gráfico de popularidade no feriado informado
    """
    # Filtrar o DataFrame para o mês e feriado específicos
    holiday_data = data[data[holiday_column] & (data['date'].dt.month == month)]
    # Agrupar por dia e gênero e calcular a média de duração
    daily_popularity = holiday_data.groupby([holiday_data['date'].dt.day, 'genre'])['duration_seconds'].mean().unstack()
    # Preencher valores ausentes com 0 para evitar saltos
    daily_popularity = daily_popularity.reindex(range(1, 32), fill_value=0)
    # Configurar o gráfico
    plt.figure(figsize=(12, 6))
    for genre in daily_popularity.columns:
        plt.plot(daily_popularity.index, daily_popularity[genre], label=genre)
    # Personalizar o gráfico
    plt.title(f"Popularidade Diária por Gênero em {holiday_name}")
    plt.xlabel("Dia do Mês")
    plt.ylabel("Duração Média (segundos)")
    plt.grid(True)
    # Ajustar o eixo X para mostrar os dias do mês
    plt.xticks(range(1, 32))
    # Ajustar a legenda para fora do gráfico
    plt.legend(title="Gênero", bbox_to_anchor=(1.05, 1), loc='upper left')
    # Exibir o gráfico
    plt.tight_layout()

    plt.show()

# Analisando os horários mais utilizados:

def verificar_horarios():
    """
    Cria um gráfico de barras que mostra a frequência de reproduções por hora do dia.
    Inclui uma linha que indica a média da frequência de reprodução.
    """
    # Extrair a coluna de horário e converter para o formato datetime se necessário
    music['time'] = pd.to_datetime(music['time'])

    # Extrair as horas dos timestamps
    music['hour'] = music['time'].dt.hour

    # Contabilizar a frequência de reproduções por hora
    hourly_counts = music['hour'].value_counts().sort_index()

    # Calcular a média de reproduções
    average_frequency = hourly_counts.mean()

    # Plotar o gráfico
    plt.figure(figsize=(12, 6))
    plt.bar(hourly_counts.index, hourly_counts.values, color='skyblue', alpha=0.7)
    plt.axhline(average_frequency, color='red', linestyle='--', label=f'Média: {average_frequency:.2f}')

    # Adicionar títulos e rótulos
    plt.title('Horários de Pico de Reprodução')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Frequência de Reprodução')
    plt.xticks(range(0, 24))
    plt.legend()

    # Mostrar o gráfico

    return plt.show()

def planos_mais_usados():
    """
    Função para gerar um gráfico de barras mostrando os tipos de assinatura mais utilizados.
    Conta a ocorrência de cada tipo de assinatura no conjunto de dados 'subscription_type'.
    """
    # Contar a ocorrência de cada tipo de assinatura
    subscription_counts = music['subscription_type'].value_counts()

    # Plotar o gráfico de barras
    plt.figure(figsize=(10, 6))
    subscription_counts.plot(kind='bar', color='skyblue')
    plt.title('Subscription Types Used by Users')
    plt.xlabel('Subscription Type')
    plt.ylabel('Number of Users')
    plt.xticks(rotation=45)
    return plt.show()

def motivos_pular():
    """
    Função para gerar um gráfico de barras dos motivos mais comuns para pular músicas.
    Conta a ocorrência de cada motivo de pular a música na coluna 'skip_reason'.
    """
    # Contar a ocorrência de cada motivo de pular a música
    skip_reasons = music['skip_reason'].value_counts()

    # Plotar o gráfico de barras dos motivos para pular músicas
    plt.figure(figsize=(10, 6))
    skip_reasons.plot(kind='bar', color='salmon')
    plt.title('Motivos pelos quais os usuários pulam músicas')
    plt.xlabel('Motivo')
    plt.ylabel('Número de Ocorrências')
    plt.xticks(rotation=45)
    plt.show()

# Analisando estilos mais populares por faixa etária:

def faixa_etaria(idade):
    """
    Função para classificar a faixa etária de um usuário baseado na sua idade.

    ARGS:
        idade (int): A idade do usuário.

    Returns:
        str: A faixa etária correspondente ao usuário.
    """
    if idade < 18:
        return 'Menor de 18'
    elif idade <= 24:
        return '18-24'
    elif idade <= 34:
        return '25-34'
    elif idade <= 44:
        return '35-44'
    elif idade <= 54:
        return '45-54'
    else:
        return '55+'

# Adicionar coluna de faixa etária
music['faixa_etaria'] = music['user_age'].apply(faixa_etaria)

# Análise de músicas mais populares (geral)
musicas_populares_geral = music.groupby('play_id').agg({
    'liked': 'sum', 'added_to_playlist': 'sum', 'share_count': 'sum'
}).sort_values(by=['liked', 'added_to_playlist', 'share_count'], ascending=False)

# Análise de músicas mais populares (por faixa etária)
musicas_populares_faixa = music.groupby(['faixa_etaria', 'play_id']).agg({
    'liked': 'sum', 'added_to_playlist': 'sum', 'share_count': 'sum'
}).sort_values(by=['faixa_etaria', 'liked', 'added_to_playlist', 'share_count'], ascending=False)

# Análise dos gêneros mais populares (geral)
generos_populares_geral = music.groupby('genre').agg({
    'liked': 'sum', 'added_to_playlist': 'sum', 'share_count': 'sum'
}).sort_values(by=['liked', 'added_to_playlist', 'share_count'], ascending=False)

# Análise dos gêneros mais populares (por faixa etária)
generos_populares_faixa = music.groupby(['faixa_etaria', 'genre']).agg({
    'liked': 'sum', 'added_to_playlist': 'sum', 'share_count': 'sum'
}).sort_values(by=['faixa_etaria', 'liked', 'added_to_playlist', 'share_count'], ascending=False)

# Análise dos subgêneros mais populares (geral)
subgeneros_populares_geral = music.groupby('subgenre').agg({
    'liked': 'sum', 'added_to_playlist': 'sum', 'share_count': 'sum'
}).sort_values(by=['liked', 'added_to_playlist', 'share_count'], ascending=False)

# Análise dos subgêneros mais populares (por faixa etária)
subgeneros_populares_faixa = music.groupby(['faixa_etaria', 'subgenre']).agg({
    'liked': 'sum', 'added_to_playlist': 'sum', 'share_count': 'sum'
}).sort_values(by=['faixa_etaria', 'liked', 'added_to_playlist', 'share_count'], ascending=False)

# criando gráficos:

def barras_faixa_etaria():
    """
    Função para gerar gráficos de barras que mostram a frequência de gêneros de música
    por faixa etária dos usuários.
    """
    # Filtrar dados para análise da frequência dos gêneros por faixa etária
    genero_faixa_etaria = music.groupby(['faixa_etaria', 'genre']).size().reset_index(name='frequencia')

    # Listar faixas etárias únicas para iterar e criar gráficos individuais
    faixas_etarias = genero_faixa_etaria['faixa_etaria'].unique()

    # Gerar gráficos de barra para cada faixa etária
    for faixa in faixas_etarias:
        plt.figure(figsize=(10, 6))
        faixa_data = genero_faixa_etaria[genero_faixa_etaria['faixa_etaria'] == faixa]
        plt.bar(faixa_data['genre'], faixa_data['frequencia'], color='skyblue')
        plt.title(f'Frequência de Gêneros para a Faixa Etária {faixa}')
        plt.xlabel('Gênero')
        plt.ylabel('Frequência')
        plt.xticks(rotation=45)
        plt.tight_layout()

    plt.show()

# Analisemos as corelações entre os estilos mais tocados

# Converter as colunas `liked` e `added_to_playlist` para inteiros (True = 1, False = 0)
music['liked'] = music['liked'].astype(int)
music['added_to_playlist'] = music['added_to_playlist'].astype(int)

# Selecionar as colunas relevantes para a análise de correlação
data_for_corr = music[['duration_seconds', 'liked', 'added_to_playlist', 'share_count']]

# Calcular a matriz de correlação
corr_matrix = data_for_corr.corr()

def gerar_heatmap():
    """
    Função para gerar um heatmap da matriz de correlação entre variáveis relacionadas
    ao comportamento de música, como 'duration_seconds', 'liked', 'added_to_playlist' e 'share_count'.
    """
    # Plotar o heatmap da matriz de correlação
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Heatmap de Correlação das Variáveis de Música")

    return plt.show()

def gerar_grafico_de_dispersao():
    """
    Função para gerar gráficos de dispersão para diferentes intervalos de duração de músicas,
    mostrando a relação entre a duração da música e o número de compartilhamentos.
    A função inclui linhas de tendência para cada gênero de música.
    """
    # Definindo os intervalos de duração de 50 em 50 segundos
    intervals = [(i, i + 50) for i in range(0, 501, 50)]
    # Definindo uma paleta de cores para os gêneros
    palette = sns.color_palette("deep", n_colors=music['genre'].nunique())

    # Iterando sobre os intervalos para criar gráficos separados
    for start, end in intervals:
        # Filtrando os dados para o intervalo atual
        subset = music[(music['duration_seconds'] >= start) & (music['duration_seconds'] < end)]
        # Criar uma nova figura para cada intervalo
        plt.figure(figsize=(10, 6))
        # Gráfico de dispersão para o intervalo atual
        scatter = sns.scatterplot(data=subset, x='duration_seconds', y='share_count', hue='genre', 
                                  alpha=0.6, s=100, palette=palette, edgecolor='w', linewidth=0.5)

        # Ajustar os eixos
        plt.xlim(start, end)
        plt.ylim(0, 3.5)  # Limite do eixo y de 0 a 3.5 para melhor visualização
        # Adicionar uma linha de tendência para cada gênero
        for idx, genre in enumerate(music['genre'].unique()):
            genre_subset = subset[subset['genre'] == genre]
            sns.regplot(x='duration_seconds', y='share_count', data=genre_subset, scatter=False, 
                        color=palette[idx], ci=None, line_kws={'linewidth': 2, 'alpha': 0.8})

        # Configurações do gráfico
        plt.title(f"Gráfico de Dispersão: Duração de {start} a {end} segundos", fontsize=16)
        plt.xlabel("Duração (segundos)", fontsize=14)
        plt.ylabel("Quantidade de Compartilhamentos", fontsize=14)
        plt.legend(title="Gênero", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()  # Ajusta o layout para evitar sobreposição

    return plt.show()  # Exibir o gráfico

# 1. Gráfico de linha mostrando tendências de popularidade ao longo do tempo
# Contando o número de streams por data
streams_over_time = music.groupby('date').size()

def gerar_num_stream_datas():
    """
    Função para gerar um gráfico de linha que mostra a tendência de popularidade das músicas
    ao longo do tempo, com base no número de streams por data.
    """
    plt.figure(figsize=(15, 6))
    plt.plot(streams_over_time.index, streams_over_time.values, marker='o', color='b', linestyle='-')
    plt.title('Tendência de Popularidade ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Número de Streams')
    plt.xticks(rotation=45)
    plt.tight_layout()

    return plt.show()

# 2. Análise de plataformas mais utilizadas
platform_counts = music['platform'].value_counts()

def gerar_plataforma_mais_utilizadas():
    """
    Função para gerar um gráfico de barras mostrando as plataformas mais utilizadas pelos usuários
    com base no número de streams.
    """
    plt.figure(figsize=(10, 6))
    platform_counts.plot(kind='bar', color='skyblue')
    plt.title('Plataformas Mais Utilizadas')
    plt.xlabel('Plataforma')
    plt.ylabel('Número de Streams')
    plt.xticks(rotation=0)
    plt.tight_layout()

    return plt.show()

# 3. Análise dos dispositivos mais utilizados
device_counts = music['preferred_device'].value_counts()

def gerar_dispositivos_mais_utilizados():
    """
    Função para gerar um gráfico de barras mostrando os dispositivos mais utilizados pelos usuários
    com base no número de streams.
    """
    plt.figure(figsize=(10, 6))
    device_counts.plot(kind='bar', color='coral')
    plt.title('Dispositivos Mais Utilizados')
    plt.xlabel('Dispositivo')
    plt.ylabel('Número de Streams')
    plt.xticks(rotation=0)
    plt.tight_layout()

    return plt.show()

# 4. Análise da qualidade de streaming mais utilizada
quality_counts = music['stream_quality'].value_counts()

def gerar_qualidade_mais_utilizada():
    """
    Função para gerar um gráfico de barras mostrando a qualidade de streaming mais utilizada pelos usuários
    com base no número de streams.
    """
    plt.figure(figsize=(10, 6))
    quality_counts.plot(kind='bar', color='lightgreen')
    plt.title('Qualidade de Streaming Mais Utilizada')
    plt.xlabel('Qualidade de Streaming')
    plt.ylabel('Número de Streams')
    plt.xticks(rotation=0)
    plt.tight_layout()

    return plt.show()