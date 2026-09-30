# Langchain Project

## Overview

Langchain is a framework designed to facilitate the orchestration of chains,
agents, prompts, and tools for various applications. It provides a structured
approach to managing workflows and decision-making processes, making it easier
to build complex systems.

### Graph diagram(WIP)

``` mermaid
flowchart TD
    A[START] --> B{Orchestrator<br/>queries generator<br>search selector}
    B --> D[Gogle search]
    B --> E[Vetric FB search]
    B --> F[Vetric IG search]
    B --> H[Vetric LI search]
    D --> I(Synthesizer<br/>Candidates to DB)
    E --> I
    F --> I
    H --> I
    I --> J{Matcher}
    J -->|no match,<br/>change criteria| B
    J -->|match| K(Enrich WIP)
```

## Installation

### As standalone app without docker

To get started with Langchain, follow these steps:

1. Clone the repository:

   ```shell
   git clone <repository-url>
   cd repo-name/langsearch
   ```

2. Create a virtual environment:
   with default installed version

   ```shell
   python -m venv venv
   ```

   or with specified version(should installed as system wide)

   ```shell
   python3.12 -m venv venv
   ```

3. Activate a virtual environment

   ```shell
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required packages:

   ```shell
   pip install -r requirements-dev.txt
   ```

### As docker container

application require imports from core library and require to build outside 
of own catalog

1. Clone the repository:

   ```shell
   git clone <repository-url>
   cd repo-name
   ```

2. Build image

   ```shell
   docker build -t signaight/langsearch -f ./langsearch/Dockerfile .
   ```

WIP

## Usage

### Run as standalone app

To run the Langchain application as cli, execute the following command:

  ```shell
  PYTHONPATH=$PYTHONPATH:./langsearch:../ taskiq worker langsearch.app:broker --reload
  ```

**NOTE:** Command line option `--reload` should be used only in dev environment

To interact with application through broker. 

  ```shell
  PYTHONPATH=$PYTHONPATH:./langsearch:../ python langsearch/cli.py search
  ```

To interact with application without broker. Broker should configured anyway but there default redis could used.

  ```shell
  PYTHONPATH=$PYTHONPATH:./langsearch:../ python langsearch/cli.py search {UUID} --no-broker
  ```

**NOTE:"" Use ` --help` to get  info about possible options for run

Example:

  ```shell
  PYTHONPATH=$PYTHONPATH:./langsearch:../ python langsearch/cli.py search --f-name Ada --l-name Lovelace --email-address "ada@example.com" --no-broker
  ```

**NOTE:** If values contain whitespaces or special symbols please encapsulate them with doublequotes same at in example

### Run as docker container

Production run

  ```shell
  docker run -p 8000:8000 signaight/langsearch
  ```
  
Development run with changes wathdog --env-file

  ```shell
  docker run -p 8000:8000 signaight/langsearch taskiq worker langsearch.app:broker --reload
  ```

Run cli task for search in docker container

  ```shell
  python langsearch/cli.py search --f-name Ada --l-name Lovelace --email-address "ada@example.com"
  ```
