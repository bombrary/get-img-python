from viewer import app
import argparse

parser = argparse.ArgumentParser(prog="viewer")
parser.add_argument('-p', type=str, default="8000")

args = parser.parse_args()

app.config['ENV'] = 'development'
app.run(debug=True, port=args.p)
