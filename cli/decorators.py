def build_action_message(
    command_keyword: str, accept_params_text: str, description: str
):

    return "- {kw} {params}\n \t{descr}\n".format(
        kw=command_keyword,
        descr=description,
        params=accept_params_text,
    )


def class_register_commands(cls):
    cls._commands = {}
    cls._help_commands = {}
    for methodname in dir(cls):
        method: object = getattr(cls, methodname)

        if hasattr(method, "_command_keyword"):
            _command_keyword = getattr(method, "_command_keyword", None) or methodname
            _accept_params_text = getattr(method, "_accept_params_text", None) or ""
            _description = getattr(method, "_description", None) or ""

            cls._commands[_command_keyword] = method
            cls._help_commands[_command_keyword] = build_action_message(
                _command_keyword, _accept_params_text, _description
            )
    return cls


def register_command(
    command_keyword: str = None, params: str = None, description: str = ""
):
    def wrapper(func):
        func._command_keyword = command_keyword
        func._accept_params_text = params
        func._description = description
        return func

    return wrapper
