import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencias)

    df_recuperacao = df_ocorrencias[['cisp', 'recuperacao_veiculos']]
    
    df_recuperacao = df_recuperacao.groupby('cisp', as_index=False)['recuperacao_veiculos'].sum()

    df_recuperacao = df_recuperacao.sort_values(by='recuperacao_veiculos', ascending=False)
    
    print(df_recuperacao.head(20))


except Exception as e:
    print(f'Erro ao obter os dados - {e}')




try:
    array_recuperacao = np.array(df_recuperacao['recuperacao_veiculos'])

    media = np.mean(array_recuperacao)
    mediana = np.median(array_recuperacao)
    distancia_media_mediana = abs((media - mediana) / mediana * 100)
    
    print(30*'-')
    print('\nMedidas de Tendência Central')
    print(f'Média: {media}')
    print(f'Mediana: {mediana}')
    print(f'Distância: {distancia_media_mediana:.2f}%')

    print(30*'-')
    print(f'\nSeparando os quartis...')
    q1 = np.quantile(array_recuperacao, .25)
    q2 = np.quantile(array_recuperacao, .50)
    q3 = np.quantile(array_recuperacao, .75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    

    # Cidades c/ menos ocorrências de roubos
    df_recuperacao_menores = df_recuperacao[
        df_recuperacao['recuperacao_veiculos'] < q1
    ]

    # Cidades c/ maiores ocorrências de roubos
    df_recuperacao_maiores = df_recuperacao[
        df_recuperacao['recuperacao_veiculos'] > q3
    ]
    print(30*'-')
    print('\nDelegacias com menores ocorrências de recuperação de veículos')
    print(df_recuperacao_menores.tail(10))
    print('\nDelegacias com maiores ocorrências de recuperação de veículos')
    print(df_recuperacao_maiores.head(10))

    print(30*'-')
    print('\nCalculando a Amplitude Total')
    maximo = np.max(array_recuperacao) 
    minimo = np.min(array_recuperacao)
    amplitude = maximo - minimo
    
    print(f'Máximo de recuperações: {maximo}')
    print(f'Mínimo de recuperações: {minimo}')
    print(f'Amplitude Total: {amplitude}')
    print(30*'-')


    assimetria = df_recuperacao['recuperacao_veiculos'].skew()
    
    curtose = df_recuperacao['recuperacao_veiculos'].kurtosis()

    print(30*'-')
    print('\nAnalisando a Distribuição:')
    print(30*'-')
    print(f'Assimetria: {assimetria:.2f}')
    print(f'Curtose: {curtose:.2f}')
    
    
    if assimetria > 1:
        print("-> Assimetria Positiva Alta: Existem delegacias com números muito altos puxando a média para cima.")
    elif assimetria < -1:
        print("-> Assimetria Negativa Alta: Existem delegacias com números muito baixos puxando a média para baixo.")
    else:
        print("-> Distribuição tendendo à simetria.")
        
    if curtose > 0.5:
        print("-> Curtose Leptocúrtica: Valores extremos (outliers) têm grande influência no total.")


    iqr = q3 - q1

    limite_superior = q3 + (1.5 * iqr)

    limite_inferior = q1 - (1.5 * iqr)


    print(f'\nLimite Superior: {limite_superior}')
    print(f'\nLimite Inferior: {limite_inferior}')

    
    df_recuperacao_outliers_menores = (
        df_recuperacao[df_recuperacao['recuperacao_veiculos'] < limite_inferior]
    )

    print('\nDelegacias com outliers inferiores')
    print(30*'-')
    if len(df_recuperacao_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_recuperacao_outliers_menores)
    

    df_recuperacao_outliers_maiores = (
        df_recuperacao[df_recuperacao['recuperacao_veiculos'] > limite_superior]
    )

    print('\nDelegacias com outliers superiores')
    print(30*'-')
    if len(df_recuperacao_outliers_maiores) == 0:
        print('Não há outliers Superiores')
    else:
        print(df_recuperacao_outliers_maiores)





except Exception as e:
    print(f'Erro ao obter medidas - {e}')


try:
    
    print('\nGerando o Painel Visual (Dashboard)...')
    
   
    plt.figure(figsize=(18, 12))

    
    plt.subplot(2, 2, 1)
    
    plt.boxplot(array_recuperacao, orientation='horizontal', showmeans=True, patch_artist=True, 
                boxprops=dict(facecolor='lightblue'))
    plt.title('Distribuição das Recuperações (Boxplot)', fontsize=14)
    plt.xlabel('Quantidade de Recuperações', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    
    plt.subplot(2, 2, 2)
    plt.text(0.05, 0.95, f'Limite Inferior: {limite_inferior:.2f}', fontsize=12)
    plt.text(0.05, 0.88, f'Mínimo: {minimo}', fontsize=12)
    plt.text(0.05, 0.81, f'Q1: {q1}', fontsize=12)
    plt.text(0.05, 0.74, f'Q2 (Mediana): {q2}', fontsize=12)
    plt.text(0.05, 0.67, f'Q3: {q3}', fontsize=12)
    plt.text(0.05, 0.60, f'Limite Superior: {limite_superior:.2f}', fontsize=12)
    plt.text(0.05, 0.53, f'Máximo: {maximo}', fontsize=12)
    
    plt.text(0.05, 0.40, f'Média: {media:.2f}', fontsize=12, fontweight='bold', color='green')
    plt.text(0.05, 0.33, f'IQR (Intervalo Interquartil): {iqr:.2f}', fontsize=12)
    plt.text(0.05, 0.26, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.text(0.05, 0.19, f'Distância Média-Mediana: {distancia_media_mediana:.2f}%', fontsize=12, color='red')
    
    
    plt.title('Resumo Estatístico', fontsize=14)
    plt.axis('off') 

    plt.subplot(2, 2, 3)
    
    plt.hist(array_recuperacao, bins=30, edgecolor='black', color='skyblue')
    plt.axvline(media, color='green', linewidth=2, label=f'Média ({media:.0f})')
    plt.axvline(mediana, color='orange', linewidth=2, label=f'Mediana ({mediana:.0f})')
    plt.title('Frequência de Recuperações por Delegacia', fontsize=14)
    plt.xlabel('Quantidade de Recuperações', fontsize=12)
    plt.ylabel('Nº de Delegacias', fontsize=12)
    plt.legend()

    
    plt.subplot(2, 2, 4)
    
    df_top10 = df_recuperacao.head(10).sort_values(by='recuperacao_veiculos', ascending=True)
    
    
    plt.bar(df_top10['cisp'].astype(str), df_top10['recuperacao_veiculos'], color='darkred')
    plt.title('Top 10 Delegacias com Mais Recuperações', fontsize=14)
    plt.xlabel('Delegacia (CISP)', fontsize=12)
    plt.ylabel('Total de Recuperações', fontsize=12)
    plt.xticks(rotation=45)

    
    plt.suptitle('Painel de Análise: Recuperação de Veículos no RJ', fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    
    plt.show()


except Exception as e:
    print(f'Erro ao gerar o gráfico - {e}')