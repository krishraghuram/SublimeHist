"""
Sublime command to print frequency of lines

TODO:
* Add commands for separators like "," and "\t"
* Allow arbitrary separators
* Sort JSON output by key (to make it easier for user to quickly lookup a word/line)
* Sort JSON output by value (to easily see which words/lines are occuring most)
"""

import json
import pprint
import collections

import sublime
import sublime_plugin


class HistLinesCommand(sublime_plugin.TextCommand):
    """
    Logic:
    Get full text from current file
    Do frequency counting of lines
    Open a new window, and print frequency counts as csv/tsv
    """
    def run(self, edit):
        # Get full text from current file
        lines = self.view.substr(sublime.Region(a=0,b=self.view.size())).splitlines()
        
        # Do frequency counting of lines
        hist = {unique_line:0 for unique_line in set(lines)}
        for line in lines:
            hist[line] += 1
        content = json.dumps(hist, indent=4)
        
        # Open a new window, and print frequency counts as csv/tsv
        scratch = self.view.window().new_file()
        scratch.set_scratch(True)
        scratch.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        scratch.run_command('insert_content', {'content': content})


class InsertContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, content):
        self.view.insert(edit, 0, content)
