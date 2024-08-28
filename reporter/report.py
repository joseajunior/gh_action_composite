import os, json

from robot.api import ExecutionResult, ResultVisitor
from robot.model.statistics import Statistics
from robot.result import TestCase, Result


class MyResultsVisitor(ResultVisitor):

    def __init__(self, markdown_file: str = 'report.md',
                 include_passed: bool = False):
        self.tests: dict = {}
        self.markdown_file: str = markdown_file
        self.include_passed: bool = include_passed
        self.elapsed_time: int = 0
        self.has_failed: bool = False

    def visit_test(self, test: TestCase):
        if test.status in ['FAIL', 'SKIP']:
            self.tests[test.name] = {'message': test.message.replace('\n', '<br />'),
                                    'status': test.status,
                                    'suite': test.parent.name}
            if test.status == 'FAIL' and not self.has_failed:
                self.has_failed = True
        elif test.status == 'PASS' and self.include_passed:
            self.tests[test.name] = {'status': test.status,
                                    'suite': test.parent.name}
        self.elapsed_time += test.elapsedtime

    def end_result(self, result: Result):
        with open(self.markdown_file, "w") as f:
            f.write("# Robot Framework Report\n")
            f.write(self._format_stats_table(result.statistics))
            if self.tests:
                f.write("\n\n")
                f.write(self._format_tests_table())
        with open('statistics.json', 'w') as j:
            json_data = {
                'total': result.statistics.total.total,
                'passed': result.statistics.total.passed,
                'failed': result.statistics.total.failed,
                'skipped': result.statistics.total.skipped,
                'pass_percentage': self.pass_percent,
                'duration': self.elapsed_time
            }
            json.dump(json_data, j)
        if os.environ.get('GITHUB_ACTIONS'):
            os.system(f'echo "HAS_FAILS={str(self.has_failed).lower()}" >> GITHUB_ENV')

    def _format_stats_table(self, statistics: Statistics):
        stats_table = ["## Test Suite Statistics", "|:white_check_mark: Passed|:x: Failed|:arrow_right_hook: Skipped|:dart: Total|Pass %|:clock12: Duration|", "|:---:|:---:|:---:|:---:|:---:|:---:|"]
        self.pass_percent = round(statistics.total.passed / (statistics.total.total -
                                                        statistics.total.skipped) * 100, 2)
        seconds = round(self.elapsed_time / 1000)
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.elapsed_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        if self.pass_percent == 100:
            medal = ":1st_place_medal:"
        elif 75 <= self.pass_percent < 100:
            medal = ":2nd_place_medal:"
        elif 50 <= self.pass_percent < 75:
            medal = ":3rd_place_medal:"
        else:
            medal = ":disappointed:"
        stats_table[1] = stats_table[1].replace("Pass %", f"{medal} Pass %")

        stats_table.append(f"|{statistics.total.passed}|{statistics.total.failed}|{statistics.total.skipped}|{statistics.total.total}|{self.pass_percent}%|{self.elapsed_time}|")

        return "\n".join(stats_table)

    def _format_tests_table(self):
        tests_table = ["## Test Status", "|Test|Status|Suite|Message|",
                                "|---|:---:|:---:|---|"]
        for name, info in self.tests.items():
            tests_table.append(f"|{name.replace('|', '&vert;')}|{info.get('status').replace('|', '&vert;')}|{info.get('suite')}|{info.get('message', '').replace('|', '&vert;')}|")

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


if __name__ == '__main__':
    main()
