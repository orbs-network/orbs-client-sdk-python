from subprocess import run


def start_gamma_server(port='8080'):
    run(['gamma-cli', 'start-local', '-port', port, '-wait'])


def stop_gamma_server():
    run(['gamma-cli', 'stop-local'])
