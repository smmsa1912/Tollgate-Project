import os
import sys
import subprocess
import signal
import atexit
import re
import netifaces
import logging
import colorlog
import platform
import uvicorn

# Setup colored logging
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s:%(reset)s     %(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Global variables to store process objects
redis_process = None
celery_process = None
cleanup_done = False  # Flag to track if cleanup has been done


def start_celery_redis():
    """Starts Redis and Celery workers."""
    global redis_process, celery_process
    os.environ['REDIS_STATUS'] = '0'
    os.environ['CELERY_STATUS'] = '0'
    logger.info('Starting Redis Server...')
    try:
        redis_process = subprocess.Popen(['redis-server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Redis Server started with PID: {redis_process.pid}")
    except FileNotFoundError:
        logger.error(
            "Redis Server not found. Make sure it is installed and in your PATH. (HINT : sudo apt install redis)")
        sys.exit(1)

    logger.info('Starting Celery Workers...')
    try:
        celery_process = subprocess.Popen(['celery', '-A', 'CoreApp', 'worker', '--loglevel=INFO'],
                                          stdout=subprocess.PIPE)  # remove stderr=subprocess.PIPE to view celery bg taskss
        logger.info(f"Celery Workers started with PID: {celery_process.pid}")
    except Exception as e:
        logger.error(f"Failed to start Celery Workers: {str(e)}")
        stop_celery_redis()
        sys.exit(1)

    if redis_process.poll() is not None:
        logger.error("Redis Server failed to start. Exiting...")
        stop_celery_redis()
        sys.exit(1)
    elif celery_process.poll() is not None:
        logger.error("Celery Workers failed to start. Exiting...")
        stop_celery_redis()
        sys.exit(1)
    else:
        os.environ['REDIS_STATUS'] = '1'
        os.environ['CELERY_STATUS'] = '1'
        logger.info("Redis Server and Celery Workers started...\n")


def stop_celery_redis():
    """Stops Redis and Celery workers."""
    global redis_process, celery_process
    if redis_process and redis_process.poll() is None:
        logger.info(f"Stopping Redis Server (PID: {redis_process.pid})...")
        redis_process.terminate()  # Terminate the process
        redis_process.wait()  # Wait for the process to finish
        logger.info("Redis Server stopped.")
        os.environ['REDIS_STATUS'] = '0'
        redis_process = None

    if celery_process and celery_process.poll() is None:
        logger.info(f"Stopping Celery Workers (PID: {celery_process.pid})...")
        celery_process.terminate()  # Terminate the process
        celery_process.wait()  # Wait for the process to finish
        logger.info("Celery Workers stopped.")
        os.environ['CELERY_STATUS'] = '0'
        celery_process = None


def handle_exit(signum, frame):
    """Handles cleanup and process termination on signals."""
    global cleanup_done
    if cleanup_done:
        return  # Prevent the cleanup from being done multiple times
    cleanup_done = True
    if os.environ.get('REDIS_STATUS') == '1' or os.environ.get('CELERY_STATUS') == '1':
        logger.info("Cleaning up before exiting...")
        stop_celery_redis()  # Stop Redis and Celery

    sys.exit(0)


def fetch_ip():
    def _get_machine_ip():
        """Get the local machine's IP address using netifaces."""
        ip = "127.0.0.1"  # Default to localhost if no network interface is found
        try:
            # Loop through network interfaces to find the correct IP address
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    # Pick the first available IPv4 address
                    ip = addrs[netifaces.AF_INET][0]['addr']
                    if ip != "127.0.0.1":
                        break
        except ValueError:
            logger.error("Could not determine machine's IP address.")
        return ip

    if not len(sys.argv) > 2:
        ip, port = _get_machine_ip(), "8000"
        return ip, port

    ip_pattern = r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)$"
    if re.match(ip_pattern, sys.argv[2]):
        ip, port = sys.argv[2].split(":")
        if not re.match(r"^\d{1,5}$", port) and not (0 <= int(port) <= 65535) or not re.match(
                r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            logger.warning("FAILED TO FETCH IP AND PORT. USING DEVICE IP AND PORT 8000")
            ip, port = _get_machine_ip(), "8000"

        return ip, port


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoreApp.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.critical("Couldn't import Django. Are you sure it's installed and available?")
        raise exc

    signal.signal(signal.SIGINT, handle_exit)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, handle_exit)  # Handle termination signals
    atexit.register(stop_celery_redis)  # Ensure cleanup on normal exit

    if os.environ.get("RUN_MAIN") == "true":
        if "runserver" in sys.argv:
            if platform.system() == "Windows":
                logger.warning("Windows is not supported for running this server. (celery and redis will not start)")
            else:
                start_celery_redis()
            try:
                ip, port = fetch_ip()
            except Exception as exc:
                logger.error(f"Failed to fetch IP and Port: {str(exc)}")
                ip, port = "127.0.0.1", "8000"
            os.environ["Server_IP"] = ip
            os.environ["Server_PORT"] = port
            uvicorn.run("CoreApp.asgi:application", host=ip, port=int(port), log_level="info", reload=True)
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
