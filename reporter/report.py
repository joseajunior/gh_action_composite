import os
from robot.api import ExecutionResult, ResultVisitor
from robot.model.statistics import Statistics
from robot.result import TestCase, Result


class MyResultsVisitor(ResultVisitor):

    def __init__(self, markdown_file: str='report.md',
                 include_passed: bool=False):
        self.tests: dict = {}
        self.markdown_file: str = markdown_file
        self.include_passed: bool = include_passed
        self.elapsed_time: int = 0

    def visit_test(self, test: TestCase):
        if test.status in ['FAIL', 'SKIP']:
            # skipcq: PY-W0073
            self.tests[test.name.replace('|', '\|')] = {'message': test.message.split('\n')[0],
                                                        'status': test.status,
                                                        'suite': test.parent.name}
        elif test.status == 'PASS' and self.include_passed:
            # skipcq: PY-W0073
            self.tests[test.name.replace('|', '\|')] = {'status': test.status,
                                                        'suite': test.parent.name}
        self.elapsed_time += test.elapsedtime

    def end_result(self, result: Result):
        with open(self.markdown_file, "w") as f:
            f.write("# Robot Framework Report\n")
            f.write(self._format_stats_table(result.statistics))
            f.write("\n\n")
            f.write(self._format_tests_table(self.tests))

    def _format_stats_table(self, statistics: Statistics):
        stats_table = ["## Test Suite Statistics", "|:white_check_mark: Passed|:x: Failed|:arrow_right_hook: Skipped|:dart: Total|Pass %|:clock12: Duration|", "|:---:|:---:|:---:|:---:|:---:|:---:|"]
        pass_percent = round(statistics.total.passed / (statistics.total.total -
                                                        statistics.total.skipped) * 100, 2)
        seconds = round(self.elapsed_time / 1000)
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        if pass_percent == 100:
            medal = ":1st_place_medal:"
        elif 75 <= pass_percent < 100:
            medal = ":2nd_place_medal:"
        elif 50 <= pass_percent < 75:
            medal = ":3rd_place_medal:"
        else:
            medal = ":disappointed:"
        stats_table[1] = stats_table[1].replace("Pass %", f"{medal} Pass %")
        stats_table.append(f"|{statistics.total.passed}|{statistics.total.failed}|{statistics.total.skipped}|{statistics.total.total}|{pass_percent}%|{elapsed_time}|")

        return "\n".join(stats_table)

    @staticmethod
    def _format_tests_table(tests: dict[str, dict[str, str]]):
        tests_table = ["## Test Status", "|Test|Status|Suite|Message|",
                       "|---|:---:|:---:|---|"]
        for name, info in tests.items():
            tests_table.append(f"|{name}|{info.get('status')}|{info.get('suite')}|{info.get('message', '')}|")

        return "\n".join(tests_table)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-r', '--report', help='The XML file',
                        required=True, type=str)
    parser.add_argument('-o', '--output', help='The Markdown result file',
                        required=False, default='report.md', type=str)
    parser.add_argument('-p', '--passed', help='Include passed tests',
                        required=False, default='false', type=str)
    args = parser.parse_args()

    output_file = os.path.join(args.report, 'output.xml') if os.path.isdir(args.report) else args.report
    markdown_file = args.output
    result = ExecutionResult(output_file)
    result.visit(MyResultsVisitor(markdown_file,
                                  include_passed=bool(args.passed.lower() == 'true')))

def callable_main(report: str, output: str = 'report.md', passed: str = 'false'):
    output_file = os.path.join(report, 'output.xml') if os.path.isdir(report) else report
    result = ExecutionResult(output_file)
    result.visit(MyResultsVisitor(output, include_passed=bool(passed.lower() == 'true')))

if __name__ == '__main__':
    main()