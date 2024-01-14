# TikTok Backend Clone

## Description

This project is a backend clone of the popular social media app TikTok, created for educational purposes. The aim is to recreate key functionalities of TikTok, applying technologies and best practices in software development that I've learned throughout my career. This repository contains the server-side code and API endpoints. 💻

## Features

This project implements a variety of functionalities inspired by TikTok, structured into different endpoints to emulate key operations of a social network. The endpoints currently developed or in development are as follows:

### 1) Users (90%):
- **User Registration**: Allows new users to create an account. `POST /users/register`
- **User Login**: Authentication for user access. `POST /users/login`
- **Get User Profile**: View specific user profile information. `GET /users/{userid}`
- **Update User Profile**: Allows users to modify their profile. `PUT /users/{userid}`
- **Delete User**: Remove a user from the system. `DELETE /users/{userid}`

### 2) Videos (TO DO 🚧):
- **Upload Video**: Users can upload videos. `POST /videos`
- **Get Video Details**: View specific details of a video. `GET /videos/{videoid}`
- **List Videos**: Get a list of all available videos. `GET /videos`
- **Delete Video**: Allows users to delete their videos. `DELETE /videos/{videoid}`

### 3) Interactions and Social Network (TO DO 🚧):
- **Like a Video**: Users can 'like' videos. `POST /videos/{videoid}/like`
- **Unlike a Video**: Remove 'like' from a video. `DELETE /videos/{videoid}/like`
- **Comment on a Video**: Post comments on videos. `POST /videos/{videoid}/comment`
- **Delete Comment**: Delete own comments from a video. `DELETE /videos/{videoid}/comment/{commentid}`
- **Follow a User**: Follow other users. `POST /users/{userid}/follow`
- **Unfollow a User**: Unfollow other users. `DELETE /users/{userid}/follow`

### 4) Feed and Discoveries (TO DO 🚧):
- **Get Video Feed**: View a personalized feed of videos. `GET /feed`
- **Search Videos/Users**: Search functionality in the platform. `GET /search`


## Technologies Used

- Python
- Django
- Django Rest Framework
- Django Rest Framework-simplejwt
- PostgreSQL
- pylint (for linting)
- JWT (JSON Web Tokens) for authentication

## Getting Started

To get started with the TikTok Clone backend, follow these steps:

1. Clone the repository: `git clone https://github.com/EdinsonRequena/tiktok-backend-clone`
2. Install the dependencies: `pipenv install Pipfile`
3. Set up the environment variables (e.g., database connection, Postgres credentials)
4. Start the server: `python manage.py runserver`

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. PRs must have a minimum of 80% test coverage to be accepted.

## License

This project is licensed under the [MIT License](LICENSE).