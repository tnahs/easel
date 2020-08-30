from src.easel import Easel


easel = Easel("examples/sargent-demo", loglevel="DEBUG")
# easel = Easel("examples/sorolla-demo", loglevel="DEBUG")


if __name__ == "__main__":

    easel.run(debug=True, host="0.0.0.0")
