from src.easel import Easel

# easel = Easel("examples/template", loglevel="DEBUG")
# easel = Easel("examples/sargent", loglevel="DEBUG")
easel = Easel("examples/sargent")


if __name__ == "__main__":

    easel.run(debug=True, host="0.0.0.0")
