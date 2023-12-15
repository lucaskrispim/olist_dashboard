# plotly_app/views.py
from django.shortcuts import render
import plotly.graph_objs as go
from plotly.offline import plot
import yfinance as yf
from .graph import *
from .indicators import *
from .utils import *
import os

def plotly_view(request):

    dir_path = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(dir_path, "olist_marketing_qualified_leads_dataset.csv")

    df = pd.read_csv(file_path)

    file_path2 = os.path.join(dir_path, "olist_closed_deals_dataset.csv")

    df2 = pd.read_csv(file_path2)

    merged_df = pd.merge(df, df2, on='mql_id', how='inner')

    # Descartando colunas com alta porcentagem de dados faltantes
    cols_to_drop = ['has_company', 'has_gtin', 'average_stock', 'declared_product_catalog_size']
    merged_df.drop(columns=cols_to_drop, inplace=True)

    # Imputando dados faltantes com a moda para as colunas restantes
    cols_to_fill = ['lead_behaviour_profile', 'origin', 'business_type', 'lead_type', 'business_segment']
    for col in cols_to_fill:
        mode_value = merged_df[col].mode()[0]
        merged_df[col].fillna(mode_value, inplace=True)

    merged_df2 = df.merge(df2, on='mql_id', how='left')

    # Convertendo as datas para formato datetime
    merged_df['first_contact_date'] = pd.to_datetime(merged_df['first_contact_date'])
    merged_df['won_date'] = pd.to_datetime(merged_df['won_date'])

    # Calculando a diferença em dias entre as datas
    merged_df['conversion_time'] = (merged_df['won_date'] - merged_df['first_contact_date']).dt.days

    merged_df['conversion_time'] = (merged_df['won_date'] - pd.to_datetime(merged_df['first_contact_date'])).dt.days

    plot_div = create_bar_chart(merged_df, 'origin', title='Contagem de Origens da origin dos leads', x_label='X', y_label='Y', x_tickangle=0)

    plot_div2 = create_line_chart(merged_df, 'conversion_time', title='Tempo Médio de Conversão por Mês', x_label='Mês', y_label='Dias', x_tickangle=0)

    plot_div3 = create_bar_chart2(merged_df, 'conversion_time','business_segment', title='Tempo Médio de Conversão por Segmento de Mercado', x_label='Dias', y_label='Segmento', x_tickangle=0)

    plot_div4 = create_bar_chart2(merged_df, 'conversion_time','lead_behaviour_profile', title='Tempo Médio de Conversão por Perfil de Comportamento', x_label='Dias', y_label='Perfil do cliente', x_tickangle=0)

    plot_div5 = create_heat_map(merged_df2)

    return render(request, 'index.html',context={'plot_div': plot_div3,'plot_div2':plot_div2,'plot_div3':plot_div,'plot_div4':plot_div4,'plot_div5':plot_div5})
