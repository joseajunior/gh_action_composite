### Description

An action to parse Robot Framework test reports in a summary and detail tables format and post them in the job description and/or as a comment on the pull request.

## Inputs

- `gh_access_token` - Token to access the GitHub API.
    This is only needed if you want to post the report to the pull request that triggered the tests.
- `report_path` - Path to the directory containing the Robot Framework test reports.
    Default: `reports`
- `pr_number` - Pull Request number.
    This is only needed if you want to post the report to the pull request that triggered the tests.
- `only_summary` - Only output report to GitHub Actions Summary.
    Default: `false`

### Usage

```yaml
---
steps:
  - name: Download reports
    uses: actions/download-artifact@v4.1.2
    with:
      name: reports
      path: reports

  - name: Send report to commit
    uses: wexinc/shared-actions/robot-framework/reporter@v1
    with:
      gh_access_token: ${{ secrets.GITHUB_TOKEN }}
      report_path: reports
      pr_number: ${{ github.event.pull_request.number }}
```
