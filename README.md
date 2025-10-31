# django-n8n-api Project

This project is a Django REST Framework application designed to facilitate integration with n8n. It provides an API endpoint for sending data to n8n workflows.

## Project Structure

```
django-n8n-api
├── manage.py                # Command-line utility for interacting with the Django project
├── requirements.txt         # Lists project dependencies
├── .env.example             # Template for environment variables
├── Dockerfile               # Instructions for building a Docker image
├── README.md                # Project documentation
├── api_project              # Main Django project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps                     # Directory for Django apps
│   └── n8n_integration      # App for n8n integration
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── permissions.py
│       ├── tests.py
│       └── migrations
│           └── __init__.py
└── scripts                  # Directory for scripts
    └── bdjobs_hot_jobs_selenium.py  # Script for scraping job data
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd django-n8n-api
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in the required values.

5. **Run migrations:**
   ```
   python manage.py migrate
   ```

6. **Start the development server:**
   ```
   python manage.py runserver
   ```

## Usage

- The API endpoint for sending data to n8n can be accessed at `/api/n8n/` (or the specific path defined in your `urls.py`).
- Ensure that your n8n instance is set up to receive data from this endpoint.

## Docker

To build and run the Docker container, use the following commands:

1. **Build the Docker image:**
   ```
   docker build -t django-n8n-api .
   ```

2. **Run the Docker container:**
   ```
   docker run -d -p 8000:8000 django-n8n-api
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.