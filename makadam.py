import os

import click
import cv2
import easyocr
import numpy as np
from openpyxl import Workbook, load_workbook
from tqdm import tqdm

TOP_LEFT_DATA_CORNER = (675, 50)  # x,y
BOTTOM_RIGHT_DATA_CORNER = (945, 670)  # x,y
DEFAULT_WB_NAME = "default_workbook.xlsx"


def image_preprocessing(image, tl_corner=None, br_corner=None):
    """Crop an image and apply a black and white mask

    Parameters
    ----------
    image : numpy array
        Image with 3 channels (BGR).
    tl_corner : Tuple
        Coordinates (x,y) of the top left corner of the rectangle to crop
    br_corner : Tuple
        Coordinates (x,y) of the bottom right corner of the rectangle to crop

    Returns
    -------
    numpy array
        binary image ready to be read by OCR
    """
    # Crop with slicing
    if tl_corner and br_corner:
        image = image[tl_corner[1] : br_corner[1], tl_corner[0] : br_corner[0]]

    # Convert to HSV channels
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # define lower and upper bounds of the filter
    lower = np.array([0, 0, 210])
    upper = np.array([255, 255, 255])
    # return the mask
    return cv2.inRange(hsv, lower, upper)


def apply_overlay(image, OCR_results):
    """Apply an overlay on the image with bounding boxes
    and the text recognized, along with the confidence level

    Parameters
    ----------
    image : numpy array
        image on which the overlay will be aplied (for better results, use BGR image)
    OCR_results : list[list]
        Detailed results given by the easyocr.Reader.readtext() function

    Returns
    -------
    numpy array
        image with the overlay of boxes and text recognized
    """
    image_with_overlay = image.copy()
    # loop over the results
    for (bbox, text, prob) in OCR_results:
        # display the OCR'd text and associated probability
        # print("[INFO] {:.4f}: {}".format(prob, text))

        # unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        # draw the box surrounding the text along
        # with the OCR'd text itself and the probability
        cv2.rectangle(image_with_overlay, tl, br, (0, 255, 0), 2)
        cv2.putText(
            image_with_overlay,
            text + " " + str(round(prob, 2)),
            (br[0] + 5, br[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )
    return image_with_overlay


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
def main(img_dir, players, workbook, save_copy):
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

    # TODO : read the data already present in the notebook
    # TODO : append the new data to the correct place (existing columns that match with the player)
    ws = wb.active
    # TODO : add --header flag
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
