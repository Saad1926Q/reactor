import errno
import os
import select

pipe_paths = ["/tmp/test_pipe01", "/tmp/test_pipe02", "/tmp/test_pipe03"]

for path in pipe_paths:
    try:
        os.mkfifo(path)
    except FileExistsError:
        pass

fds = [os.open(path, os.O_RDONLY | os.O_NONBLOCK) for path in pipe_paths]


def handle_fd(fd, idx):
    try:
        data = os.read(fd, 100)
    except OSError as e:
        if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
            return
        raise

    if data:
        print(data.decode(), end="")
    else:
        os.close(fd)
        fds[idx] = os.open(pipe_paths[idx], os.O_RDONLY | os.O_NONBLOCK)


while True:
    try:
        readable, _, _ = select.select(fds, [], [])

        for fd in readable:
            idx = fds.index(fd)
            handle_fd(fd, idx)
    except KeyboardInterrupt:
        break

# Clean up
for fd in fds:
    os.close(fd)

for path in pipe_paths:
    os.unlink(path)
