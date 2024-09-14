# Food and Calorie Tracker API

The **Food and Calorie Tracker API** is designed to help users track their daily food intake, manage their calories, and set fitness goals. It provides features like logging meals, tracking calorie intake, setting custom calorie goals, and managing user profiles.

## Features

- **User Authentication**: Secure authentication with OAuth2 and JWT for token-based access.
- **Profile Management**: Users can manage their profiles, including personal details, fitness goals, and weight targets.
- **Food Entry Management**: Add, search, update, and delete food entries associated with your profile.
- **Daily Caloric Goal**: Set a daily caloric goal and track progress based on food logged.
- **Password Reset**: Secure password reset functionality via email.

## Endpoints

### Authentication
- `POST /login`: User login with credentials.
- `POST /signup`: Register a new user.
- `POST /forgot-password`: Trigger password reset email.
- `POST /reset-password/{secret_token}`: password reset.

### User Profile
- `GET /users/me/profile`: Get the authenticated user's profile.
- `POST /users/me/profile`: Create user's profile.
- `PUT /users/profile/edit-profile`: Update user profile information.
- `DELETE /users/profile/delete-profile`: Removes user profile information.

### Food Entries
- `POST /food`: Log a new food entry.
- `GET /foods`: Retrieve all food entries by user.
- `GET /foods/{food_id}`: Retrieve a food entry by its ID.
- `PUT /foods/{food_id}`: Update a food entry.
- `DELETE /foods/{food_id}`: Delete a food entry.
- `GET /foods/search`: Search for foods by name (only authenticated user's data).
- `GET /foods/total-calories`: Retrieve user's sum total calorie intake.

### Daily Caloric Goal
- `POST /users/me/calorie-goal`: Set a daily caloric goal.
- `GET /users/me/calorie-goal`: Get daily caloric goal.
- `GET /users/me/calorie-goal-progress`: Get progress toward the daily caloric goal.


## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/PreciousSteve/food-calorie-api.git
   cd food-calorie-api
   ```

2. **Set up the virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the root directory to store secret keys and configurations:
   Example:
   ```env
   APP_HOST=http://localhost:8000
   DATABASE_URL=sqlite:///./foodcal.db.sqlite
   SECRET_KEY=your-secret-key
   JWT_ALGORITHM=HS256
   MAIL_USERNAME=your-email@example.com
   MAIL_PASSWORD=your-email-password
   MAIL_FROM=noreply@example.com
   ```

6. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

7. **API Documentation**:
   You can access the interactive API docs at `http://localhost:8000/docs`.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Contributions are always welcome!
