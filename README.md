# Habit Tracker App

A simple API that allows users to track their habits and log their progress.

## Features ✨
- JWT-based authentication
- Create, update, delete, and view habits
- Log habit completion by date
- Retrieve logs for specific habits

## Technologies Used 🛠️
- **Backend framework:** Flask
- **Database:** MongoDB
- **Authentication:** Flask-JWT-Extended
- **Validation:** Marshmallow

## API Endpoints

### Auth
- `POST /auth/register` – Register a new user
- `POST /auth/login` – Login and receive a JWT token

### Habits
- `GET /habits` – Get all habits
- `POST /habits` – Create new habit
- `PUT /habits/<habit_id>` – Update habit
- `DELETE /habits/<habit_id>` – Delete habit

### Logs
- `GET /habits/<habit_id>/logs` – Get logs for a habit
- `POST /habits/<habit_id>/logs` – Log a habit for a date
- `DELETE /logs/<log_id>` – Delete log

## How to Run 🚀
1. Clone this repository: `git clone https://github.com/lia-xyz/habit-tracker-app.git`
2. Create virtual environment: `python -m venv venv`
```
On Mac: source venv/bin/activate
On Windows: venv\Scripts\activate
```
3. Install dependencies: `pip install -r requirements.txt`
4. Setup environment variables. Create a `.env` file and add the following:
```
MONGO_URI=your_database_url
JWT_SECRET_KEY=your_jwt_key
```
5. Run the app: `python run.py`

## Contributing 🤝

Contributions, issues, and feature requests are welcome!  
Feel free to fork the repo and submit a pull request.

## License 📄
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.