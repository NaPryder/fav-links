import re

from cli.decorators import build_action_message


EXTRACT_OPTION_PATTERN = r"""([a-zA-Z]+)=([^\s]+)"""


def casting_parameter_type(params: list[str]):
    casted = {}
    for key, value in params:
        if isinstance(value, str):
            value = value.replace("'", "").replace('"', "")
            if value == "":
                continue

            elif value.isnumeric():
                value = int(value)

            elif value == "None":
                value = None

            # print(eval(value), type(eval(value)))

        if key == "id":
            key = "_id"

        casted[key] = value

    return casted


def extract_input(text: str):

    splitted = text.split(" ")
    if not splitted:
        raise Exception("Enter command " "or enter --help for see actions")

    command_keyword = splitted[0]
    args = text[len(command_keyword) :]
    args_spliter = re.findall(EXTRACT_OPTION_PATTERN, args)
    parameters = casting_parameter_type(args_spliter)

    return command_keyword, parameters


def get_command_help_texts(help_commands: dict):

    texts = ["Actions you can do:"]
    # add parking lot commands
    for help_text in help_commands.values():
        texts.append(help_text)

    # add common commands
    texts.append(build_action_message("help", "", "Display help"))
    texts.append(build_action_message("exit", "", "Return to shell"))
    texts.append(f"")
    texts.append(f"*** The format of command")
    texts.append(f"1. The first argument must be action name.")
    texts.append(f"2. The rest of arguments will parameter.")
    texts.append(f"3. Using '=' for assign parameter value.")
    texts.append(f"4. Text without space can leave double quote i.e. param=hello")
    texts.append(
        f'5. If parameter has space, you need to place value between double quote i.e. param="hello world"'
    )
    texts.append(f"6. Tags parameter can use , (comma) for seperate value to list")
    texts.append(f"")
    texts.append(
        f"""Follow this format: [action] param1=value param2=value2 param3="string with space" """
    )
    texts.append(" For example:")
    texts.append(f'   - list title=new category="hello world" tags=python,py')
    texts.append(f"   - get id=1")
    texts.append(f"")

    return "\n".join(texts)
