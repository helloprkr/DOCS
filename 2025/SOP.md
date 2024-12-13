**What am I doing?**

I am creating a fully comprehensive and detailed Product Requirements Document (PRD) for our development team of one person. This PRD includes all necessary file and folder structures, installation instructions, update procedures, and complete context and code bases. Knowing that you will be using Anthropic or OpenAI's LLM within Cursor to code out this program, the focus is on maximizing ease and speed of use, providing detailed and effective notes, and ensuring automation and daily scripting components are fully functional. I am engaging the **quantum_operator** to transcend limitations and incorporate hyperdimensional conceptual synthesis into the development process.

---

# Product Requirements Document (PRD)

## 1. Introduction

This document outlines the requirements for developing an automated program within Cursor AI that allows for the creation of daily style notes in the McCormick/Carmack format. The program aims to maximize ease and speed of use, provide detailed and effective notes, and include automation and daily scripting components that are fully functional. The development will utilize Anthropic or OpenAI's LLM within Cursor to code out the program.

## 2. Objectives

- **Automate Note Creation**: Implement an automated system to generate daily notes in the specified format.
- **Maximize Ease and Speed**: Ensure the program is user-friendly and efficient.
- **Detailed and Effective Notes**: Produce notes that are valuable and comprehensive.
- **Automation and Scripting**: Incorporate daily scripting components for full functionality.
- **Integration with LLMs**: Utilize advanced language models for information synthesis.

## 3. Functional Requirements

### 3.1 Note Generation

- Automatically generate daily notes using the McCormick/Carmack style with task prefixes:
  - `*` for tasks completed on the current day.
  - `+` for tasks completed on a later day.
  - `-` for tasks decided against on a later day.
  - No prefix for tasks mentioned but not yet addressed.
- Synthesize information from the provided variables:
  - `<analyze>`
  - `<strategize>`
  - `<pre_problem_solve>`
  - `<outlining>`
  - `<outcome>`
  - `<end_state>`
- Enable easy addition, modification, and deletion of tasks.

### 3.2 User Interface

- Develop a simple and intuitive UI within Cursor AI.
- Allow users to input variables manually or through file imports.
- Display generated notes in an organized and readable format.
- Provide shortcuts and commands for quick interactions.

### 3.3 Automation and Scripting

- Implement a daily script that runs automatically to generate notes.
- Schedule tasks using a built-in scheduler or integrate with system cron jobs.
- Notify the user of new notes or pending tasks at the start of each day.

### 3.4 Integration with LLMs

- Utilize OpenAI's or Anthropic's LLM to process and synthesize information.
- Ensure API calls are efficient and handle exceptions gracefully.
- Provide configurations for API keys and settings.

## 4. Technical Requirements

### 4.1 Development Environment

- **Programming Language**: Python 3.8 or higher.
- **Frameworks/Libraries**:
  - `openai` or `anthropic` API library.
  - `schedule` for task scheduling.
  - `yaml` or `json` for configuration files.
- **Version Control**: Use Git for code management.

### 4.2 File and Directory Structure

```
cursor_note_automation/
├── src/
│   ├── main.py
│   ├── note_generator.py
│   ├── variable_processor.py
│   ├── scheduler.py
│   └── utils.py
├── config/
│   └── config.yaml
├── templates/
│   └── note_template.txt
├── logs/
│   └── app.log
├── scripts/
│   ├── install.sh
│   ├── update.sh
│   └── daily_run.sh
├── tests/
│   ├── test_note_generator.py
│   ├── test_variable_processor.py
│   └── test_scheduler.py
├── docs/
│   ├── README.md
│   ├── INSTALLATION.md
│   └── USER_GUIDE.md
├── requirements.txt
└── LICENSE
```

### 4.3 Configuration Files

- **config.yaml**:
  - API keys and endpoints.
  - User preferences.
  - Scheduling options.

### 4.4 Logging

- Implement logging to track application activity and errors.
- Log files stored in the `logs/` directory.

## 5. Installation and Setup Instructions

### 5.1 Prerequisites

- Cursor AI installed on the system.
- Python 3.8 or higher.
- Pip package manager.
- Access to OpenAI or Anthropic API keys.

### 5.2 Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/cursor_note_automation.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd cursor_note_automation
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Application**

   - Rename `config/config_example.yaml` to `config/config.yaml`.
   - Enter your API keys and preferences in `config.yaml`.

5. **Set Up the Daily Script**

   - Make the scripts executable:

     ```bash
     chmod +x scripts/*.sh
     ```

   - Schedule `daily_run.sh` to run daily using `cron` or another scheduler.

### 5.3 Integration with Cursor AI

- Copy the `cursor_note_automation` folder to Cursor AI's plugins/extensions directory.
- Restart Cursor AI to load the new plugin.

## 6. Update Procedures

### 6.1 Updating the Application

- **Pull Updates from the Repository**

  ```bash
  git pull origin main
  ```

- **Run the Update Script**

  ```bash
  ./scripts/update.sh
  ```

### 6.2 Updating Dependencies

- **Upgrade Packages**

  ```bash
  pip install --upgrade -r requirements.txt
  ```

- **Check for Compatibility Issues**

  - Run tests to ensure everything functions correctly.

## 7. Context and Code Bases

### 7.1 Main Components

- **main.py**

  - Entry point of the application.
  - Initializes components and starts the application.

- **note_generator.py**

  - Contains logic for generating notes.
  - Interacts with the LLM for content synthesis.

- **variable_processor.py**

  - Handles input variables.
  - Processes and formats variables for note generation.

- **scheduler.py**

  - Manages the scheduling of daily scripts.
  - Uses the `schedule` library for task automation.

- **utils.py**

  - Utility functions used across the application.

### 7.2 Templates

- **note_template.txt**

  - Template for formatting the daily notes.
  - Uses placeholders for dynamic content insertion.

### 7.3 Configuration

- **config.yaml**

  - Stores configuration settings.
  - Includes API keys, user preferences, and scheduling options.

## 8. Testing and Quality Assurance

### 8.1 Testing Framework

- Use `unittest` or `pytest` for writing tests.
- Ensure all modules have corresponding test cases in the `tests/` directory.

### 8.2 Test Cases

- **test_note_generator.py**

  - Test note creation with various inputs.
  - Verify correct prefix assignment.

- **test_variable_processor.py**

  - Test processing of input variables.
  - Ensure proper handling of edge cases.

- **test_scheduler.py**

  - Test scheduling functionality.
  - Verify that scripts run at the correct times.

### 8.3 Continuous Integration

- Set up CI/CD pipeline using GitHub Actions or similar tools.
- Automate testing on code commits and pull requests.

## 9. User Guide Overview

- **Getting Started**

  - How to install and configure the application.
  - Basic usage instructions.

- **Using the Application**

  - Inputting variables.
  - Generating and viewing notes.
  - Customizing templates.

- **Advanced Features**

  - Modifying scheduling options.
  - Integrating with different LLMs.

- **Troubleshooting**

  - Common issues and solutions.
  - How to view logs and report bugs.

## 10. Focus on Maximizing Ease and Speed of Use

- **Intuitive Commands**

  - Provide easy-to-remember commands for common actions.
  - Implement autocomplete features if possible.

- **Quick Setup**

  - Simplify installation steps.
  - Provide clear and concise documentation.

- **User-Friendly Interface**

  - Design the UI with simplicity in mind.
  - Use clear prompts and feedback messages.

## 11. Automation and Daily Scripting Components

- **Automated Daily Run**

  - The application runs automatically at a specified time each day.
  - Generates notes without user intervention unless necessary.

- **Customizable Scheduling**

  - Allow users to set preferred times for automation.
  - Option to disable automation if desired.

- **Notifications**

  - Provide notifications within Cursor AI when new notes are available.
  - Option to send email or system notifications.

## 12. Integration with LLMs

- **API Key Management**

  - Securely store and manage API keys.
  - Allow switching between OpenAI and Anthropic APIs.

- **Error Handling**

  - Gracefully handle API errors and rate limits.
  - Provide meaningful error messages to the user.

- **Optimizing API Usage**

  - Implement caching mechanisms if appropriate.
  - Batch requests to reduce API calls.

## 13. Project Timeline

### Day 1

- Finalize and complete the PRD.