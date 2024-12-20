[![PyPI version](https://img.shields.io/pypi/v/cognitoctl.svg?style=plastic)](https://pypi.org/project/cognitoctl/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/cognitoctl?style=plastic)


# cognitoctl

A command-line tool for interacting with AWS Cognito, designed to simplify user, group, and authentication management.  

## Table of Contents

1. [Description](#description)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
    - [Available Commands](#available-commands)
6. [Contributing](#contributing)

---

## Description

This CLI enables easy management of **users and groups in AWS Cognito**. Features include:  
- Group creation and management.
- User registration, authentication, and management.
- Password recovery and token updates.

It’s designed for developers needing quick integration with AWS Cognito from the command line.  

## Requirements

Before using this CLI, ensure the following prerequisites are met:

- **Python 3.10+**
- **AWS CLI configured** with the necessary credentials to access Cognito.
- Sufficient AWS permissions to manage Cognito.

## Installation

1. Install package:
```bash
   pip install cognitoctl
```

## Getting Started

### Initialize the CLI
To use the CLI, you must initialize it with at least one **Cognito project**. Use the init command to set up a project. You can either input configuration details interactively or provide them via a configuration file.  
You can use the --help option to get help on parameters and commands.

#### Interactive Mode:
```bash
   cognitoctl init
```

You will be prompted to enter the necessary configuration values such as:

- Project Name (e.g., "development", "production").
- AWS Access Key ID
- AWS Secret Access Key
- Cognito User Pool ID.
- Cognito App Client ID
- Cognito Client Secret
- Need use Secret Hash (Y/N)


#### Configuration File:  
Alternatively, you can provide the details through a TOML file:
```bash
   cognitoctl init -f config.toml
```

Example of config.toml:

```
[project1]
key_id = "your-aws-access-key-id"
access_key = "your-aws-secret-access-key"
userpool_id = "your-userpool-id"
app_client_id = "your-client-id"
app_client_secret = "your-client-secret"
secret_hash = true
```


### Managing Multiple Projects
The CLI allows you to manage multiple Cognito environments as separate projects. Each project is stored in the CLI's configuration, and you can switch between them as needed.

#### Add a New Project
To add another project, simply run init again with a different name:
```bash
   cognitoctl init -f proyect2.toml
```

#### Select project
You can select project using:

```bash
   cognitoctl config select project1
```

## Usage
| Command                     | Description                                      | Actions                                                              |
|-----------------------------|--------------------------------------------------|----------------------------------------------------------------------|
| `init`                      | Initializes the CLI with required configuration. |                                                                      |
| `config`                    | Apply CLI configuration level actions.           | list, current, set, get, select, edit                                |
| `group`                     | Apply group level actions.                       | create, delete, delete-user, add-user, list, get, edit               |
| `user`                      | Apply user level actions.                        | create, confirm, delete, change-password, enable, disable, get, list |

## Contributing
Contributions are welcome! To improve this tool, follow these steps:  
Fork the repository.  

Create a new branch:
```bash
git checkout -b feature/new-feature
```

Submit a Pull Request to the main repository, in the branch dev.

