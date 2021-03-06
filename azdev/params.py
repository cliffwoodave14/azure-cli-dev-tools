# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

# pylint: disable=line-too-long
import argparse

from knack.arguments import ArgumentsContext

from azdev.completer import get_test_completion


class Flag(object):
    pass


def load_arguments(self, _):

    with ArgumentsContext(self, '') as c:
        c.argument('modules', options_list=['--modules', '-m'], nargs='+', help='Space-separated list of modules to check. Omit to check all.')
        c.argument('private', action='store_true', help='Target the private repo.')

    with ArgumentsContext(self, 'setup') as c:
        c.argument('cli_path', options_list=['--cli', '-c'], nargs='?', const=Flag, help='Path to an existing Azure CLI repo. Omit value to search for the repo.')
        c.argument('ext_repo_path', options_list=['--repo', '-r'], nargs='+', help='Space-separated list of paths to existing Azure CLI extensions repos.')
        c.argument('ext', options_list=['--ext', '-e'], nargs='+', help='Space-separated list of extensions to install initially.')

    with ArgumentsContext(self, 'test') as c:
        c.argument('discover', options_list='--discover', action='store_true', help='Build an index of test names so that you don\'t need to specify fully qualified test paths.')
        c.argument('xml_path', options_list='--xml-path', help='Path and filename at which to store the results in XML format. If omitted, the file will be saved as `test_results.xml` in your `.azdev` directory.')
        c.argument('in_series', options_list='--series', action='store_true', help='Disable test parallelization.')
        c.argument('run_live', options_list='--live', action='store_true', help='Run all tests live.')
        c.positional('tests', nargs='*', help='Space-separated list of tests to run. Can specify test filenames, class name or individual method names.', completer=get_test_completion)
        c.argument('profile', options_list='--profile', help='Run automation against a specific profile. If omit, the tests will run against current profile.')
        c.argument('pytest_args', nargs=argparse.REMAINDER, options_list=['--pytest-args', '-a'], help='Denotes the remaining args will be passed to pytest.')
        c.argument('last_failed', options_list='--lf', action='store_true', help='Re-run the last tests that failed.')

    with ArgumentsContext(self, 'coverage') as c:
        c.argument('prefix', type=str, help='Filter analysis by command prefix.')
        c.argument('report', action='store_true', help='Display results as a report.')
        c.argument('untested_params', nargs='+', help='Space-separated list of param dest values to search for (OR logic)')

    with ArgumentsContext(self, 'style') as c:
        c.positional('modules', nargs='*', help='Space-separated list of modules or extensions to check.')
        c.argument('pylint', action='store_true', help='Run pylint.')
        c.argument('pep8', action='store_true', help='Run flake8 to check PEP8.')

    for scope in ['history', 'version']:
        with ArgumentsContext(self, 'verify {}'.format(scope)) as c:
            c.positional('modules', nargs='*', help='Space-separated list of modules to check.')

    with ArgumentsContext(self, 'verify version') as c:
        c.argument('update', action='store_true', help='If provided, the command will update the versions in azure-cli\'s setup.py file.')
        c.argument('pin', action='store_true', help='If provided and used with --update, will pin the module versions in azure-cli\'s setup.py file.')

    with ArgumentsContext(self, 'linter') as c:
        c.positional('modules', nargs='*', help='Space-separated list of modules or extensions to check.')
        c.argument('rules', options_list=['--rules', '-r'], nargs='+', help='Space-separated list of rules to run. Omit to run all rules.')
        c.argument('rule_types', options_list=['--rule-types', '-t'], nargs='+', choices=['params', 'commands', 'command_groups', 'help_entries'], help='Space-separated list of rule types to run. Omit to run all.')

    with ArgumentsContext(self, 'perf') as c:
        c.argument('runs', type=int, help='Number of runs to average performance over.')

    for scope in ['extension add', 'extension remove']:
        with ArgumentsContext(self, scope) as c:
            c.positional('extensions', metavar='NAME', nargs='+', help='Space-separated list of extension names.')

    for scope in ['extension repo add', 'extension repo remove']:
        with ArgumentsContext(self, scope) as c:
            c.positional('repos', metavar='PATH', nargs='+', help='Space-separated list of paths to Git repositories.')

    with ArgumentsContext(self, 'extension update-index') as c:
        c.positional('extension', metavar='URL', help='URL to an extension WHL file.')

    with ArgumentsContext(self, 'group delete') as c:
        c.argument('product', help='Value for tag `product` to mark for deletion.', arg_group='Tag')
        c.argument('older_than', type=int, help='Minimum age (in hours) for tag `date` to mark for deletion.', arg_group='Tag')
        c.argument('cause', help='Value for tag `cause` to mark for deletion.', arg_group='Tag')
        c.argument('yes', options_list=['--yes', '-y'], help='Do not prompt.')
        c.argument('prefixes', options_list=['--prefixes', '-p'], nargs='+', help='Space-separated list of prefixes to filter by.')
