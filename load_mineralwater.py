import sys, os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "minwater_review.settings")

import django

django.setup()

from reviews.models import Mineral_Water


def save_mineralwater_from_row(mineralwater_row):
    mineralwater = Mineral_Water()
    mineralwater.id = mineralwater_row[0]
    mineralwater.name = mineralwater_row[1]
    mineralwater.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        mineralwater_df = pd.read_csv(sys.argv[1])
        print(mineralwater_df)

        mineralwater_df.apply(
            save_mineralwater_from_row,
            axis=1
        )

        print("There are {} mineral water".format(Mineral_Water.objects.count()))

    else:
        print("Please, provide Mineral Water file path")
