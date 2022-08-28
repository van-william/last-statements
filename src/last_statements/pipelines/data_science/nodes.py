"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.2
"""
from typing import Dict
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


def kmeans_single(df: pd.DataFrame, df_statements:pd.DataFrame, n_clust: int) -> pd.DataFrame:
    """transforms last statements using tf-idf and other manipulations.
    Args:
        Processed DataFrame of Last Statements
    Returns:
        Transformed Matrix for Clustering
    """

    modelkmeans = KMeans(n_clusters=n_clust, init='k-means++', n_init=100)
    clusters = modelkmeans.fit_predict(df)
    df_statements['cluster'] = clusters
    return df_statements, modelkmeans 


def kmeans_optimize(df: pd.DataFrame, df_statements:pd.DataFrame, min_clusters: int, max_clusters: int) -> pd.DataFrame:
    """transforms last statements using tf-idf and other manipulations.
    Args:
        Processed DataFrame of Last Statements
    Returns:
        Transformed Matrix for Clustering
    """
    silhouette_list = []
    K = list(range(min_clusters, max_clusters+1))
    for k in K:
        clusterer = KMeans(n_clusters=k)
        cluster_labels = clusterer.fit_predict(df)
        silhouette_avg = silhouette_score(df, cluster_labels)
        silhouette_list.append(silhouette_avg)
    df_sil = pd.DataFrame(list(zip(K, silhouette_list)), columns =['k', 'sil_score'])
    df_sil.sort_values(by='sil_score', inplace=True, ascending=False)
    optimal_k = df_sil.iloc[0,0]
    modelkmeans = KMeans(n_clusters=optimal_k, init='k-means++', n_init=100)
    clusters = modelkmeans.fit_predict(df)
    df_statements['cluster'] = clusters
    return df_statements

def plot_pca(df: pd.DataFrame, parameters: Dict) -> None:
    plt.close('all')
    pca_2 = PCA(n_components=2)
    pca_2_df = pd.DataFrame(data = pca_2.fit_transform(df), columns = ['PC2_1', 'PC2_2'])
    sns.scatterplot(x='PC2_1', y='PC2_2', data=pca_2_df)

    image_name = parameters[0]['pca_plot']
    
    plt.savefig('./data/08_reporting/'+image_name, pad_inches=0.5)
    plt.close('all')
    return None