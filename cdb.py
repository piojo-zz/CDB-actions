'''Module encapsulating the operations on CDB'''
import os
import sys

class cdb_error(Exception):
    '''Exception for errors dealing with CDB'''
    def __init__(self, descro, process):
        self.msg = descro
        self.process = process

    def __str__(self):
        lines = [self.msg, "\nStandard output:\n"]
        lines.extend(l for l in self.process.stdout)
        lines.append("\nStandard error:\n")
        lines.extend(l for l in self.process.stderr)
        return "".join(lines)

def do_commit(*arg):
    '''Commits the modified templates to CDB'''
    cdbcmd = ('update ' + ' '.join(arg) +
              '; commit -c "Upgrade templates that come from external sources')
    cdbcall = [ 'cdbop', '--server', 'cdbserv', '--cfgfile', '/dev/fd/0',
                '--command',  cdbcmd]

    p = subprocess.Popen(cdbcall, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    if not os.environ.has_key('CDB_USER'):
        p.stdin.write('use-krb5=1\n')
    p.stdin.close()
    if p.wait() != 0:
        raise cdb_error("Failed to commit to CDB", p)

    
