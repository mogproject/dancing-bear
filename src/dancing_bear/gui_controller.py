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

    def play_downbeat(self):
        pass

    def play_upbeat(self):
        pass

    def send_bpm(self, bpm):
        self._execute_command(['document.getElementById("bpm").innerHTML = "%s";' % bpm])

    def stop_play(self):
        self.send_bpm('???')

    def _execute_command(self, cmd):
        capture_command(args=self.cmd_prefix + cmd + ['-t', self.tab_id])
    
    def close(self):
        capture_command(args=[self.executable, 'close', '-w'])
