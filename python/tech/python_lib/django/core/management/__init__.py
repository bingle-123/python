import functools
import os
import pkgutil
import sys
from collections import OrderedDict, defaultdict
from importlib import import_module

import django
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import (
    BaseCommand, CommandError, CommandParser, handle_default_options,
)
from django.core.management.color import color_style
from django.utils import autoreload
from django.utils.encoding import force_text


def find_commands(management_dir):
    """
    Given a path to a management directory, return a list of all the command
    names that are available.
    """
    command_dir = os.path.join(management_dir, 'commands')
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


def load_command_class(app_name, name):
    """
    Given a command name and an application name, return the Command
    class instance. Allow all errors raised by the import process
    (ImportError, AttributeError) to propagate.
    """
    module = import_module('%s.management.commands.%s' % (app_name, name))
    return module.Command()


@functools.lru_cache(maxsize=None)
def get_commands():
    """
    Return a dictionary mapping command names to their callback applications.

    Look for a management.commands package in django.core, and in each
    installed application -- if a commands package exists, register all
    commands in that package.

    Core commands are always included. If a settings module has been
    specified, also include user-defined commands.

    The dictionary is in the format {command_name: app_name}. Key-value
    pairs from this dictionary can then be used in calls to
    load_command_class(app_name, command_name)

    If a specific version of a command must be loaded (e.g., with the
    startapp command), the instantiated module can be placed in the
    dictionary in place of the application name.

    The dictionary is cached on the first call and reused on subsequent
    calls.
    """
    commands = {name: 'django.core' for name in find_commands(__path__[0])}

    if not settings.configured:
        return commands

    for app_config in reversed(list(apps.get_app_configs())):
        path = os.path.join(app_config.path, 'management')
        commands.update({name: app_config.name for name in find_commands(path)})

    return commands


def call_command(command_name, *args, **options):
    """
    Call the given command, with the given options and args/kwargs.

    This is the primary API you should use for calling specific commands.

    `command_name` may be a string or a command object. Using a string is
    preferred unless the command object is required for further processing or
    testing.

    Some examples:
        call_command('migrate')
        call_command('shell', plain=True)
        call_command('sqlmigrate', 'myapp')

        from django.core.management.commands import flush
        cmd = flush.Command()
        call_command(cmd, verbosity=0, interactive=False)
        # Do something with cmd ...
    """
    if isinstance(command_name, BaseCommand):
        # Command object passed in.
        command = command_name
        command_name = command.__class__.__module__.split('.')[-1]
    else:
        # Load the command object by name.
        try:
            app_name = get_commands()[command_name]
        except KeyError:
            raise CommandError("Unknown command: %r" % command_name)

        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            command = app_name
        else:
            command = load_command_class(app_name, command_name)

    # Simulate argument parsing to get the option defaults (see #10080 for details).
    parser = command.create_parser('', command_name)
    # Use the `dest` option name from the parser option
    opt_mapping = {
        min(s_opt.option_strings).lstrip('-').replace('-', '_'): s_opt.dest
        for s_opt in parser._actions if s_opt.option_strings
    }
    arg_options = {opt_mapping.get(key, key): value for key, value in options.items()}
    defaults = parser.parse_args(args=[force_text(a) for a in args])
    defaults = dict(defaults._get_kwargs(), **arg_options)
    # Raise an error if any unknown options were passed.
    stealth_options = set(command.base_stealth_options + command.stealth_options)
    dest_parameters = {action.dest for action in parser._actions}
    valid_options = (dest_parameters | stealth_options).union(opt_mapping)
    unknown_options = set(options) - valid_options
    if unknown_options:
        raise TypeError(
            "Unknown option(s) for %s command: %s. "
            "Valid options are: %s." % (
                command_name,
                ', '.join(sorted(unknown_options)),
                ', '.join(sorted(valid_options)),
            )
        )
    # Move positional args out of options to mimic legacy optparse
    args = defaults.pop('args', ())
    if 'skip_checks' not in options:
        defaults['skip_checks'] = True

    return command.execute(*args, **defaults)


class ManagementUtility:
    """
    Encapsulate the logic of the django-admin and manage.py utilities.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        # 如果prog_name!='manage.py'就改为'python -m django'
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == '__main__.py':
            self.prog_name = 'python -m django'
        self.settings_exception = None

    def main_help_text(self, commands_only=False):
        """Return the script's main help text, as a string."""
        if commands_only:
            usage = sorted(get_commands())
        else:
            usage = [
                "",
                "Type '%s help <subcommand>' for help on a specific subcommand." % self.prog_name,
                "",
                "Available subcommands:",
            ]
            commands_dict = defaultdict(lambda: [])
            for name, app in get_commands().items():
                if app == 'django.core':
                    app = 'django'
                else:
                    app = app.rpartition('.')[-1]
                commands_dict[app].append(name)
            style = color_style()
            for app in sorted(commands_dict):
                usage.append("")
                usage.append(style.NOTICE("[%s]" % app))
                for name in sorted(commands_dict[app]):
                    usage.append("    %s" % name)
            # Output an extra note if settings are not properly configured
            if self.settings_exception is not None:
                usage.append(style.NOTICE(
                    "Note that only Django core commands are listed "
                    "as settings are not properly configured (error: %s)."
                    % self.settings_exception))

        return '\n'.join(usage)

    def fetch_command(self, subcommand):
        """
        Try to fetch the given subcommand, printing a message with the
        appropriate command called from the command line (usually
        "django-admin" or "manage.py") if it can't be found.
        """
        # Get commands outside of try block to prevent swallowing exceptions
        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:
            if os.environ.get('DJANGO_SETTINGS_MODULE'):
                # If `subcommand` is missing due to misconfigured settings, the
                # following line will retrigger an ImproperlyConfigured exception
                # (get_commands() swallows the original one) so the user is
                # informed about it.
                settings.INSTALLED_APPS
            else:
                sys.stderr.write("No Django settings specified.\n")
            sys.stderr.write(
                "Unknown command: %r\nType '%s help' for usage.\n"
                % (subcommand, self.prog_name)
            )
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, subcommand)
        return klass

    def autocomplete(self):
        """
        Output completion suggestions for BASH.

        The output of this function is passed to BASH's `COMREPLY` variable and
        treated as completion suggestions. `COMREPLY` expects a space
        separated string as the result.

        The `COMP_WORDS` and `COMP_CWORD` BASH environment variables are used
        to get information about the cli input. Please refer to the BASH
        man-page for more information about this variables.

        Subcommand options are saved as pairs. A pair consists of
        the long option string (e.g. '--exclude') and a boolean
        value indicating if the option requires arguments. When printing to
        stdout, an equal sign is appended to options which require arguments.

        Note: If debugging this function, it is recommended to write the debug
        output in a separate file. Otherwise the debug output will be treated
        and formatted as potential completion suggestions.
        """
        # Don't complete if user hasn't sourced bash_completion file.
        if 'DJANGO_AUTO_COMPLETE' not in os.environ:
            return

        cwords = os.environ['COMP_WORDS'].split()[1:]
        cword = int(os.environ['COMP_CWORD'])

        try:
            curr = cwords[cword - 1]
        except IndexError:
            curr = ''

        subcommands = list(get_commands()) + ['help']
        options = [('--help', False)]

        # subcommand
        if cword == 1:
            print(' '.join(sorted(filter(lambda x: x.startswith(curr), subcommands))))
        # subcommand options
        # special case: the 'help' subcommand has no options
        elif cwords[0] in subcommands and cwords[0] != 'help':
            subcommand_cls = self.fetch_command(cwords[0])
            # special case: add the names of installed apps to options
            if cwords[0] in ('dumpdata', 'sqlmigrate', 'sqlsequencereset', 'test'):
                try:
                    app_configs = apps.get_app_configs()
                    # Get the last part of the dotted path as the app name.
                    options.extend((app_config.label, 0) for app_config in app_configs)
                except ImportError:
                    # Fail silently if DJANGO_SETTINGS_MODULE isn't set. The
                    # user will find out once they execute the command.
                    pass
            parser = subcommand_cls.create_parser('', cwords[0])
            options.extend(
                (min(s_opt.option_strings), s_opt.nargs != 0)
                for s_opt in parser._actions if s_opt.option_strings
            )
            # filter out previously specified options from available options
            prev_opts = {x.split('=')[0] for x in cwords[1:cword - 1]}
            options = (opt for opt in options if opt[0] not in prev_opts)

            # filter options by current input
            options = sorted((k, v) for k, v in options if k.startswith(curr))
            for opt_label, require_arg in options:
                # append '=' to options which require args
                if require_arg:
                    opt_label += '='
                print(opt_label)
        # Exit code of the bash completion function is never passed back to
        # the user, so it's safe to always exit with 0.
        # For more details see #25420.
        sys.exit(0)

    def execute(self):
        """
        Given the command-line arguments, figure out which subcommand is being
        run, create a parser appropriate to that command, and run it.
        """
        # 先找出二级指令,没有二级指令就打印帮助信息
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        # 预处理的选项,这些选项会和当前传递的选项有冲突,所以先解析出这些选项,这样用户传递的选项才不会被影响.
        # Preprocess options to extract --settings and --pythonpath.
        # These options could affect the commands that are available, so they
        # must be processed early.
        parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
        # 这里是指定settings文件
        parser.add_argument('--settings')
        # 这里是指定python路径
        parser.add_argument('--pythonpath')
        parser.add_argument('args', nargs='*')  # catch-all
        try:
            options, args = parser.parse_known_args(self.argv[2:])
            # 修改环境settings和pythonpath
            handle_default_options(options)
        except CommandError:
            pass  # Ignore any option errors at this point.

        try:
            # django在启动时会创建settings = LazySettings()
            # 通过读取os.environ.get('DJANGO_SETTINGS_MODULE'),来初始化settings对象
            # settings是一个lazy对象,使用self._wrapped保存Settings对象,当读取属性时,lazy对象会先进行_setup,然后会调用getattr(self._wrapped,key)
            # 当要读取INSTALLED_APPS时,会先进行_setup
            # 说白了就是LazySetting对象读取属性时,会真正初始化Settings对象,并赋值给LazySetting._wrapped=Settings()
            settings.INSTALLED_APPS
        except ImproperlyConfigured as exc:
            self.settings_exception = exc

        if settings.configured:
            # 就是返回self._wrapped is not empty,当前是否已经初始化好了settings
            # Start the auto-reloading dev server even if the code is broken.
            # The hardcoded condition is a code smell but we can't rely on a
            # flag on the command class because we haven't located it yet.
            if subcommand == 'runserver' and '--noreload' not in self.argv:
                try:
                    # 执行django.setup,如果有错误那么
                    autoreload.check_errors(django.setup)()
                except Exception:
                    # The exception will be raised later in the child process
                    # started by the autoreloader. Pretend it didn't happen by
                    # loading an empty list of applications.
                    apps.all_models = defaultdict(OrderedDict)
                    apps.app_configs = OrderedDict()
                    apps.apps_ready = apps.models_ready = apps.ready = True

                    # Remove options not compatible with the built-in runserver
                    # (e.g. options for the contrib.staticfiles' runserver).
                    # Changes here require manually testing as described in
                    # #27522.
                    _parser = self.fetch_command('runserver').create_parser('django', 'runserver')
                    _options, _args = _parser.parse_known_args(self.argv[2:])
                    for _arg in _args:
                        self.argv.remove(_arg)

            # In all other cases, django.setup() is required to succeed.
            else:
                # 执行django.setup
                django.setup()

        self.autocomplete()

        if subcommand == 'help':
            if '--commands' in args:
                sys.stdout.write(self.main_help_text(commands_only=True) + '\n')
            elif len(options.args) < 1:
                sys.stdout.write(self.main_help_text() + '\n')
            else:
                self.fetch_command(options.args[0]).print_help(self.prog_name, options.args[0])
        # Special-cases: We want 'django-admin --version' and
        # 'django-admin --help' to work, for backwards compatibility.
        elif subcommand == 'version' or self.argv[1:] == ['--version']:
            sys.stdout.write(django.get_version() + '\n')
        elif self.argv[1:] in (['--help'], ['-h']):
            sys.stdout.write(self.main_help_text() + '\n')
        else:
            # 这里执行fetch_command('runserver').run_from_argv(['/Users/mering/Proje...manage.py', 'runserver', '--noreload', '--nothreading'])
            # runserver 对应的是django.contrib.staticfiles
            # 加载该class import_module('%s.management.commands.%s' % (app_name, name))
            # import_module('django.contrib.staticfiles.management.commands.runserver')
            # 放回的fetch_command(subcommand)=django.contrib.staticfiles.management.commands.runserver.Command()
            # django.contrib.staticfiles.management.commands.runserver.Command继承自django.core.management.Command,
            # run_from_argv会调用django.core.management.Command.excute-->django.core.management.BaseCommand.excute
            # django.core.management.commands.runserver.Command.handle
            # django.core.management.commands.runserver.Command.run
            # django.core.management.commands.runserver.Command.inner_run
            # django.contrib.staticfiles.management.commands.runserver.Command.get_handler  获得wsgiapp
            #  Debug模式下返回StaticFilesHandler
            # django.core.servers.run
            # def run(addr, port, wsgi_handler, ipv6=False, threading=False, server_cls=WSGIServer):
            #     server_address = (addr, port)
            #     if threading:
            #         # 创建一个新类型继承自socketserver.ThreadingMixIn和WSGIServer
            #         httpd_cls = type('WSGIServer', (socketserver.ThreadingMixIn, server_cls), {})
            #     else:
            #         httpd_cls = server_cls
            #     httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
            #     if threading:
            #         # ThreadingMixIn.daemon_threads indicates how threads will behave on an
            #         # abrupt shutdown; like quitting the server by the user or restarting
            #         # by the auto-reloader. True means the server will not wait for thread
            #         # termination before it quits. This will make auto-reloader faster
            #         # and will prevent the need to kill the server manually if a thread
            #         # isn't terminating correctly.
            #         httpd.daemon_threads = True
            #     httpd.set_app(wsgi_handler)
            #     httpd.serve_forever()
            self.fetch_command(subcommand).run_from_argv(self.argv)


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
