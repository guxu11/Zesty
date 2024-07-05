# coding=utf-8

import os

def read_pid():
        with open('uwsgi/uwsgi.pid') as f:
                pid = int(f.readline())

        return pid

def kill_process(pid):
        kill_cmd = 'kill -9 {}'.format(pid)
        resp = os.system(kill_cmd)
        return resp

if __name__ == '__main__':
        pid = read_pid()
        resp = kill_process(pid)
        if resp == 0:
                print('kill pid: {} successfully!'.format(pid))
        else:
                print('kill pid: {} failed!'.format(pid))
