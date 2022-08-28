"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from .pipelines import data_extraction as de
from .pipelines import data_processing as dp
from .pipelines import data_science as ds


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    data_extraction_pipeline = de.create_pipeline()
    data_processing_pipeline = dp.create_pipeline()
    data_science_pipeline = ds.create_pipeline()
    
    return {
        "__default__": data_extraction_pipeline + data_processing_pipeline + data_science_pipeline,
        "de": data_extraction_pipeline,
        "dp": data_processing_pipeline,
        "ds": data_science_pipeline
        }
