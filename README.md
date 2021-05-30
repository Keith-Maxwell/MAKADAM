<!-- ![MAKADAM](<https://socialify.git.ci/Keith-Maxwell/MAKADAM/image?description=1&descriptionEditable=MarioKartDataMiner%20(MAKADAM)%20uses%20Optical%20Character%20Recognition%20to%20get%20data%20from%20Mario%20Kart%20screenshots&font=Inter&issues=1&language=1&logo=https%3A%2F%2F1.bp.blogspot.com%2F-GZl7vDxEWIM%2FWUaVEfHpx_I%2FAAAAAAABM-c%2FIgHT-DryPLoouFVIaqNI3ZZgjrBZy0UcQCLcBGAs%2Fs1600%2F600px-MK8_Deluxe_Art_-_Mario_%252528transparent%252529.png&owner=1&pattern=Charlie%20Brown&pulls=1&stargazers=1&theme=Dark>) -->

![MAKDAM_gif](MAKADAM.gif)

# What is MAKADAM ?

MAKADAM stands for **MA**rio **KA**rt **DA**ta **M**iner. This CLI program allows you to track your progress in _Mario Kart 8 Deluxe_ on Nintendo Switch. It reads the rankings of each player on the end-game screen, and writes the results in an Excel file.

In the current version, MAKADAM works by analysing screenshots of the game results. In future versions, MAKADAM will be able to analyse real time video from the game.

# How to use ?

## Collect screenshots from your games

In _Mario Kart 8 Deluxe_, at the end of the race, you are presented with a screen like the following :

![results](<img\Samples\sample(1).jpg>)

You must take a screenshot using the little square button on your Switch controller.

At the end of your gaming session, plug your Switch to your computer using an USB-C cable and go to the console `settings > data > manage screenshots and videos > copy to a computer via USB`.

On your computer, navigate to the Mario Kart directory and copy the files wherever you want on your computer. Be sure to put them in a directory.

## Run the code to fill an Excel file

First, install the software by following the instructions in the section [installation](#installation)

Use the command `makadam` followed by the arguments and options.
The detailed list of arguments is shown with :

```
makadam --help
```

For basic usage, type

```
makadam path/to/img/folder player_name1 ...
```

You must enter a path to a folder and at least one player name. The other parameters are optional.

The code will scan the folder for the `.jpg` images and apply an OCR (Optical Character Recognition) algorithm to guess the player names. The order of the player names gives the position in the race.

The code saves the positions of the provided `PLAYERS`, so be sure to use the same name as the one in-game. You can track multiple players at once.

The positions will be written in the Excel file given with the option `--workbook`. If the file exists, results are appended at the end. If it doesn't, then the file will be created. You can save the results in a copy of the input workbook with the flag `--save-copy`. A default workbook will be created if the parameter is left blank

## Example

In this current directory :

```
makadam ./img/Samples Makss Marie PH alice Player --workbook new_workbook.xlsx
```

This command will read through the images stored in the `./img/Samples` directory of this repo, and search for the positions of the players `Makss`, `Marie`, `PH`, `alice` and `Player`. Their positions will then be written to a new excel file called `new_workbook.xlsx` and will look like this :

| Makss | Marie | PH  | alice | Player |
| :---: | :---: | :-: | :---: | :----: |
|   1   |   8   |  7  |   5   |   3    |
|   2   |   5   |  7  |   1   |   3    |
|   1   |   9   |  3  |   4   |   5    |
|   2   |   8   |  5  |   4   |   3    |
|   3   |   9   |  5  |   6   |   1    |
|   1   |   4   |  8  |   2   |   9    |
|   1   |   4   |  3  |   5   |   8    |
|   1   |   2   |  8  |   6   |   3    |
|   3   |   5   |  8  |   6   |   1    |
|   1   |   8   |  9  |   2   |   3    |

# Installation

This code is not yet published on Pypi, so you'll have to clone the repo. Wherever you want, open a terminal and run

```
git clone https://github.com/Keith-Maxwell/MAKADAM.git
```

It is strongly advised to create a virtual environment

```
python -m venv venv_name
```

Then, activate it.

- on windows : `.\venv_name\Scripts\activate`
- on Linux/MacOs : `source venv_name/bin/activate`

Once activated, you can install mariokart2excel inside by running the command :

```
pip install .
```

This will also install all the dependencies, mainly the following:

- easyOCR
- opencv-python
- openpyxl
- click
- tqdm
