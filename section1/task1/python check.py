import argparse
import pandas as pd


def check_integrity(args):

    d = pd.read_csv(args.yourdata)
    s = pd.read_csv(args.sample)

    col = d.columns == s.columns

    search = pd.DataFrame.duplicated(d)
    d = pd.DataFrame.drop_duplicates(d, ignore_index=True)

    print('remove ' + str(len(search[search])) + ' duplicates')

    merge = diff(d, s)

    if col.all() and len(d.index) == len(s.index):
        if diff(d, s).empty:
            print('your data is successfully integrited!')
        else:
            print(merge)

    elif col.all() and len(d.index) != len(s.index):
        print('index does not match!')
        print('your data index length: ' + str(len(d.index)))
        print('sample index length: ' + str(len(s.index)))
        print(merge)

    elif col.all() == False and len(d.index) == len(s.index):
        print('columns does not match!')
        print('your columns: ')
        print(d.columns)
        print('sample columns: ')
        print(s.columns)
        print(merge)

    else:
        print('both index and columns do not match!')
        print('index does not match!')
        print('your data index length: ' + str(len(d.index)))
        print('sample index length: ' + str(len(s.index)))
        print('columns does not match!')
        print('your columns: ')
        print(d.columns)
        print('sample columns: ')
        print(s.columns)
        print(merge)



def diff(f1, f2):
    merge = f2.merge(f1, indicator=True,
                     how='outer').loc[lambda x: x['_merge'] != 'both']
    return merge


def main():
    parser = argparse.ArgumentParser(
        prog='Check csv differences',
        description='check your hourly data with sample file')
    parser.add_argument(
        '-s',
        dest='sample',
        required=True,
        help='Input sample data, _merge shows left_only if sample data has rows that are not in your data',
        type=argparse.FileType('r'))
    parser.add_argument(
        '-d',
        dest='yourdata',
        required=True,
        help='Input your data, _merge shows right_only if your data has rows that are not in sample data',
        type=argparse.FileType('r'))
    parser.set_defaults(func=check_integrity)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
