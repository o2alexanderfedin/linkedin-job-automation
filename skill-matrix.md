| #  | Technology                                      | Years Used | Years Tech Exists | Proficiency |
|----|-------------------------------------------------|------------|-------------------|-------------|
| 1  | Programming Languages (C#, C++, Java, TypeScript)| 25         | 25                | 10/10       |
| 2  | Relational DBs (MS SQL, MySQL, Postgres)        | 18         | 35+               | 10/10       |
| 3  | Leadership & Team Management (Local & Remote)   | 15         | 50                | 10/10       |
| 4  | Large Language Models (OpenAI GPT, Google Bard, LLaMA, Claude)| 2 | 5 | 10/10 |
| 5  | Prompt Engineering                              | 2          | 5                 | 10/10       |
| 6  | Retrieval-Augmented Generation & Vector DBs (Pinecone, PgVector) | 2 | 5 | 10/10 |
| 7  | Cloud Services (AWS, Azure)                     | 10         | 15                | 9/10        |
| 8  | RESTful microservices                           | 10         | 10                | 9/10        |
| 9  | Containers (Docker, Kubernetes, QEMU/WASM)      | 7          | 10                | 9/10        |
| 10 | NoSQL/Blob Storages                             | 15         | 20                | 9/10        |
| 11 | Software Methodologies (Agile, XP)              | 15         | 20                | 10/10       |
| 12 | Data pipelines                                  | 10         | 20                | 9/10        |
| 13 | Performance optimization                        | 12         | 20                | 9/10        |
| 14 | Queues (SQS, RabbitMQ, MassTransit, ServiceBUS) | 5          | 20                | 9/10        |
| 15 | MATLAB                                          | 10         | 35                | 9/10        |
| 16 | IoT                                             | 8          | 15                | 9/10        |
| 17 | UI (Maui, Blazor, QT, ASP.NET MVC, WPF, Angular, jQuery)| 15 | 20 | 9/10 |
| 18 | Actor Models (Akka, Orleans)                    | 7          | 20                | 10/10       |
| 19 | Soft real-time systems                          | 10         | 20                | 9/10        |



- **Epic 1:** User Authentication and Authorization
   - **Description:** Implement user authentication and role-based authorization.
   - **User Stories:**
      - **User Story 1:** As a user, I want to register and log in to the system so that I can access my tasks.
         - **Acceptance Criteria:**
            - 1. User can register with email and password.
            - 2. User can log in using registered credentials.
            - 3. User roles determine access levels.

- **Epic 2:** Task Management
   - **Description:** Core functionalities for managing tasks (CRUD operations).
   - **User Stories:**
      - **User Story 1:** As a user, I want to create a task so that I can keep track of my work.
         - **Acceptance Criteria:**
            - 1. User can create a task with title, description, due date, and priority.
            - 2. Task is stored in the database and retrievable.
      - **User Story 2:** As a user, I want to update a task to reflect changes in its status or details.
         - **Acceptance Criteria:**
            - 1. User can update task details.
            - 2. Changes are saved and reflected in the task list.

- **Epic 3:** Notifications and Alerts
   - **Description:** Notify users about task updates and deadlines.
   - **User Stories:**
      - **User Story 1:** As a user, I want to receive notifications for task deadlines.
         - **Acceptance Criteria:**
            - 1. User receives email or in-app notifications.
            - 2. Notifications are sent based on task due dates.

- **Epic 4:** Reporting and Analytics
   - **Description:** Provide insights into task progress and performance metrics.
   - **User Stories:**
      - **User Story 1:** As a manager, I want to view task completion reports to monitor team performance.
         - **Acceptance Criteria:**
            - 1. Reports show task completion rates and timelines.
            - 2. Data is filterable by user, project, and date range.