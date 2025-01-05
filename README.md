# Real-Time Collaborative Document Editor

This project is a collaborative text editor that allows multiple users to work on documents simultaneously. It supports real-time editing, rich-text formatting, and permissions management based on user roles.

## Features

- **Real-time collaboration**: Multiple users can edit the same document simultaneously with changes reflected in real-time.
- **Role-based access control**: Restrict document viewing and editing based on user permissions (e.g., view-only, editor).
- **Rich text editing**: Uses Quill.js for rich text features like bold, italics, lists, and headings.
- **WebSocket-based**: Updates are broadcast in real-time using Django Channels and WebSockets.
- **Redis caching**: Caches document data for faster load times and reduced database access.
- **Low-latency updates**: Utilizes Redis Channel Layer for efficient message passing between clients and server.
- **Unique collaboration sessions**: Each document is assigned a unique session using UUIDs.

## Technologies Used

- **Backend**: Django, Django Channels
- **Frontend**: Quill.js, JavaScript, HTML, CSS
- **Database**: SQLite (can be configured to MySQL/PostgreSQL)
- **Real-time communication**: WebSockets, Redis (for caching and message layer)

