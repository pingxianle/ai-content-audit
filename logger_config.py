import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="server.log",
    datefmt="%Y-%m-%d %H:%M:%S"
)
