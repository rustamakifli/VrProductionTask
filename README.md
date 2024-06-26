# VrProductionTask
## Prerequisites

- Python 3.x
- Git
- Virtualenv

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/rustamakifli/VrProductionTask.git
cd VrProductionTask
```
### Setting Up the Virtual Environment
macOS and Linux
Create a Virtual Environment:

```bash
python3 -m venv venv
```
### Activate the Virtual Environment:

```bash
source venv/bin/activate
```
## Windows

### Setting Up the Virtual Environment
Create a Virtual Environment:

```bash
python -m venv venv
```
### Activate the Virtual Environment:

```bash
venv\Scripts\activate
```

## Install Dependencies
With the virtual environment activated, install the project dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup
Run migrations
```bash
python manage.py migrate
```
Create a Superuser
```bash
python manage.py createsuperuser
```
## Running the Development Server
```bash
python manage.py runserver
```
