# DevOps Project Team 1

## Commit Message Style

### Format

\<type\>(optional scope of changes): brief description of changes

Example 1: `feat(playerController): Add movement to player`

Example 2: `docs: Update README to show virtual environment commands`

### Commit Types

| Commit Type | Title                    | Description                                                                                    | Emoji |
| ----------- | ------------------------ | ---------------------------------------------------------------------------------------------- | ----- |
| feat        | Features                 | A new feature                                                                                  | ✨    |
| fix         | Bug Fixes                | A bug fix                                                                                      | 🐛    |
| docs        | Documentation            | Documentation only changes                                                                     | 📚    |
| style       | Styles                   | Changes that do not affect the meaning of the code (e.g. white-space, formatting, semi-colons) | 💎    |
| refactor    | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                      | 📦    |
| perf        | Performance Improvements | A code change that improves performance                                                        | 🚀    |
| test        | Tests                    | Adding missing tests or correcting existing tests                                              | 🚨    |
| ci          | Continuous Integrations  | Changes to our CI configuration files and scripts                                              | ⚙️    |
| chore       | Chores                   | Changes to the build or auxiliary tools and libraries such as documentation generation         | ♻️    |

## Setting Up Project

### Create Virtual Environment

To create a virtual environment locally, within the project folder, type

```sh
python -m venv dev_env
```

Make sure that the venv follows the same name so git ignores the venv folder.

### Virtual Environment Commands

```sh
# Entering virtual environment
.\dev_env\Scripts\activate

# Installing dependencies from requirements.txt
python -m pip install -r requirements.txt

# Exit virutal environment
deactivate
```

### Installing New Dependencies

Whenever a new dependency is required for the project, the requirements.txt file has to be updated. To do this, simply type:

```sh
python -m pip freeze > requirements.txt
```

## Team

### Scrum Master

- Lim Dong Kiat

### Developers

- Danny Chan Yu Tian
- Lee Quan Sheng

### Quality Assurance

- Caleb Goh En Yu
- Swee Kah Ho
