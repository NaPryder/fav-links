from django.core.management import BaseCommand
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


from cli.extract_prompts import extract_input, get_command_help_texts
from fav_link.command_actions import CommandActions

import argparse


def check_exit_command(message: str):
    if message.lower().startswith("exit"):
        print("exit")
        exit()


def process_authenticate():
    current_user = None
    while current_user is None:
        # process
        print("Please login")
        username = input("Enter [username]: ").strip()
        password = input("Enter [password]: ").strip()

        current_user = authenticate(username=username, password=password)
        print("--login user", current_user)

        if not current_user:
            print("Invalid user.")
            prompt = input("Retry (enter 'y') or exit (enter any key): ")

            if prompt.strip().lower() == "y":
                continue
            else:
                print("exit")
                exit()
        print("Login success")
        return current_user


class Command(BaseCommand):
    help = "Start CLI"

    def handle(self, *args, **options):
        print(CommandActions._help_commands)
        print(CommandActions._commands)
        argparse.ArgumentParser()

        # by pass auth
        # current_user = process_authenticate()
        current_user = User.objects.get(username="root")

        print("  current user", current_user)

        commands = CommandActions(user=current_user)

        while True:

            message = input("Enter action or exit or help: ").strip()

            command_keyword, parameters = extract_input(message)

            check_exit_command(command_keyword)
            if command_keyword == "help":
                print(get_command_help_texts(commands._help_commands))
                continue

            if command_keyword == "":
                continue

            method = commands._commands.get(command_keyword)
            if not method:
                print("Invalid command")
                continue

            try:
                method(commands, **parameters)

            except Exception as error:
                print("Error", error)
                print()
                print(commands._help_commands.get(command_keyword))

            finally:
                print()

            # get_command_method()

        # print("--end")
