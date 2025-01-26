#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

import os
import subprocess
import shlex


def execute_command(command):
    """Execute external commands and handle piping."""
    try:
        if "|" in command:
            # Split and handle piping
            commands = [shlex.split(cmd.strip()) for cmd in command.split("|")]
            prev_process = None

            for cmd in commands:
                if prev_process is None:
                    # First command, no input stream yet
                    prev_process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                else:
                    # Pipe previous command's output as input
                    prev_process = subprocess.Popen(
                        cmd, stdin=prev_process.stdout, stdout=subprocess.PIPE
                    )

            # Wait for the last process to complete and print its output
            output, error = prev_process.communicate()
            if output:
                print(output.decode(), end="")
            if error:
                print(error.decode(), end="")
        else:
            # Handle a single command
            subprocess.run(shlex.split(command))
    except FileNotFoundError:
        print(f"psh: command not found: {command}")
    except Exception as e:
        print(f"psh: error: {e}")


def psh_cd(path):
    """Convert to absolute path and change directory."""
    try:
        if path.strip():
            os.chdir(os.path.abspath(path))
        else:
            os.chdir(os.path.expanduser("~"))  # Default to the home directory
    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")
    except Exception as e:
        print(f"cd: error: {e}")


def psh_help():
    """Print help message."""
    print("psh: A simple Python shell.\nSupports basic commands like cd, help, and external programs.")


def main():
    """Main loop for the shell."""
    while True:
        try:
            inp = input("$ ").strip()
            if not inp:
                continue
            if inp == "exit":
                break
            elif inp.startswith("cd "):
                psh_cd(inp[3:].strip())
            elif inp == "help":
                psh_help()
            else:
                execute_command(inp)
        except KeyboardInterrupt:
            print("\nType 'exit' to quit.")
        except EOFError:
            print("\nExiting shell.")
            break


if __name__ == "__main__":
    main()
