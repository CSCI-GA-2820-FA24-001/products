# NYU DevOps Products

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/VectorZYJ/products/actions/workflows/workflow.yml/badge.svg)](https://github.com/VectorZYJ/products/actions)

This is the development and utilization documentation for `products` squad. The products service represents the store items that the customer can buy. They have a unique product id, a name, description, price, and an imageURL for display.

Team Members:\
Shilong Dong, Yujia Zhu, Weilin Chen, Tiancheng Zhang, Arya Goyal

## Overview

This project inherits basic code structure from [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd).

- The `/service` folder contains our `models.py` file for our model and a `routes.py` file for our service.
- The `/tests` folder has test case code for testing the model and the service separately.

## Project Setup

You need to clone this repo to your local dir and enter the project's directory. Then open it in VSCode, and make sure reopen it in Docker Container.

```bash
git clone https://github.com/CSCI-GA-2820-FA24-001/products.git
cd products
code .
```

## Usage

### REST APIs

We provide basic CRUD operations for the product service.

- Create a Product: `POST` `/products` 
- Read a Product: `GET` `/products/<product_id>`
- Update a Product: `PUT` `/products/<product_id>`
- Delete a Product: `DELETE` `/products/<product_id>`
- List all Products (Base URL): `GET` `/products`

When using List service, we can also specify `name` or `price` for fuzzy query, such as `GET /products?name=iPhone` and `GET /products?price=1088`. First request returns products whose name contains iPhone, and the second request returns those with price around 1088.
  
### Test

We follow the TDD manner during our development. If you want to test the project, you can follow the following commands.

```bash
cd products
make test
```

Our test report is as follows:

```bash
---------- coverage: platform linux, python 3.11.10-final-0 ----------
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
service/__init__.py                   22      2    91%   50-51
service/common/cli_commands.py         7      0   100%
service/common/error_handlers.py      32      3    91%   91-93
service/common/log_handlers.py        10      1    90%   35
service/common/status.py              45      0   100%
service/config.py                      7      0   100%
service/models.py                     71      0   100%
service/routes.py                     84      2    98%   217-218
----------------------------------------------------------------
TOTAL                                278      8    97%

Required test coverage of 95% reached. Total coverage: 97.12%
=================== 34 passed in 1.23s ===================
```

### Run

You can start the service using the following commands.

```bash
cd products
make run
```

Then you are able to visit the homepage from `http://localhost:8080/` or `http://0.0.0.0:8080/`, and utilize our services with prompts on the homepage.

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```
## 



## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
