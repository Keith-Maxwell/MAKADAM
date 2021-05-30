# Dataset creation

The goal is to create a dataset of labelled images representing the positions. This dataset can be used to train a classification ML model that will recognize the current position on screen.

## Data collection

I captured a lot of sample videos from the game and isolated small parts for each of the 12 positions. I ended up with dozens of small video clips (a few seconds each) where i keep a constant position in the race. I did this on many different circuits in order to have a large variety of backgrounds.

Each video clip is stored inside a directory corrsponding to the position in the race. For example :

```
ML_dataset
├── 1
│   ├── sample1.mp4
│   └── sample2.mp4
├── 2
│   ├── sample1.mp4
│   └── sample2.mp4
:
└── 12
    └── sample.mp4
```

This allows to easily label the data

## Automated dataset creation

The python script `create_ML_dataset.py` iterates trough each position directory and reads the video samples frame by frame. It crops the position and saves the image in the directory corresponding to the position, thus labelling the data. The image and label are also saved in numpy arrays that are then exported as `dataset.npy` and `labels.npy`.

These `.npy` files can easily be imported to train a ML model.
