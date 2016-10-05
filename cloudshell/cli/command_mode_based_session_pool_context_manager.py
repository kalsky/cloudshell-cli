from cloudshell.cli.command_mode import CommandMode
from cloudshell.cli.command_mode_helper import CommandModeHelper
from cloudshell.cli.session_pool import SessionPool
from cloudshell.cli.command_mode_session_wrapper import CommandModeSessionWrapper


class CommandModeBasedSessionPoolContextManager(object):
    """
    Get and return session from pool and change mode if specified
    """

    def __init__(self, session_pool, command_mode=None, logger=None, **session_attributes):
        """
        :param session_pool:
        :type session_pool: SessionPool
        """
        self._session_pool = session_pool
        self._command_mode = command_mode
        self._session_attributes = session_attributes
        self._logger = logger
        self._wrapped_session = None

    def __enter__(self):
        prompts_re = r'|'.join(CommandMode.DEFINED_MODES.keys())
        session = self._session_pool.get_session(logger=self._logger, prompt=prompts_re,
                                                 **self._session_attributes)
        self._wrapped_session = CommandModeSessionWrapper(session, self._command_mode, self._logger)
        if self._command_mode:
            CommandModeHelper.change_session_mode(self._wrapped_session, self._command_mode, self._logger)
        return self._wrapped_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session_pool.return_session(self._wrapped_session.session, self._logger)