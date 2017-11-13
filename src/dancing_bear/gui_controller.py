from mog_commons.command import capture_command


class GUIController:
    def __init__(self, url='http://localhost:8000/bpm.html', executable = '/usr/local/bin/chrome-cli'):
        cmd = [executable, 'open', url]
        ret, out, err = capture_command(cmd)

        if ret:
            raise RuntimeError('Failed to open URL: %s' % url)
        tab_id = out.splitlines(False)[0].split(b' ')[1]
        self.executable = executable
        self.tab_id = tab_id
        self.cmd_prefix = [executable, 'execute']
        self.beat = 0

    def play_downbeat(self):
        self._play_beat(1)

    def play_upbeat(self):
        self._play_beat(min(4, self.beat + 1))

    def send_bpm(self, bpm):
        self._execute_command(['document.getElementById("bpm").innerHTML = "%s";' % bpm])

    def stop_play(self):
        self.send_bpm('???')

    def _play_beat(self, next_beat):
        self._execute_command(['document.getElementById("beat%d").click();' % next_beat])
        self.beat = next_beat

    def _execute_command(self, cmd):
        capture_command(args=self.cmd_prefix + cmd + ['-t', self.tab_id])

    def close(self):
        capture_command(args=[self.executable, 'close', '-w'])
