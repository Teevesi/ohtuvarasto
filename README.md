# ohtuvarasto

[![GHA workflow badge](https://github.com/Teevesi/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/Teevesi/ohtuvarasto/actions)
[![codecov](https://codecov.io/github/Teevesi/ohtuvarasto/graph/badge.svg?token=UEVOP3V870)](https://codecov.io/github/Teevesi/ohtuvarasto)

## Warehouse Management Web Application

A Flask-based web application for managing warehouses (Varasto). This application allows you to create, edit, and delete warehouses, as well as add and remove content from them.

### Features

- **Create warehouses** with custom capacity and initial balance
- **Edit warehouse capacity** - update the capacity of existing warehouses
- **Delete warehouses** - remove warehouses you no longer need
- **Add content** - add items to a warehouse
- **Remove content** - remove items from a warehouse
- **Visual progress bars** - see how full each warehouse is at a glance
- **Responsive design** - works on desktop and mobile devices

### Dependencies

- Python 3.12+
- Flask 3.0+

### Running the Application

1. Install dependencies:
   ```bash
   pip install flask
   ```

2. Run the Flask application:
   ```bash
   cd src
   python app.py
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000`

### Environment Variables

- `SECRET_KEY` - Flask secret key for session management (auto-generated if not set)
- `FLASK_DEBUG` - Set to `true` to enable debug mode (disabled by default)

### Running Tests

```bash
python -m pytest src/tests/ -v
```
