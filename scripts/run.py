import pathlib
import sys


path_src = str(pathlib.Path(__file__).resolve().parent.parent / "src")
sys.path.append(path_src)


from easel import Easel


easel = Easel("./examples/sorolla-demo", debug=True, loglevel="DEBUG")


if __name__ == "__main__":

    easel.run(host="0.0.0.0", port=8000)
