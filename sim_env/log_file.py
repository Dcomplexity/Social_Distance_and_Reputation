import logging


def create_logger(name=None, file_name=None, file_level=logging.DEBUG, stream_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # Use FileHandler logging to file on disk
    fh = logging.FileHandler(file_name, mode='w')
    fh.setLevel(file_level)
    fh.setFormatter(formatter)

    # Use StreamHandler logging to screen
    ch = logging.StreamHandler()
    ch.setLevel(stream_level)
    ch.setFormatter(formatter)

    # Add these two Handler
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

