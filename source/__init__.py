import sys

if sys.argv[0] != "-m" and not sys.argv[0].endswith("pytest"):
    from .git_plugin_action import GitPluginAction

    GitPluginAction().register()
