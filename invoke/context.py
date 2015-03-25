from .runner import Local
from .config import Config, DataProxy


class Context(DataProxy):
    """
    Context-aware API wrapper & state-passing object.

    `.Context` objects are created during command-line parsing (or, if desired,
    by hand) and used to share parser and configuration state with executed
    tasks (see :doc:`/concepts/context`).

    Specifically, the class offers wrappers for core API calls (such as `.run`)
    which take into account CLI parser flags, configuration files, and/or
    changes made at runtime. It also acts as a proxy for its `~.Context.config`
    attribute - see that attribute's documentation for details.

    Instances of `.Context` may be shared between tasks when executing
    sub-tasks - either the same context the caller was given, or an altered
    copy thereof (or, theoretically, a brand new one).
    """
    def __init__(self, config=None):
        """
        :param config:
            `.Config` object to use as the base configuration.

            Defaults to an empty `.Config`.
        """

        #: The fully merged `.Config` object appropriate for this context.
        #:
        #: `.Config` settings (see their documentation for details) may be
        #: accessed like dictionary keys (``ctx.config['foo']``) or object
        #: attributes (``ctx.config.foo``).
        #:
        #: As a convenience shorthand, the `.Context` object proxies to its
        #: ``config`` attribute in the same way - e.g. ``ctx['foo']`` or
        #: ``ctx.foo`` returns the same value as ``ctx.config['foo']``.
        self.config = config if config is not None else Config()

    # TODO: make this take 'command', not *args
    def run(self, *args, **kwargs):
        """
        Execute a local shell command, honoring config options.

        Specifically, this method:

        * starts with a copy of the ``run`` tree of this object's `.Config`
          (which may be blank, or may contain keys mapping to keyword arguments
          such as ``echo``);
        * merges any given ``kwargs`` into that dict;
        * instantiates a `.Runner` subclass (according to the ``runner``
          parameter) and calls its `.Local.run` method, with this method's
          ``args``, and the above dict as its ``kwargs``.
        """
        # TODO: this can become a one liner
        options = dict(self.config.get('run', {}))
        runner = kwargs.pop('runner', Local)
        options.update(kwargs)
        return runner().run(*args, **options)
