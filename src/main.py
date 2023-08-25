import curses
import os

from azure.devops.v7_0.git.models import GitRepository
from git import Repo

from azdevops import AzDevopsManager

stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

ORGANIZATION = "test_org"
PROJECT = "test_proj"


def repository_exists(repository: GitRepository) -> bool:
    repo_directory = os.path.join(os.getcwd(), repository.name)
    if os.path.exists(repo_directory):
        return True
    return False


def confirm_clone(selected_repository: GitRepository) -> bool:
    stdscr.clear()
    stdscr.addstr(
        0,
        0,
        f"Do you want to clone {selected_repository.name} to the current working directory? (y/n)",  # noqa: E501
    )
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key in [ord("y"), ord("Y")]:
            return True
        elif key in [ord("n"), ord("N")]:
            return False


def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    # List of strings to display
    azdevops_manager = AzDevopsManager(PROJECT, ORGANIZATION)
    repositories = azdevops_manager.get_repositories()
    selected_item = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for index, repo in enumerate(repositories):
            y = index + 1
            x = 2

            if y < height - 1:
                if index == selected_item:
                    stdscr.addstr(
                        y, x, repo.name, curses.A_REVERSE
                    )  # Highlight selected item
                else:
                    stdscr.addstr(y, x, repo.name)
            else:
                stdscr.addstr(height - 1, x, "...")
                break

        stdscr.refresh()

        # Wait for user input
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_item > 0:
            selected_item -= 1
        elif key == curses.KEY_DOWN and selected_item < len(repositories) - 1:
            selected_item += 1
        elif key == 10:  # Check for Enter key press (ASCII code 10)
            selected_repository = repositories[selected_item]
            should_clone = confirm_clone(selected_repository)
            if should_clone:
                # Clone the repository to the current working directory
                remote_url = azdevops_manager.get_remote_url_with_pat(
                    selected_repository
                )
                Repo.clone_from(remote_url, selected_repository.name)
                break

        elif key == 27:  # Exit if the user presses the ESC key
            break


# Run the curses application
curses.wrapper(main)
