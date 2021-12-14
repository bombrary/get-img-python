from . import download_imgs_from_page
import argparse

parser = argparse.ArgumentParser(prog="commandline")
parser.add_argument('url', type=str)
parser.add_argument('path', type=str)
parser.add_argument('-v', nargs='?', default=False, const=True, help="print log verbosely")
parser.add_argument('-s', type=str, help="CSS selector")

args = parser.parse_args()

failInfo = download_imgs_from_page(args.url, args.path, args.s, args.v)
for info in failInfo:
    print(info[0], info[1])
