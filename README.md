# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/institutohumai/pyeph/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                             |    Stmts |     Miss |   Cover |   Missing |
|--------------------------------- | -------: | -------: | ------: | --------: |
| pyeph/\_\_init\_\_.py            |        5 |        0 |    100% |           |
| pyeph/ads.py                     |        4 |        0 |    100% |           |
| pyeph/calc/\_\_init\_\_.py       |        4 |        0 |    100% |           |
| pyeph/calc/\_base\_calculator.py |       46 |       26 |     43% |18-26, 30-32, 42, 46-57, 61-63 |
| pyeph/calc/\_template.py         |        8 |        8 |      0% |      1-28 |
| pyeph/calc/\_types.py            |       15 |        8 |     47% |6, 9-11, 16, 19-21 |
| pyeph/calc/dwelling.py           |       62 |        7 |     89% |49, 53, 56, 78, 80, 84, 87 |
| pyeph/calc/labor\_market.py      |       68 |       37 |     46% |27, 31-33, 36-42, 45-50, 53-57, 64-71, 77-82, 88-92 |
| pyeph/calc/poverty.py            |      103 |       60 |     42% |53-69, 73-79, 83-95, 99-117, 123-133, 138-149 |
| pyeph/config.py                  |        3 |        0 |    100% |           |
| pyeph/errors.py                  |        7 |        0 |    100% |           |
| pyeph/get/\_\_init\_\_.py        |       14 |        0 |    100% |           |
| pyeph/get/\_base\_getter.py      |       80 |       10 |     88% |53, 94-96, 127-132 |
| pyeph/get/basket.py              |       60 |        7 |     88% | 69, 77-82 |
| pyeph/get/equivalent\_adult.py   |        4 |        0 |    100% |           |
| pyeph/get/mautic.py              |       43 |        1 |     98% |        16 |
| pyeph/get/microdata.py           |       81 |        6 |     93% |32, 47, 62, 72, 96, 102 |
| pyeph/tools/\_\_init\_\_.py      |        2 |        0 |    100% |           |
| pyeph/tools/decorators.py        |       24 |       10 |     58% |6, 13-16, 21-28 |
| pyeph/tools/labels.py            |       39 |       29 |     26% |11-17, 20-22, 26-53 |
| pyeph/tools/merge.py             |       21 |       16 |     24% |      8-35 |
| **TOTAL**                        |  **693** |  **225** | **68%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/institutohumai/pyeph/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/institutohumai/pyeph/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/institutohumai/pyeph/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/institutohumai/pyeph/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Finstitutohumai%2Fpyeph%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/institutohumai/pyeph/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.