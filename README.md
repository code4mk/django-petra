# Django Petra

Django Petra is a powerful collection of utilities and enhancements for Django Rest Framework (DRF), designed to streamline the process of building RESTful APIs. It provides convenience functions, tools, and patterns to help developers write clean, efficient, and maintainable code.

## Features

### Core Functionality
- Enhanced DRF core components for common API development tasks
- Customized base classes with improved functionality
- Utility functions and mixins for common API patterns
- Simplified pagination, routing, and data serialization

### File Storage
- Flexible storage system supporting both local and S3 storage
- Easy file operations (put, get, delete, update, etc.)
- Temporary URL generation for S3
- Directory listing and file management

### Email Management
- Enhanced email sending capabilities
- HTML template support with inline CSS
- Queue-based email sending using Celery
- Attachment support including inline images

### CORS Handling
- Comprehensive CORS middleware
- Configurable CORS settings
- Origin whitelist and regex support
- Preflight request handling

### API Logging
- Automatic API request/response logging
- Performance metrics tracking
- Client IP tracking
- Detailed request/response information storage

### Task Scheduling
- Celery integration for background tasks
- Flexible scheduling patterns (cron-style)
- Various scheduling intervals (seconds to yearly)
- Queue management

### Database Utilities
- Raw query helpers
- Custom model managers
- Soft delete functionality
- Time-stamped model mixins

