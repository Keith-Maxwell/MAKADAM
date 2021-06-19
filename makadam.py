import os

import click
import cv2
import easyocr
import numpy as np
from openpyxl import Workbook, load_workbook
from tqdm import tqdm

from utils import apply_overlay, image_preprocessing

TOP_LEFT_DATA_CORNER = (675, 50)  # x,y
BOTTOM_RIGHT_DATA_CORNER = (945, 670)  # x,y
DEFAULT_WB_NAME = "default_workbook.xlsx"


@click.command()
@click.argument("img-dir", type=click.Path(exists=True))
@click.argument("players", nargs=-1, required=True)
@click.option(
    "-w",
    "--workbook",
    default=DEFAULT_WB_NAME,
    show_default=True,
    type=click.Path(),
    help="Path to the workbook to fill. If it does not exist, it will be created. Must include the extension",
)
@click.option(
    "--save-copy/--no-save-copy",
    default=False,
    show_default=True,
    help="Save the new workbook as a copy or overwrite the old one",
)
@click.option(
    "--header/--no-header",
    default=True,
    show_default=True,
    help="Add a header row with the player names",
)
def main(img_dir, players, workbook, save_copy, header):
    """Read the finish grid from MarioKart screenshots and fill an Excel workbook with the results

    IMG-DIR is the path to the directory where your screenshots are saved

    PLAYERS is the names of the players to write in the Excel workbook, separated by spaces
    """

    # --------- Load the Workbook or create a new one -----------
    try:
        wb = load_workbook(workbook)
    except FileNotFoundError:
        wb = Workbook()
        click.echo(f"[INFO] The file named '{workbook}' has not been found, so it will be created")

    # TODO : read the data already present in the workbook
    # TODO : append the new data to the correct place (existing columns that match with the player)
    ws = wb.active
    if header:
        ws.append(players)  # Add headers

    # --------- Verify the validity of img_dir ----------
    try:
        img_list = os.listdir(img_dir)
    except NotADirectoryError:
        click.echo()
        raise click.BadParameter(message=f"'{img_dir}' is not a directory.")

    # --------- Create the OCR reader ----------
    reader = easyocr.Reader(["fr"])

    # -------- Iterate over all files in img_dir ---------
    for img_name in tqdm(img_list):
        if img_name.endswith(".jpg"):
            img = cv2.imread(os.path.join(img_dir, img_name), -1)
        else:  # If file is not an image, skip the iteration
            continue

        # ------- Preprocess and read the image ---------
        img = image_preprocessing(img, TOP_LEFT_DATA_CORNER, BOTTOM_RIGHT_DATA_CORNER)
        results = reader.readtext(
            img,
            allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            detail=1,
        )
        finish_grid = [item[1] for item in results]

        # ------- for Each player wanted by the user, assign a position -------
        positions = []
        for player in players:
            try:
                positions.append(finish_grid.index(player) + 1)
            except ValueError:  # happens when the OCR did not succeed
                click.echo(
                    f"\n\n[WARN] Player '{player}' was not found in the finish grid :( The image I had trouble with is {os.path.abspath(img_name)}\n"
                )
                positions.append("NA")
        # add the positions to a new row in the worksheet
        ws.append(positions)

    # ------- Save the workbook ---------
    if save_copy:
        wb.save(workbook[:-5] + "_copy.xlsx")
    else:
        wb.save(workbook)


if __name__ == "__main__":
    main()
