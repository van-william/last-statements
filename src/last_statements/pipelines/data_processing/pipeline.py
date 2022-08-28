"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import process_last_statements, transform_last_statements

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
            node(
                func=process_last_statements,
                inputs=["raw_last_statements", "params:statements_to_remove"],
                outputs="processed_last_statements",
                name="process_statements",
            ),
            node(
                func=transform_last_statements,
                inputs="processed_last_statements",
                outputs="transformed_last_statement",
                name="transform_statements",
            ),
    ])

