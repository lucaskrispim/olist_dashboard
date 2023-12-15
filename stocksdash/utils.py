import pandas as pd
from sklearn.linear_model import LinearRegression

def getDataFrameByIndex(origin,subindex):

    # Selecionando colunas com o subíndice "VALE3.SA"
    df = origin.loc[:, origin.columns.get_level_values(1) == subindex]

    # Removendo o segundo nível do índice
    df.columns = df.columns.droplevel(1)

    return df

def getPctChange(origin,benchmark_column,asset_column):
    df = pd.DataFrame()

    df[benchmark_column] = origin["Close"][benchmark_column].pct_change()
    df[asset_column] = origin["Close"][asset_column].pct_change()

    df.dropna(inplace=True)

    return df

def getLinearCoef(df,benchmark,asset):
    # Colocando os dados no formato correto para a regressão
    X = df[benchmark].values.reshape(-1, 1)  # Eixo X
    y = df[asset].values  # Eixo Y

    # Criando o modelo de regressão linear
    model = LinearRegression()

    # Treinando o modelo com os dados
    model.fit(X, y)

    # Coeficientes da regressão
    coeficiente_angular = model.coef_
    intercepto = model.intercept_

    return coeficiente_angular,intercepto