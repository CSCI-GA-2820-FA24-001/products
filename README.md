# NYU DevOps Products

[![Build Status](https://github.com/CSCI-GA-2820-FA24-001/products/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA24-001/products/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-FA24-001/products/graph/badge.svg?token=JCE8OGIJZY)](https://codecov.io/gh/CSCI-GA-2820-FA24-001/products)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

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

We provide basic CRUD, List, Query and Purchase operations for our product service.

| Operation | Method | Endpoint |
| :-------: | :----: | :------: |
| Create a product | `POST` | `/products` |
| Read a product | `GET` | `/products/<product_id>` |
| Update a product | `PUT` | `/products/<product_id>` |
| Delete a product | `DELETE` | `/products/<product_id>` |
| List all products | `GET` | `/products` |
| Query products by name | `GET` | `/products?name=<product_name>` |
| Query products by price | `GET` | `/products?price=<product_price>` |
| Purchase a product | `PUT` | `/products/<product_id>/purchase` |

When using Query service, we can specify `name` or `price` for fuzzy query, such as `GET /products?name=iPhone` and `GET /products?price=1088`. First request returns products whose name contains iPhone, and the second request returns those with price around 1088.
  
### Test

We follow the TDD manner during our development. If you want to test the project, you can follow the following commands.

```bash
flask db-create
make test
make lint
```

Our test report is as follows:

```bash
---------- coverage: platform linux, python 3.11.10-final-0 ----------
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
service/__init__.py                   22      2    91%   50-51
service/common/cli_commands.py        12      0   100%
service/common/error_handlers.py      32      3    91%   91-93
service/common/log_handlers.py        10      1    90%   35
service/common/status.py              45      0   100%
service/config.py                      7      0   100%
service/models.py                     93      0   100%
service/routes.py                     96      0   100%
----------------------------------------------------------------
TOTAL                                317      6    98%

Required test coverage of 95% reached. Total coverage: 98.11%

===================================================== 59 passed in 1.86s ===
```

### Run

You can start the service using the following commands.

```bash
make run
```

Then you are able to visit the homepage from `http://localhost:8080/` or `http://0.0.0.0:8080/`, and utilize our services with prompts on the homepage.

### Deployment

Deployment of our `products` service can be done in following steps:

1. Create dev cluster

```shell
make cluster
```

2. Build this project as a Docker image

```shell
docker build -t products:latest .
```

3. Configure registry
   
Check if `cluster-registry` is configured in `/etc/hosts`:

```shell
cat /etc/hosts
```

If there is no entry for `cluster-registry`, add it by running:

```shell
sudo bash -c "echo '127.0.0.1    cluster-registry' >> /etc/hosts"
```

4. Create tag and push our image to K3d registry

```shell
docker tag products:latest cluster-registry:5000/products:latest
docker push cluster-registry:5000/products:latest
```

5. Create and switch to a new Kubernetes Namespace

```shell
kubectl create namespace deployment
kubectl config set-context --current --namespace deployment
```

6. Deploy our image with postgresql and products service

```shell
kubectl apply -f k8s/postgresql/
kubectl apply -f k8s
```

wait for approximately 20 seconds until all services are running, using following command to track status

```shell
kubectl get all
```

7. View logs from a service

```shell
kubectl get pods
kubectl logs pod/<pod-name>
```

Now we can access `http://localhost:8080` for our `product` service that is deployed on local cluster

8. Remove all services from the namespace and remove cluster

```shell
kubectl delete -f k8s -R
make cluster-rm
```

### Deployment on Red Hat OpenShift

Login command within shell

(See slides)

Switch to project namespace

```shell
oc project vectorzyj-dev
```

Deploy PostgreSQL Database

```shell
oc apply -f k8s/postgresql/
```

Add Event Listener

```shell
oc apply -f .tekton/events/
```

Then click on `Trigger -> Deployment -> el-cd-listener`, in deployment details, set scaling to `1 pod`.
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
