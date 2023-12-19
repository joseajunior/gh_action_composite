import os
from robot.api import ExecutionResult, ResultVisitor
from robot.model.statistics import Statistics
from robot.result import TestCase, Result

class MyResultsVisitor(ResultVisitor):
    def __init__(self, markdown_file: str='report.md', only_failed: bool=False):
        self.tests: dict = dict()
        self.markdown_file: str = markdown_file
        self.only_failed: bool = only_failed

    def visit_test(self, test: TestCase):
        if test.status == 'FAIL':
            self.tests[test.name] = {'message': test.message.split('\n')[0], 'status': test.status}
        elif test.status == 'PASS':
            self.tests[test.name] = {'status': test.status}

    def end_result(self, result: Result):
        with open(self.markdown_file, "w") as f:
            f.write("# Robot Framework Report\n")
            f.write(self._format_stats_table(result.statistics, result.suite.elapsedtime))
            f.write("\n\n")
            f.write(self._format_tests_table(self.tests))

    def _format_stats_table(self, statistics: Statistics, elapsed_time: int):
        stats_table = ["## Test Suite Statistics", "|✅ Passed|❌ Failed|⏭️ Skipped|Total|Pass %|⏱️ Duration|", "|:---:|:---:|:---:|:---:|:---:|:---:|"]
        pass_percent = round(statistics.total.passed / statistics.total.total * 100, 2)
        seconds = elapsed_time / 1000
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        stats_table.append(f"|{statistics.total.passed}|{statistics.total.failed}|{statistics.total.skipped}|{statistics.total.total}|{pass_percent}%|{elapsed_time}|")

        return "\n".join(stats_table)

    def _format_tests_table(self, tests: dict[str, dict[str, str]]):
        tests_table = ["## Test Status", "|Test|Status|Message|", "|---|:---:|---|"]
        for name, info in tests.items():
            if self.only_failed and info.get('status') != 'FAIL':
                continue
            tests_table.append(f"|{name}|{info.get('status')}|{info.get('message', '')}|")

        return "\n".join(tests_table)

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-r', '--report', help='The XML file', required=True, type=str)
    parser.add_argument('-o', '--output', help='The Markdown result file', required=False, default='report.md', type=str)
    parser.add_argument('--only-failed', help='Only show failed tests', required=False, default=False, type=bool)
    args = parser.parse_args()

    output_file = os.path.join(args.report, 'output.xml')
    markdown_file = args.output
    only_failed = args.only_failed
    result = ExecutionResult(output_file)
    result.visit(MyResultsVisitor(markdown_file, only_failed))

if __name__ == '__main__':
    main()
