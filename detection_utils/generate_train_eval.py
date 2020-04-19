import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import ntpath
import random


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Separates a CSV file into training and validation sets',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'input_csv',
        metavar='input_csv',
        type=str,
        help='Path to the input CSV file')
    parser.add_argument(
        '-f',
        metavar='train_frac',
        type=float,
        default=.75,
        help=
        'fraction of the dataset that will be separated for training (default .75)'
    )
    parser.add_argument(
        '-s',
        metavar='stratify',
        type=bool,
        default=True,
        help='Stratify by class instead of whole dataset (default True)')
    parser.add_argument(
        '-o',
        metavar='output_dir',
        type=str,
        default=None,
        help=
        'Directory to output train and evaluation datasets (default input_csv directory)'
    )

    parser.add_argument(
        '-v',
        metavar='valid_str',
        type=str,
        default=None,
        help=
        'Validate example prefix string'
    )

    parser.add_argument(
        '-cheat',
        metavar='if_cheat',
        type=bool,
        default=True,
        help=
        'add validation data to train'
    )

    args = parser.parse_args()

    if args.f < 0 or args.f > 1:
        raise ValueError('train_frac must be between 0 and 1')

    # output_dir = input_csv directory is None
    if args.o is None:
        output_dir, _ = os.path.split(args.input_csv)
    else:
        output_dir = args.o

    df = pd.read_csv(args.input_csv)

    if args.v:
        if args.cheat:
            train_df = df
        else:
            train_df = df.loc[~df['filename'].str.startswith(args.v), :]
        train_df = train_df.sample(frac=1)
        validation_df = df.loc[df['filename'].str.startswith(args.v), :]
        validation_df = validation_df.sample(frac=1)
    else:
        examples_list = list(df['filename'].unique())
        random.seed(42)
        random.shuffle(examples_list)
        num_examples = len(examples_list)
        num_train = int(args.f * num_examples)
        train_examples = examples_list[:num_train]
        val_examples = examples_list[num_train:]

        train_df = df.loc[df['filename'].isin(train_examples), :]
        validation_df = df.loc[df['filename'].isin(val_examples), :]
    # output files have the same name of the input file, with some extra stuff appended
    csv_file = path_leaf(args.input_csv)
    new_csv_name = os.path.splitext(csv_file)[0]
    train_csv_path = os.path.join(output_dir, new_csv_name + '_train.csv')
    eval_csv_path = os.path.join(output_dir, new_csv_name + '_eval.csv')

    train_df.to_csv(train_csv_path, index=False)
    validation_df.to_csv(eval_csv_path, index=False)
