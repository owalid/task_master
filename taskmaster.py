import argparse as ap
from argparse import RawTextHelpFormatter
from parsing_conf import parse_conf_file

if __name__ == "__main__":
    parser = ap.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-c", "--conf", required=True, type=str, help='Path of your configuration file')
    args = parser.parse_args()

    # Load configuration file
    conf_path = args.conf
    print(conf_path)
    parse_conf_file(conf_path)
