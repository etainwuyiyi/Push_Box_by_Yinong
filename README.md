# Push_Box_by_Yinong

> **Team members**: Yinong Zhao

This file is used to find the solutions for the **Sokoban** game. **Sokoban** is another term as "push box". This file aim to find solution for every level.

**Package Install**

sympy package must be installed to make sure that code would work.
```
pip install pillow
```

**This repository contains:**

1. [box_3.py](box_3.py) to read in the configuration by accessing the .data file. Find Solution. Display solution in a sery of images. When going through the solution images, pretend it's a video, then you understand the solution.
2. [README.md](README.md) to give introductions to this file.
3. [unit_test_1.data](unit_test_1.data) is one config file for testing the code. Same as for unit_test_2.data, unit_test_3.data.
4. There is a example solution displayed in the zip file.

## Compatability
TeamLasor project works with python 3 under both Windows and Mac systems. Click [here](https://www.python.org/downloads/) to download the newst version of python.

****

## Appendix

### box_3.py

To use **box_3.py**, use the code via loading the desired config file.
```
game_readin = load_unit_test("unit_test_2.data")

```
