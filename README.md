# cognitoctl

A command-line tool for interacting with AWS Cognito, designed to simplify user, group, and authentication management.

## Table of Contents

1. [Description](#description)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
    - [Available Commands](#available-commands)
5. [Configuration](#configuration)
6. [Contributing](#contributing)
7. [License](#license)

---

## Description

This CLI enables easy management of **users and groups in AWS Cognito**. Features include:
- Group creation and management.
- User registration, authentication, and management.
- Password recovery and token updates.
- Deleting users and more.

It’s designed for developers needing quick integration with AWS Cognito from the command line.

## Requirements

Before using this CLI, ensure the following prerequisites are met:

- **Python 3.7+**
- **AWS CLI configured** with the necessary credentials to access Cognito.
- Installed `boto3` library.
- Sufficient AWS permissions to manage Cognito.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/cognito-cli.git
   cd cognito-cli
