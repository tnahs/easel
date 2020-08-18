from logging import log
from src.easel import Easel


easel = Easel("examples/template")


if __name__ == "__main__":

    easel.run(loglevel="DEBUG")
