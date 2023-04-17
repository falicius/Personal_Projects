import curses
from curses import textpad, ascii
from datetime import datetime
import asyncio


class Terminal:
    def __init__(self):
        self.screen = curses.initscr()
        y, x = self.screen.getmaxyx()
        self.output = self.screen.subwin(y - 1, x, 0, 0)
        self.prompt = curses.newwin(1, x, y - 1, 0)
        self.prompt_string = '>:'
        self.done = False
        self._initialize()
        self._rebuild_prompt()
        self.commands = {
            'quit': self.quit,
            'clear': self.clear,
            'time': self._time,
            'help': self.help,
            'log': self.debug,
        }

    def _initialize(self):
        curses.init_pair(1, curses.COLOR_YELLOW, 0)
        curses.init_pair(2, curses.COLOR_RED, 0)
        curses.init_pair(3, curses.COLOR_WHITE, 0)
        curses.init_pair(4, curses.COLOR_CYAN, 0)
        self.WARN_LOG = curses.color_pair(1)
        self.ERR_LOG = curses.color_pair(2)
        self.INFO_LOG = curses.color_pair(3)
        self.DEBUG_LOG = curses.color_pair(4)
        self.edit = textpad.Textbox(self.prompt, insert_mode=True)
        self.output.scrollok(True)

    def _rebuild_prompt(self, default_text=None):
        self.prompt.clear()
        self.prompt.addstr(self.prompt_string)
        if default_text:
            self.prompt.addstr(default_text)
        self._reset()

    def _resize(self):
        max_y, max_x = self.screen.getmaxyx()
        self.output.resize(max_y - 1, max_x)
        self.prompt.resize(1, max_x)
        self.prompt.mvwin(max_y - 1, 0)

    def _refresh(self):
        self.output.refresh()
        self.prompt.refresh()

    def _time(self):
        time = str(datetime.utcnow().isoformat())
        self.output.addstr(time + '\n')

    def warning(self, str='warning'):
        self.output.addstr(str + '\n', self.WARN_LOG)

    def error(self, str='error'):
        self.output.addstr(str + '\n', self.ERR_LOG)

    def info(self, str='info'):
        self.output.addstr(str + '\n', self.INFO_LOG)

    def debug(self, str='debug'):
        self.output.addstr(str + '\n', self.DEBUG_LOG)

    def _cmd(self, cmd):
        # check if cmd is a key in dictionary
        if cmd in self.commands:
            return self.commands[cmd]()
        self.output.addstr(cmd + '\n')

    def _validate_input(self, key):
        if key == ord('\n'):
            return curses.ascii.BEL
        if key == 127:
            key = curses.KEY_BACKSPACE
        if key in (curses.ascii.STX, curses.KEY_LEFT, curses.ascii.BS, curses.KEY_BACKSPACE):
            min_x = len(self.prompt_string)
            y, x = self.prompt.getyx()
            if x == min_x:
                return None
            if key == curses.KEY_BACKSPACE:
                self.curx -= 1
            return key
        if key == curses.KEY_RIGHT:
            y, x = self.prompt.getyx()
            if x == self.curx:
                return None
            return key
        if key == curses.KEY_RESIZE:
            return None
        if curses.ascii.isalnum(key):
            self.curx += 1
        return key

    def _input(self):
        while True:
            self.input_string = self.edit.edit(self._validate_input)
            self.input_string = self.input_string[len(self.prompt_string):len(self.input_string) - 1]
            self._rebuild_prompt()
            return self._cmd(self.input_string)

    def restore_screen(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    async def __input(self):
        while not self.done:
            await asyncio.sleep(0.1)
            await asyncio.to_thread(self._input)

    async def __refresh(self):
        while not self.done:
            await asyncio.sleep(0.1)
            await asyncio.to_thread(self._resize)
            await asyncio.to_thread(self._refresh)

    async def run(self) -> None:
        await asyncio.gather(
            self.__input(), self.__refresh())

    def _reset(self):
        # reset the cursor position counter
        self.curx = 2

    def quit(self):
        self.restore_screen()
        self.done = True

    def clear(self):
        self.output.clear()

    def help(self):
        self.output.addstr(str(self.commands.keys()) + '\n')


def main(stdscr):
    display = Terminal()
    asyncio.run(display.run())


if __name__ == '__main__':
    curses.wrapper(main)
