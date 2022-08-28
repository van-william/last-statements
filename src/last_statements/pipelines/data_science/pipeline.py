"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import kmeans_single, kmeans_optimize, plot_pca


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
            node(
                func=kmeans_single,
                inputs=["transformed_last_statement", "processed_last_statements", "params:n_clust"],
                outputs=["n_cluster_output", "kmeans_model"],
                name="process_specific_n_kmeans_clusters",
            ),
            node(
                func=kmeans_optimize,
                inputs=["transformed_last_statement", "processed_last_statements", "params:min_clusters", "params:max_clusters"],
                outputs="optimal_cluster_output",
                name="process_optimal_kmeans_clusters",
            ),
            node(
                func=plot_pca,
                inputs=["transformed_last_statement", "params:visualization_names"],
                outputs=None,
                name="visualize_pca_2d",
            ),

    ])

