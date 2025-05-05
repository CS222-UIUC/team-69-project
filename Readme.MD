
# Tutorswap

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]

[contributors-shield]: https://img.shields.io/github/contributors/CS222-UIUC/team-69-project.svg?style=for-the-badge
[contributors-url]: https://github.com/CS222-UIUC/team-69-project/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/CS222-UIUC/team-69-project.svg?style=for-the-badge
[forks-url]: https://github.com/CS222-UIUC/team-69-project/network/members

[stars-shield]: https://img.shields.io/github/stars/CS222-UIUC/team-69-project.svg?style=for-the-badge
[stars-url]: https://github.com/CS222-UIUC/team-69-project/stargazers


## Summary

Tutorswap is a peer-to-peer tutoring platform designed for UIUC students. It allows students to connect based on the classes they need help in or can tutor. Unlike formal tutoring platforms, Tutorswap matches students based on shared courses, ratings, recent activity, and academic background—focusing on accessibility and relevance over certification.

Key features include:
- Login and profile creation
- Tutor matching based on course overlap, rating, and major
- Real-time messaging with matched users
- Course-based and user-based search
- Class-specific rating and review system
- AI-powered starter messages for chat

---

## Technical Architecture


![Python](https://img.shields.io/badge/Python-55%25-blue?style=for-the-badge&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-31%25-3178c6?style=for-the-badge&logo=typescript&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-9.9%25-purple?style=for-the-badge&logo=css3&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-1.8%25-e34c26?style=for-the-badge&logo=html5&logoColor=white)
![Shell](https://img.shields.io/badge/Shell-1.4%25-89e051?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Dockerfile](https://img.shields.io/badge/Dockerfile-0.5%25-384d54?style=for-the-badge&logo=docker&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-0.4%25-f1e05a?style=for-the-badge&logo=javascript&logoColor=black)


<p align="center">
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/react/react.png" height="30" alt="React"/> &nbsp;
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/typescript/typescript.png" height="30" alt="TypeScript"/> &nbsp;
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/flask/flask.png" height="30" alt="Flask"/> &nbsp;
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/postgresql/postgresql.png" height="30" alt="PostgreSQL"/> &nbsp;
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/socket-io/socket-io.png" height="30" alt="Socket.IO"/> &nbsp;
  <img src="https://raw.githubusercontent.com/github/explore/main/topics/javascript/javascript.png" height="30" alt="JavaScript"/>
</p>


<p align="center">
  <img src="https://github.com/CS222-UIUC/team-69-project/blob/main/backend/tech-arch.jpeg?raw=true" alt="Tutorswap Technical Architecture" width="600"/>
</p>



Tutorswap follows a full-stack architecture:

**Frontend**: React + TypeScript, styled with MUI, supports dynamic routing and state management for profile creation, search, and chat.

**Backend**: Flask + Flask-SocketIO powers the core API and real-time chat. It includes matching logic (Python), user authentication (OAuth), and class/course rating endpoints.

**Database**: PostgreSQL stores user profiles, ratings, messages, and match history. GIN indexing supports fuzzy search and name autocomplete.

**DevOps**: GitHub Actions for linting (Flake8) and testing (Pytest, 98% coverage).

---

## Components

### Login and Register Pages  
Users can create accounts or log in using a simple interface connected to Flask sessions. Once authenticated, users are redirected to the homepage and have access to all platform features.

- Adeetya created the login page UI  
- Aryaa designed the signup page in Figma  
- Yash implemented both flows in React  
- Cameron connected backend logic and session handling  

### Home Page  
The welcome page, where potential users understand how our platform operates. It shows how to use the platform, basic top user info, and a Call To Action.

- Designed in Figma by Aryaa and Adeetya  
- React implementation by Yash  
- Backend data connection by Cameron  

### Matching Page  
Displays top matches based on course overlap, user rating, major similarity, and recent activity. The logic includes scoring and ranking, with fuzzy search and filters.

- Matching algorithm written by Adeetya  
- Backend search optimization and GIN indexing by Aryaa  
- React frontend by Yash  
- Integrated end-to-end by Cameron  

### Chat Page  
Enables real-time messaging between matched users. Messages are stored by match ID and loaded dynamically. Also includes AI-generated starter prompts using GPT.

- Backend logic and AI prompt generation by Adeetya  
- Chat UI built by Yash in React  
- Server connection and SocketIO setup by Cameron  

---

## How to Install

1. **Clone the repository**
    ```bash
    git clone https://github.com/CS222-UIUC/team-69-project.git
    cd team-69-project
    ```

2. **Frontend setup**
    ```bash
    cd frontend
    npm install --force
    npm start
    ```

3. **Backend setup**
    ```bash
    cd ../backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    flask run
    ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Team Contributions

| Name      | Role                        | Highlights |
|-----------|-----------------------------|------------|
| **Adeetya** | Matching, Backend APIs, Design | Built the matching algorithm, designed login page UI, created REST endpoints, added fuzzy subject search, and implemented AI-enhanced chat messages |
| **Aryaa**   | UI/UX Design, Backend Search    | Designed profile and signup pages, optimized fuzzy search with GIN indexing, implemented filtering and sorting logic |
| **Yash**    | Frontend Engineer               | Built login, signup, homepage, and chat features in React, integrated styling and frontend logic |
| **Cameron** | Integration & System Setup      | Connected backend APIs to frontend, created the PostgreSQL schema, added dummy data, integrated SocketIO and chat backend |

All members contributed to planning, regular check-ins, code reviews, and final testing.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

Special thanks to **Akshat Bhat**, our mentor on this project, for his guidance, feedback, and support throughout the semester.
