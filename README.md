# Pong Web Game

Welcome to the **Pong Web Game** project, an online version of the classic Pong game. This project combines the fun of gaming with modern technologies and a secure architecture.

## Description

**Pong Web Game** allows users to play Pong in an online environment. The application offers a responsive and interactive user interface, with features for user login and score tracking to monitor player performance.

## Features

- **User Authentication:** Sign up, login, and account management.
- **Account Security:** Two-factor authentication (2FA) for enhanced security.
- **Session Management:** Use of JWT tokens to secure sessions.
- **Leaderboards:** Tracking user scores with leaderboard display.
- **Game Interface:** Interactive Pong game developed.
- **Logs and Monitoring:** Integration of ELK (Elasticsearch, Logstash, Kibana) and Grafana for log visualization and performance metrics.

## Technologies Used

- **Frontend:** 
  - HTML5, CSS3 (with Bootstrap for design)
  - Pure JavaScript for application logic and game management
- **Backend:** 
  - Django for REST API management
- **Database:** 
  - PostgreSQL for storing user data and scores
- **Containerization:** 
  - Docker for deploying microservices
- **Secrets Management:** 
  - HashiCorp Vault for securely storing database credentials and SSL certificates
- **Logs and Monitoring:** 
  - ELK Stack (Elasticsearch, Logstash, Kibana) for log management
  - Grafana for visualizing performance metrics

## Architecture

The project is structured into microservices, each with a specific responsibility:

- **Authentication Service:** Manages signup, login, and 2FA.
- **Game Service:** Handles Pong game logic, game sessions, and scores.
- **Storage Service:** Interacts with the PostgreSQL database.
- **Logging Service:** Manages logs and metrics using ELK.
