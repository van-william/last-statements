"""
This is a boilerplate pipeline 'data_extraction'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import extract_names, extract_statements


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
            node(
                func=extract_names,
                inputs="params:web_scraping_URL",
                outputs="name_lookup_table",
                name="extract_names_node",
            ),
            node(
                func=extract_statements,
                inputs="name_lookup_table",
                outputs="raw_last_statements",
                name="extract_statements_node",
            ),
    ])
