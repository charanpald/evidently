import copy
import dataclasses
import json
import uuid
from collections import Counter
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

import evidently
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns
from evidently.dashboard.dashboard import SaveMode
from evidently.dashboard.dashboard import SaveModeMap
from evidently.dashboard.dashboard import TemplateParams
from evidently.dashboard.dashboard import save_data_file
from evidently.dashboard.dashboard import save_lib_files
from evidently.metrics.base_metric import InputData
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.renderers.notebook_utils import determine_template
from evidently.suite.base_suite import Suite
from evidently.suite.base_suite import find_test_renderer
from evidently.test_preset.test_preset import TestPreset
from evidently.tests.base_test import BaseTestGenerator
from evidently.tests.base_test import DEFAULT_GROUP
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestResult
from evidently.utils import NumpyEncoder


class TestSuite:
    _inner_suite: Suite
    _columns_info: DatasetColumns
    _test_presets: List[TestPreset]
    _test_generators: List[BaseTestGenerator]

    def __init__(self, tests: Optional[List[Union[Test, TestPreset, BaseTestGenerator]]]):
        self._inner_suite = Suite()
        self._test_presets = []
        self._test_generators = []

        for original_test in tests or []:
            if isinstance(original_test, TestPreset):
                self._test_presets.append(original_test)

            elif isinstance(original_test, BaseTestGenerator):
                self._test_generators.append(original_test)

            else:
                self._add_test(original_test)

    def _add_test(self, test: Test):
        new_test = copy.copy(test)
        self._inner_suite.add_test(new_test)

    def __bool__(self):
        return all(test_result.is_passed() for _, test_result in self._inner_suite.context.test_results.items())

    def _add_tests_from_generator(self, test_generator: BaseTestGenerator):
        for test_item in test_generator.generate_tests(columns_info=self._columns_info):
            self._add_test(test_item)

    def run(
        self,
        *,
        reference_data: Optional[pd.DataFrame],
        current_data: pd.DataFrame,
        column_mapping: Optional[ColumnMapping] = None,
    ) -> None:
        if column_mapping is None:
            column_mapping = ColumnMapping()

        self._columns_info = process_columns(current_data, column_mapping)

        for preset in self._test_presets:
            tests = preset.generate_tests(InputData(reference_data, current_data, column_mapping), self._columns_info)

            for test in tests:
                if isinstance(test, BaseTestGenerator):
                    self._add_tests_from_generator(test)

                else:
                    self._add_test(test)

        for test_generator in self._test_generators:
            self._add_tests_from_generator(test_generator)

        self._inner_suite.verify()
        self._inner_suite.run_calculate(InputData(reference_data, current_data, column_mapping))
        self._inner_suite.run_checks()

    def _repr_html_(self):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        template_params = TemplateParams(
            dashboard_id=dashboard_id, dashboard_info=dashboard_info, additional_graphs=graphs
        )
        return self._render(determine_template("auto"), template_params)

    def show(self, mode="auto"):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        template_params = TemplateParams(
            dashboard_id=dashboard_id, dashboard_info=dashboard_info, additional_graphs=graphs
        )
        # pylint: disable=import-outside-toplevel
        try:
            from IPython.display import HTML

            return HTML(self._render(determine_template(mode), template_params))
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err

    def save_html(self, filename: str, mode: Union[str, SaveMode] = SaveMode.SINGLE_FILE):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        if isinstance(mode, str):
            _mode = SaveModeMap.get(mode)
            if _mode is None:
                raise ValueError(f"Unexpected save mode {mode}. Expected [{','.join(SaveModeMap.keys())}]")
            mode = _mode
        if mode == SaveMode.SINGLE_FILE:
            template_params = TemplateParams(
                dashboard_id=dashboard_id,
                dashboard_info=dashboard_info,
                additional_graphs=graphs,
            )
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(self._render(determine_template("inline"), template_params))
        else:
            font_file, lib_file = save_lib_files(filename, mode)
            data_file = save_data_file(filename, mode, dashboard_id, dashboard_info, graphs)
            template_params = TemplateParams(
                dashboard_id=dashboard_id,
                dashboard_info=dashboard_info,
                additional_graphs=graphs,
                embed_lib=False,
                embed_data=False,
                embed_font=False,
                font_file=font_file,
                include_js_files=[lib_file, data_file],
            )
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(self._render(determine_template("inline"), template_params))

    def as_dict(self) -> dict:
        test_results = []
        counter = Counter(test_result.status for test_result in self._inner_suite.context.test_results.values())

        for test in self._inner_suite.context.test_results:
            renderer = find_test_renderer(type(test), self._inner_suite.context.renderers)
            test_results.append(renderer.render_json(test))

        total_tests = len(self._inner_suite.context.test_results)

        return {
            "version": evidently.__version__,
            "datetime": datetime.now().isoformat(),
            "tests": test_results,
            "summary": {
                "all_passed": bool(self),
                "total_tests": total_tests,
                "success_tests": counter["SUCCESS"] + counter["WARNING"],
                "failed_tests": counter["FAIL"],
                "by_status": counter,
            },
            "columns_info": dataclasses.asdict(self._columns_info),
        }

    def json(self) -> str:
        return json.dumps(self.as_dict(), cls=NumpyEncoder)

    def save_json(self, filename):
        with open(filename, "w", encoding="utf-8") as out_file:
            json.dump(self.as_dict(), out_file, cls=NumpyEncoder)

    def _render(self, temple_func, template_params: TemplateParams):
        return temple_func(params=template_params)

    def _build_dashboard_info(self):
        test_results = []
        total_tests = len(self._inner_suite.context.test_results)
        by_status = {}

        for test, test_result in self._inner_suite.context.test_results.items():
            # renderer = find_test_renderer(type(test.obj), self._inner_suite.context.renderers)
            renderer = find_test_renderer(type(test), self._inner_suite.context.renderers)
            by_status[test_result.status] = by_status.get(test_result.status, 0) + 1
            test_results.append(renderer.render_html(test))

        summary_widget = BaseWidgetInfo(
            title="",
            size=2,
            type="counter",
            params={
                "counters": [{"value": f"{total_tests}", "label": "Tests"}]
                + [
                    {"value": f"{by_status.get(status, 0)}", "label": f"{status.title()}"}
                    for status in [TestResult.SUCCESS, TestResult.WARNING, TestResult.FAIL, TestResult.ERROR]
                ]
            },
        )
        test_suite_widget = BaseWidgetInfo(
            title="",
            type="test_suite",
            size=2,
            params={
                "tests": [
                    dict(
                        title=test_info.name,
                        description=test_info.description,
                        state=test_info.status.lower(),
                        details=dict(
                            parts=[
                                dict(id=f"{test_info.name}_{idx}_{item.id}", title=item.title, type="widget")
                                for item in test_info.details
                            ]
                        ),
                        groups=test_info.groups,
                    )
                    for idx, test_info in enumerate(test_results)
                ],
                "testGroupTypes": DEFAULT_GROUP,
            },
            additionalGraphs=[],
        )
        return (
            "evidently_dashboard_" + str(uuid.uuid4()).replace("-", ""),
            DashboardInfo("Test Suite", widgets=[summary_widget, test_suite_widget]),
            {
                f"{info.name}_{idx}_{item.id}": dataclasses.asdict(item.info)
                for idx, info in enumerate(test_results)
                for item in info.details
            },
        )
