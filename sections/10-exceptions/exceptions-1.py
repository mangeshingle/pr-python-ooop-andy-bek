import random
import string
import time

from rich.console import Console

console = Console(force_terminal=True, stderr=False)


class BaseValueException(Exception):
    def __str__(self):
        return self.message


class InvalidValueException(BaseValueException):
    def __init__(self, message="InvalidValueException"):
        self.message = message
        super().__init__(self.message)


class BeforeValueException(BaseValueException):
    def __init__(self, message="BeforeValueException"):
        self.message = message
        super().__init__(self.message)


class AfterValueException(BaseValueException):
    def __init__(self, message="AfterValueException"):
        self.message = message
        super().__init__(self.message)


class LetterGuessingGame:
    def __init__(self):
        self.system_pick = random.choice(string.ascii_lowercase)
        self.end_time = 0
        self.after_guess_counter = 0
        self.before_guess_counter = 0
        console.print(
            f"[blue]The computer has chosen a letter['{self.system_pick}'].\nWhat do you think it was? : [/blue]"
        )
        self.start_time = time.time()
        self.user_pick = input()

    def validate(self, value):
        if isinstance(value, str) and len(value) == 1:
            value = value.lower()
            if value in string.ascii_lowercase:
                return

        raise InvalidValueException

    def start(self):
        try:
            diff = ord(self.system_pick) - ord(self.user_pick)
            match diff:
                case value if value > 0:  # After
                    self.after_guess_counter += 1
                    raise AfterValueException("after")
                case value if value < 0:  # Before
                    self.before_guess_counter += 1
                    raise BeforeValueException("before")
                case _:  # Stop
                    console.print("[green]That was correct! [/green]")
        except (AfterValueException, BeforeValueException) as abve:
            console.print(f"\n[red]Nope, it was something {abve}, guess again[/red]")
            self.user_pick = input()
            self.start()

    @property
    def user_pick(self):
        return self._user_pick

    @user_pick.setter
    def user_pick(self, value):
        try:
            self.validate(value)
            self._user_pick = value.lower()
        except InvalidValueException as ive:
            console.print(
                "[red]Not a valid input, please provide english alphabet : [/red]"
            )
            self._user_pick = input()


if __name__ == "__main__":
    try:
        lgg = LetterGuessingGame()
        lgg.start()
    except Exception as e:
        console.print("Something went wrong...")
    finally:
        lgg.end_time = time.time()
        console.print(
            f"[green]You played for {lgg.end_time - lgg.start_time:.4f} seconds and made {lgg.before_guess_counter} before guess and {lgg.after_guess_counter} after guesses.[/green]"
        )
