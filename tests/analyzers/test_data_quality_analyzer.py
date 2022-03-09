from datetime import datetime

import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.analyzers.data_quality_analyzer import FeatureQualityStats
from evidently.analyzers.utils import process_columns

import pytest


@pytest.mark.parametrize(
    "dataset, expected_metrics",
    [
        (
            pd.DataFrame({"numerical_feature": []}),
            FeatureQualityStats(
                feature_type="num",
                count=0,
                percentile_25=None,
                percentile_50=None,
                percentile_75=None,
                infinite_count=None,
                infinite_percentage=None,
                max=None,
                min=None,
                mean=None,
                missing_count=None,
                missing_percentage=None,
                most_common_value=None,
                most_common_value_percentage=None,
                std=None,
                unique_count=None,
                unique_percentage=None,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
            ),
        ),
        (
            pd.DataFrame({"numerical_feature": [np.nan, np.nan, np.nan, np.nan]}),
            FeatureQualityStats(
                feature_type="num",
                count=0,
                percentile_25=np.nan,
                percentile_50=np.nan,
                percentile_75=np.nan,
                infinite_count=0,
                infinite_percentage=0,
                max=np.nan,
                min=np.nan,
                mean=np.nan,
                missing_count=4,
                missing_percentage=100,
                most_common_value=np.nan,
                most_common_value_percentage=100,
                std=np.nan,
                unique_count=0,
                unique_percentage=0,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
            ),
        ),
        (
            pd.DataFrame({"numerical_feature": [np.nan, 2, 2, 432]}),
            FeatureQualityStats(
                feature_type="num",
                count=3,
                infinite_count=0,
                infinite_percentage=0.0,
                missing_count=1,
                missing_percentage=25,
                unique_count=2,
                unique_percentage=50,
                percentile_25=2.0,
                percentile_50=2.0,
                percentile_75=217.0,
                max=432.0,
                min=2.0,
                mean=145.33,
                most_common_value=2,
                most_common_value_percentage=50,
                std=248.26,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
            ),
        ),
    ],
)
def test_data_profile_analyzer_num_features(dataset: pd.DataFrame, expected_metrics: FeatureQualityStats) -> None:
    data_profile_analyzer = DataQualityAnalyzer()

    data_mapping = ColumnMapping(
        numerical_features=["numerical_feature"],
    )
    result = data_profile_analyzer.calculate(dataset, None, data_mapping)
    assert result.reference_features_stats is not None
    assert result.reference_features_stats.num_features_stats is not None
    assert "numerical_feature" in result.reference_features_stats.num_features_stats
    metrics = result.reference_features_stats.num_features_stats["numerical_feature"]
    assert metrics == expected_metrics


@pytest.mark.parametrize(
    "dataset, expected_metrics",
    [
        (
            pd.DataFrame({"category_feature": []}),
            FeatureQualityStats(
                feature_type="cat",
                count=0,
                percentile_25=None,
                percentile_50=None,
                percentile_75=None,
                infinite_count=None,
                infinite_percentage=None,
                max=None,
                min=None,
                mean=None,
                missing_count=None,
                missing_percentage=None,
                most_common_value=None,
                most_common_value_percentage=None,
                std=None,
                unique_count=None,
                unique_percentage=None,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": [None, None, None, None]}),
            FeatureQualityStats(
                feature_type="cat",
                count=0,
                infinite_count=None,
                infinite_percentage=None,
                missing_count=4,
                missing_percentage=100.0,
                unique_count=0,
                unique_percentage=0.0,
                percentile_25=None,
                percentile_50=None,
                percentile_75=None,
                max=None,
                min=None,
                mean=None,
                most_common_value=np.nan,
                most_common_value_percentage=100.0,
                std=None,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
                new_in_current_values_count=None,
                unused_in_current_values_count=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": [np.nan, 2, 2, 1]}),
            FeatureQualityStats(
                feature_type="cat",
                count=3,
                infinite_count=None,
                infinite_percentage=None,
                missing_count=1,
                missing_percentage=25,
                unique_count=2,
                unique_percentage=50,
                percentile_25=None,
                percentile_50=None,
                percentile_75=None,
                max=None,
                min=None,
                mean=None,
                most_common_value=2,
                most_common_value_percentage=50,
                std=None,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": ["y", "n", "n/a", "n"]}),
            FeatureQualityStats(
                feature_type="cat",
                count=4,
                infinite_count=None,
                infinite_percentage=None,
                missing_count=0,
                missing_percentage=0,
                unique_count=3,
                unique_percentage=75,
                percentile_25=None,
                percentile_50=None,
                percentile_75=None,
                max=None,
                min=None,
                mean=None,
                most_common_value="n",
                most_common_value_percentage=50,
                std=None,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
            ),
        ),
        (
            pd.DataFrame({"category_feature": ["n", "d", "p", "n"]}),
            FeatureQualityStats(
                feature_type="cat",
                count=4,
                infinite_count=None,
                infinite_percentage=None,
                missing_count=0,
                missing_percentage=0,
                unique_count=3,
                unique_percentage=75,
                percentile_25=None,
                percentile_50=None,
                percentile_75=None,
                max=None,
                min=None,
                mean=None,
                most_common_value="n",
                most_common_value_percentage=50,
                std=None,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
            ),
        ),
    ],
)
def test_data_profile_analyzer_cat_features(dataset: pd.DataFrame, expected_metrics: FeatureQualityStats) -> None:
    data_profile_analyzer = DataQualityAnalyzer()

    for task_type in (None, "regression", "classification"):
        result = data_profile_analyzer.calculate(
            dataset, None, ColumnMapping(categorical_features=["category_feature"], task=task_type)
        )
        assert result.reference_features_stats is not None
        assert result.reference_features_stats.cat_features_stats is not None
        assert "category_feature" in result.reference_features_stats.cat_features_stats
        metrics = result.reference_features_stats.cat_features_stats["category_feature"]
        assert metrics == expected_metrics


def test_data_profile_analyzer_classification_with_target() -> None:
    reference_data = pd.DataFrame(
        {
            "target": ["cat_1", "cat_1", "cat_2", "cat_3", "cat_1"],
            "prediction": ["cat_2", "cat_1", "cat_1", "cat_3", "cat_1"],
        }
    )
    current_data = pd.DataFrame(
        {
            "target": ["cat_1", "cat_6", "cat_2", None, "cat_1"],
            "prediction": ["cat_5", "cat_1", "cat_1", "cat_3", np.nan],
        }
    )
    data_profile_analyzer = DataQualityAnalyzer()
    data_mapping = ColumnMapping(task="classification")

    result = data_profile_analyzer.calculate(reference_data, current_data, data_mapping)
    assert result.reference_features_stats is not None
    assert result.reference_features_stats.target_stats is not None
    assert result.reference_features_stats.target_stats["target"] == FeatureQualityStats(
        feature_type="cat",
        count=5,
        infinite_count=None,
        infinite_percentage=None,
        missing_count=0,
        missing_percentage=0.0,
        unique_count=3,
        unique_percentage=60.0,
        percentile_25=None,
        percentile_50=None,
        percentile_75=None,
        max=None,
        min=None,
        mean=None,
        most_common_value="cat_1",
        most_common_value_percentage=60.0,
        std=None,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
        new_in_current_values_count=None,
        unused_in_current_values_count=None,
    )
    assert result.current_features_stats is not None
    assert result.current_features_stats.target_stats is not None
    assert result.current_features_stats.target_stats["target"] == FeatureQualityStats(
        feature_type="cat",
        count=4,
        infinite_count=None,
        infinite_percentage=None,
        missing_count=1,
        missing_percentage=20.0,
        unique_count=3,
        unique_percentage=60.0,
        percentile_25=None,
        percentile_50=None,
        percentile_75=None,
        max=None,
        min=None,
        mean=None,
        most_common_value="cat_1",
        most_common_value_percentage=40.0,
        std=None,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
        new_in_current_values_count=2,
        unused_in_current_values_count=1,
    )


@pytest.mark.parametrize(
    "reference_dataset, current_dataset, expected_new, expected_unused",
    [
        (
            pd.DataFrame({"category_feature": ["", "a", "b"]}),
            pd.DataFrame({"category_feature": ["a", "b"]}),
            0,
            1,
        ),
        (
            pd.DataFrame({"category_feature": [np.nan, 2, 2, 43]}),
            pd.DataFrame({"category_feature": [6, 2, 5, np.nan]}),
            2,
            1,
        ),
        (
            pd.DataFrame({"category_feature": [1, 2, 3, 4]}),
            pd.DataFrame({"category_feature": [6, 2, 5, np.nan]}),
            3,
            3,
        ),
        (
            pd.DataFrame({"category_feature": ["a", "b", "c", "d"]}),
            pd.DataFrame({"category_feature": ["a", "a", "a"]}),
            0,
            3,
        ),
        (
            pd.DataFrame({"category_feature": [np.nan, np.nan, np.nan, np.nan]}),
            pd.DataFrame({"category_feature": ["a", "a", "a"]}),
            1,
            1,
        ),
        (
            pd.DataFrame({"category_feature": [1, 2, 3, np.nan]}),
            pd.DataFrame({"category_feature": [np.nan, np.nan, np.nan]}),
            0,
            3,
        ),
        (
            pd.DataFrame({"category_feature": [1, 2, 3, np.nan, None]}),
            pd.DataFrame({"category_feature": [np.nan]}),
            0,
            3,
        ),
        (
            pd.DataFrame({"category_feature": ["test1", np.nan, None, ""]}),
            pd.DataFrame({"category_feature": [np.nan, None, ""]}),
            0,
            1,
        ),
        (
            pd.DataFrame({"category_feature": ["test1", np.nan, None, ""]}),
            pd.DataFrame({"category_feature": [np.nan, None, "value"]}),
            1,
            2,
        ),
    ],
)
def test_data_profile_analyzer_new_and_unused_count_for_cat_features(
    reference_dataset: pd.DataFrame, current_dataset: pd.DataFrame, expected_new: int, expected_unused: int
) -> None:
    data_profile_analyzer = DataQualityAnalyzer()
    data_mapping = ColumnMapping(
        categorical_features=["category_feature"],
        numerical_features=[],
    )
    result = data_profile_analyzer.calculate(reference_dataset, current_dataset, data_mapping)
    assert result.current_features_stats is not None
    assert result.current_features_stats.cat_features_stats is not None
    assert "category_feature" in result.current_features_stats.cat_features_stats
    metrics = result.current_features_stats.cat_features_stats["category_feature"]
    assert metrics.new_in_current_values_count == expected_new
    assert metrics.unused_in_current_values_count == expected_unused


@pytest.mark.parametrize(
    "dataset, expected_metrics",
    [
        (
            pd.DataFrame({"datetime_feature": [np.nan, np.nan, np.nan, np.nan]}),
            FeatureQualityStats(
                feature_type="datetime",
                count=0,
                percentile_25=None,
                percentile_50=None,
                percentile_75=None,
                infinite_count=None,
                infinite_percentage=None,
                max="nan",
                min="nan",
                mean=None,
                missing_count=4,
                missing_percentage=100,
                most_common_value="nan",
                most_common_value_percentage=100,
                std=None,
                unique_count=0,
                unique_percentage=0,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
            ),
        ),
        (
            pd.DataFrame(
                {
                    "datetime_feature": [
                        pd.NaT,
                        datetime(year=2012, month=1, day=5),
                        datetime(year=2002, month=12, day=5, hour=12),
                        datetime(year=2012, month=1, day=5),
                    ]
                }
            ),
            FeatureQualityStats(
                feature_type="datetime",
                count=3,
                infinite_count=None,
                infinite_percentage=None,
                missing_count=1,
                missing_percentage=25,
                unique_count=2,
                unique_percentage=50,
                percentile_25=None,
                percentile_50=None,
                percentile_75=None,
                max=str(datetime(year=2012, month=1, day=5)),
                min=str(datetime(year=2002, month=12, day=5, hour=12)),
                mean=None,
                most_common_value=str(datetime(year=2012, month=1, day=5)),
                most_common_value_percentage=50,
                std=None,
                most_common_not_null_value=None,
                most_common_not_null_value_percentage=None,
            ),
        ),
    ],
)
def test_data_profile_analyzer_datetime_features(dataset: pd.DataFrame, expected_metrics: FeatureQualityStats) -> None:
    data_profile_analyzer = DataQualityAnalyzer()

    data_mapping = ColumnMapping(
        datetime_features=["datetime_feature"],
    )
    result = data_profile_analyzer.calculate(dataset, None, data_mapping)
    assert result.reference_features_stats is not None
    assert result.reference_features_stats.datetime_features_stats is not None
    assert "datetime_feature" in result.reference_features_stats.datetime_features_stats
    metrics = result.reference_features_stats.datetime_features_stats["datetime_feature"]
    assert metrics == expected_metrics

def test_data_profile_analyzer_datetime_features_zero_lenth() -> None:
    reference_data = pd.DataFrame({"datetime_feature": []})
    data_profile_analyzer = DataQualityAnalyzer()

    data_mapping = ColumnMapping(
        datetime_features=["datetime_feature"],
    )
    result = data_profile_analyzer.calculate(reference_data, None, data_mapping)
    assert "datetime_feature" not in result.reference_features_stats.datetime_features_stats


def test_data_profile_analyzer_empty_features() -> None:
    data_profile_analyzer = DataQualityAnalyzer()
    reference_data = pd.DataFrame(
        {
            "datetime_feature": [np.nan, np.nan, np.nan],
        }
    )
    data_mapping = ColumnMapping(
        datetime_features=["datetime_feature"],
    )
    result = data_profile_analyzer.calculate(reference_data, None, data_mapping)

    assert "datetime_feature" in result.reference_features_stats.datetime_features_stats
    datetime_feature = result.reference_features_stats.datetime_features_stats["datetime_feature"]
    assert datetime_feature == FeatureQualityStats(
        feature_type="datetime",
        count=0,
        infinite_count=None,
        infinite_percentage=None,
        missing_count=3,
        missing_percentage=100,
        unique_count=0,
        unique_percentage=0,
        percentile_25=None,
        percentile_50=None,
        percentile_75=None,
        max="nan",
        min="nan",
        mean=None,
        most_common_value="nan",
        most_common_value_percentage=100,
        std=None,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
        new_in_current_values_count=None,
        unused_in_current_values_count=None,
    )


def test_data_profile_analyzer_regression() -> None:
    data_profile_analyzer = DataQualityAnalyzer()
    reference_data = pd.DataFrame(
        {
            "my_target": [1, 2, 3, 1],
            "reference": [2, 1, 1, 1],
            "numerical_feature_1": [0, 2, -1, 5],
            "numerical_feature_2": [0.3, 5, 0.3, 3.4],
            "categorical_feature_1": [1, 1, 5, 2],
            "categorical_feature_2": ["y", "y", "n", "y"],
            "datetime_feature_1": [
                datetime(year=2012, month=1, day=5),
                datetime(year=2002, month=12, day=5),
                datetime(year=2012, month=1, day=5),
                datetime(year=2012, month=1, day=6),
            ],
            "datetime_feature_2": [
                datetime(year=2022, month=1, day=5, hour=13, minute=23),
                datetime(year=2022, month=1, day=5, hour=10, minute=23),
                datetime(year=2022, month=1, day=5, hour=13),
                datetime(year=2022, month=1, day=5, hour=10, minute=23),
            ],
        }
    )
    data_mapping = ColumnMapping(
        target="my_target",
        numerical_features=["numerical_feature_1", "numerical_feature_2"],
        categorical_features=["categorical_feature_1", "categorical_feature_2"],
        datetime_features=["datetime_feature_1", "datetime_feature_2"],
        task="regression",
    )
    result = data_profile_analyzer.calculate(reference_data, None, data_mapping)
    assert result.columns is not None
    assert result.reference_features_stats is not None
    assert result.reference_features_stats.num_features_stats is not None
    assert "numerical_feature_1" in result.reference_features_stats.num_features_stats
    numerical_feature_1 = result.reference_features_stats.num_features_stats["numerical_feature_1"]
    assert numerical_feature_1 == FeatureQualityStats(
        feature_type="num",
        count=4,
        infinite_count=0,
        infinite_percentage=0.0,
        missing_count=0,
        missing_percentage=0.0,
        unique_count=4,
        unique_percentage=100,
        percentile_25=-0.25,
        percentile_50=1.0,
        percentile_75=2.75,
        max=5,
        min=-1,
        mean=1.5,
        most_common_value=5,
        most_common_value_percentage=25,
        std=2.65,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
    )
    assert "numerical_feature_2" in result.reference_features_stats.num_features_stats
    numerical_feature_2 = result.reference_features_stats.num_features_stats["numerical_feature_2"]
    assert numerical_feature_2 == FeatureQualityStats(
        feature_type="num",
        count=4,
        infinite_count=0,
        infinite_percentage=0.0,
        missing_count=0,
        missing_percentage=0.0,
        unique_count=3,
        unique_percentage=75,
        percentile_25=0.3,
        percentile_50=1.85,
        percentile_75=3.8,
        max=5.0,
        min=0.3,
        mean=2.25,
        most_common_value=0.3,
        most_common_value_percentage=50,
        std=2.34,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
    )

    assert result.reference_features_stats.cat_features_stats is not None
    assert "categorical_feature_1" in result.reference_features_stats.cat_features_stats
    categorical_feature_1 = result.reference_features_stats.cat_features_stats["categorical_feature_1"]
    assert categorical_feature_1 == FeatureQualityStats(
        feature_type="cat",
        count=4,
        infinite_count=None,
        infinite_percentage=None,
        missing_count=0,
        missing_percentage=0.0,
        unique_count=3,
        unique_percentage=75,
        percentile_25=None,
        percentile_50=None,
        percentile_75=None,
        max=None,
        min=None,
        mean=None,
        most_common_value=1,
        most_common_value_percentage=50,
        std=None,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
    )

    assert "categorical_feature_2" in result.reference_features_stats.cat_features_stats
    categorical_feature_2 = result.reference_features_stats.cat_features_stats["categorical_feature_2"]
    assert categorical_feature_2 == FeatureQualityStats(
        feature_type="cat",
        count=4,
        infinite_count=None,
        infinite_percentage=None,
        missing_count=0,
        missing_percentage=0.0,
        unique_count=2,
        unique_percentage=50,
        percentile_25=None,
        percentile_50=None,
        percentile_75=None,
        max=None,
        min=None,
        mean=None,
        most_common_value="y",
        most_common_value_percentage=75,
        std=None,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
    )

    assert result.reference_features_stats.datetime_features_stats is not None
    assert "datetime_feature_1" in result.reference_features_stats.datetime_features_stats
    datetime_feature_1 = result.reference_features_stats.datetime_features_stats["datetime_feature_1"]
    assert datetime_feature_1 == FeatureQualityStats(
        feature_type="datetime",
        count=4,
        infinite_count=None,
        infinite_percentage=None,
        missing_count=0,
        missing_percentage=0.0,
        unique_count=3,
        unique_percentage=75,
        percentile_25=None,
        percentile_50=None,
        percentile_75=None,
        max="2012-01-06 00:00:00",
        min="2002-12-05 00:00:00",
        mean=None,
        most_common_value="2012-01-05 00:00:00",
        most_common_value_percentage=50,
        std=None,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
    )
    assert "datetime_feature_2" in result.reference_features_stats.datetime_features_stats
    datetime_feature_2 = result.reference_features_stats.datetime_features_stats["datetime_feature_2"]
    assert datetime_feature_2 == FeatureQualityStats(
        feature_type="datetime",
        count=4,
        infinite_count=None,
        infinite_percentage=None,
        missing_count=0,
        missing_percentage=0.0,
        unique_count=3,
        unique_percentage=75,
        percentile_25=None,
        percentile_50=None,
        percentile_75=None,
        max="2022-01-05 13:23:00",
        min="2022-01-05 10:23:00",
        mean=None,
        most_common_value="2022-01-05 10:23:00",
        most_common_value_percentage=50,
        std=None,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
    )

    assert result.reference_features_stats.target_stats is not None
    assert "my_target" in result.reference_features_stats.target_stats
    target_stats = result.reference_features_stats.target_stats["my_target"]
    assert target_stats == FeatureQualityStats(
        feature_type="num",
        count=4,
        infinite_count=0,
        infinite_percentage=0.0,
        missing_count=0,
        missing_percentage=0.0,
        unique_count=3,
        unique_percentage=75,
        percentile_25=1.0,
        percentile_50=1.5,
        percentile_75=2.25,
        max=3,
        min=1,
        mean=1.75,
        most_common_value=1,
        most_common_value_percentage=50,
        std=0.96,
        most_common_not_null_value=None,
        most_common_not_null_value_percentage=None,
    )

    assert result.current_features_stats is None

def test_select_features_for_corr() -> None:
    data_profile_analyzer = DataQualityAnalyzer()
    reference_data = pd.DataFrame(
        {
            "my_target": [1, 2, 3, 1],
            "reference": [2, 1, 1, 1],
            "numerical_feature_1": [0, 2, -1, 5],
            "numerical_feature_2": [0.3, 5, 0.3, 3.4],
            "numerical_feature_empty": [np.nan]*4,
            "numerical_feature_constant": [1]*4,
            "categorical_feature_1": [1, 1, 5, 2],
            "categorical_feature_2": ["y", "y", "n", "y"],
            "categorical_feature_empty": [np.nan]*4,
            "categorical_feature_constant": [1, 1, 1, np.nan],
            "datetime_feature_1": [
                datetime(year=2012, month=1, day=5),
                datetime(year=2002, month=12, day=5),
                datetime(year=2012, month=1, day=5),
                datetime(year=2012, month=1, day=6),
            ],
            "datetime_feature_2": [
                datetime(year=2022, month=1, day=5, hour=13, minute=23),
                datetime(year=2022, month=1, day=5, hour=10, minute=23),
                datetime(year=2022, month=1, day=5, hour=13),
                datetime(year=2022, month=1, day=5, hour=10, minute=23),
            ],
        }
    )
    column_mapping = ColumnMapping(
        target="my_target",
        numerical_features=["numerical_feature_1", "numerical_feature_2", "numerical_feature_empty",
        "numerical_feature_constant"],
        categorical_features=["categorical_feature_1", "categorical_feature_2", "categorical_feature_empty",
        "categorical_feature_constant"],
        datetime_features=["datetime_feature_1", "datetime_feature_2"],
        task="regression",
    )
    columns = process_columns(reference_data, column_mapping)
    reference_features_stats = data_profile_analyzer._calculate_stats(reference_data, columns, "regression")
    num_for_corr, cat_for_corr = data_profile_analyzer._select_features_for_corr(reference_features_stats, 
                                                                                 target_name="my_target")
    assert num_for_corr == ["numerical_feature_1", "numerical_feature_2", "my_target"]
    assert cat_for_corr == ["categorical_feature_1", "categorical_feature_2"]


def test_cramer_v() -> None:
    x = pd.Series(['a'] * 15 + ['b'] * 13)
    y = pd.Series(['c'] * 7 + ['d'] * 8 + ['c'] * 11 + ['d'] * 2)
    data_profile_analyzer = DataQualityAnalyzer()
    v = data_profile_analyzer._cramer_v(x, y)

    assert v == 0.3949827793858816

def test_corr_matrix() -> None:
    df = pd.DataFrame(
        {
            'x': ['a'] * 15 + ['b'] * 13,
            'y': ['c'] * 7 + ['d'] * 8 + ['c'] * 11 + ['d'] * 2,
            'z': ['f'] * 14 + ['e'] * 14
        }
    )
    data_profile_analyzer = DataQualityAnalyzer()
    corr_matrix = data_profile_analyzer._corr_matrix(df, data_profile_analyzer._cramer_v)
    expected = np.array(
        [[1.        , 0.39498278, 0.93094934],
        [0.39498278, 1.        , 0.2981424 ],
        [0.93094934, 0.2981424 , 1.        ]]
    )

    assert np.allclose(corr_matrix.values, expected)


