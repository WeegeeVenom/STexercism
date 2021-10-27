import sublime
import sublime_plugin
import subprocess
import re


class StexercismSubmitCurrentFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            submit_cli = subprocess.check_output(
                ["exercism",
                "submit",
                self.view.file_name()],
                stderr=subprocess.STDOUT)
            sublime.active_window().run_command(
                "show_panel",
                {"panel": "console", "toggle": True})
            print(submit_cli.decode('UTF-8').strip())
        except subprocess.CalledProcessError as err:
            raise RuntimeError(
                "command '{}' returned with error (code {}): {}.".format(
                    err.cmd,
                    err.returncode,
                    err.output.decode('UTF-8').strip())
                + "\n\nMaybe you submitted the wrong file?")

# TODO: make sure you get the right file? this would be very language dependent


class StexercismOpenCurrentExerciseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        match = re.search(
            r'exercism/\w*/([-\w]*)/',
            self.view.file_name())
        if match:
            open_cli = subprocess.check_output([
                "exercism",
                "open",
                match.group(1)])

class StexercismTestCurrentFilePythonCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            submit_cli = subprocess.check_output(
                ["python",
                "-m",
                "pytest",
                self.view.file_name()[:-3]+"_test.py"],
                stderr=subprocess.STDOUT)
            sublime.active_window().run_command(
                "show_panel",
                {"panel": "console", "toggle": True})
            print(submit_cli.decode('UTF-8').strip())
        
        except subprocess.CalledProcessError as err:
            
            if err.returncode == 1: #This is an exception made for if there are failed tasks
                print(err.output.decode('UTF-8').strip())
                pass
            else:
                raise RuntimeError(
                    "command '{}' returned with error (code {}): {}.".format(
                        err.cmd,
                        err.returncode,
                        err.output.decode('UTF-8').strip())
                    + "\n\nMaybe you are checking the wrong file?")

#TODO: Add more tracks, possibly make it a list on Sublime to not fill command list.

def convert(text):
	s = ''.join(ch for ch in text if ch.isalnum() or ch == " ")
    str_list = s.strip().split()
    return "-".join(str_list).lower()

def converttrack(text):
	str_list = s.strip().split()
    return "-".join(str_list).lower()

class StexercismExerciseNameInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "exername"

    def placeholder(self):
        return "Exercise Name"

    def next_input(self, args):
        if 'trackname' not in args:
            return StexercismTrackNameInputHandler()

class StexercismTrackNameInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "trackname"

    def placeholder(self):
        return "Track Name"

class StexercismDownloadFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, exername, trackname): #unfinished
        try:
            submit_cli = subprocess.check_output(
                ["exercism",
                "download",
                "--exercise=" + convert(exername),
                "--track=" + converttrack(trackname)],
                stderr=subprocess.STDOUT)
            sublime.active_window().run_command(
                "show_panel",
                {"panel": "console", "toggle": True})
            print(submit_cli.decode('UTF-8').strip())
        except subprocess.CalledProcessError as err:
            raise RuntimeError(
                "command '{}' returned with error (code {}): {}.".format(
                    err.cmd,
                    err.returncode,
                    err.output.decode('UTF-8').strip()))

    def input(self, args):
        if 'exername' not in args:
            return StexercismExerciseNameInputHandler()
        elif 'trackname' not in args:
            return StexercismTrackNameInputHandler()