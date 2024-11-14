# Biodiversity Tracking Database

**Course:** Database Management Systems | UE22CS351A  
**Project:** Bio-Sustainability Tracking Database  
**Authors:**  
- Namita Achyuthan (PES1UG22AM100)  
- R Deeksha (PES1UG22AM125)  

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Features](#project-features)
3. [User Classes](#user-classes)
4. [System Architecture](#system-architecture)
5. [Database Design](#database-design)
6. [Setup and Installation](#setup-and-installation)
7. [Usage](#usage)
8. [Advanced SQL Operations](#advanced-sql-operations)
9. [Future Enhancements](#future-enhancements)
10. [References](#references)

## Project Overview
The **Biodiversity Tracking Database** is a comprehensive tool designed to aid researchers, conservationists, city planners, and policymakers in monitoring and managing biodiversity within specific regions. This web-based platform serves as a centralized repository to catalog species, record habitat information, and track conservation activities. The database aims to support scientific research and practical conservation by providing a user-friendly interface for data management and analysis.

## Project Features
- **Species Database:** Store detailed information about local flora and fauna.
- **Sustainability Initiative Tracking:** Log and manage data on conservation and sustainability projects.
- **Data Analysis:** Analyze biodiversity metrics to assess the impact of sustainability practices.
- **Reporting and Visualization:** Generate insights through interactive charts and geographic maps.
- **Citizen Science Module:** Enable the public to contribute biodiversity observations.
- **Predictive Modeling:** Forecast biodiversity trends using data analytics.

## User Classes
1. **Researchers** - Analyze biodiversity data for environmental studies.
2. **City Planners** - Use data to plan sustainability initiatives.
3. **Conservationists** - Focus on monitoring biodiversity and habitat health.
4. **Administrators** - Manage database access and maintenance.
5. **Policy Makers** - Leverage data to inform environmental policies.
6. **Citizen Scientists** - Contribute to biodiversity tracking through observations.
7. **General Public** - Access biodiversity information and contribute observations.

## System Architecture
The project uses a client-server model with the following stack:
- **Backend:** Python (Flask for web application, MySQL for database management)
- **Frontend:** HTML, CSS, and JavaScript for UI, with visualization libraries for data presentation.
- **Database:** MySQL, with relational tables for species, habitats, sustainability initiatives, and biodiversity metrics.
- **Operating System:** Ubuntu, selected for stability and compatibility with open-source tools.

## Database Design
### Key Entities
- **Species**: Stores species ID, name, habitat, conservation status, and other attributes.
- **Sustainability Initiative**: Logs data on conservation and sustainability efforts.
- **Biodiversity Metric**: Tracks metrics such as species count and health index.
- **User**: Manages user authentication and roles.
- **Report**: Holds generated reports, including analysis and insights.

### Entity-Relationship (ER) Diagram
The ER Diagram provides a graphical view of database entities and relationships.

### Relational Schema
A relational schema is designed to ensure data integrity and optimized for scalability. Key relationships include:
- **Species to BiodiversityMetric** (One-to-Many)
- **SustainabilityInitiative to BiodiversityMetric** (One-to-Many)
- **User to Report** (One-to-Many)

## Setup and Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/biodiversity-tracking-database.git
   cd biodiversity-tracking-database
   ```
2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip mysql-server
   pip install -r requirements.txt
   ```
3. **Configure MySQL**:
   - Create a MySQL database and user for the project.
   - Update the MySQL credentials in the `.env` file.
4. **Run the database setup scripts**:
   ```sql
   source db_setup.sql;
   ```
5. **Start the Flask application**:
   ```bash
   python app.py
   ```

## Usage
- **Login and User Roles:** Login with appropriate credentials based on your role (e.g., Researcher, Administrator).
- **Data Entry:** Use the web forms to add new species, habitats, and sustainability initiatives.
- **Data Analysis:** View biodiversity metrics and trends using interactive charts and geographic maps.
- **Generate Reports:** Create and download reports on species trends and sustainability effectiveness.

## Advanced SQL Operations
- **Triggers:** Automated logging and deletion restrictions maintain an audit trail and ensure data integrity.
- **Stored Procedures:** Custom procedures for retrieving biodiversity metrics linked to specific initiatives.
- **Views:** Predefined views consolidate data for reporting purposes.
- **Nested Queries:** Enable complex analysis, such as aggregate metrics per species and sustainability impact.

## Future Enhancements
- Mobile Application: Extend platform access to mobile devices.
- AI-Based Predictive Analytics: Enhance biodiversity forecasting accuracy with machine learning.
- Expanded Citizen Science Features: Include a broader range of public-contribution tools.
- Data Sharing API: Facilitate data exchange with other conservation and biodiversity platforms.

## References
- Urban Biodiversity and Ecology Research Papers
- Local Biodiversity Action Plans
- IUCN Red List of Threatened Species
- United Nations Sustainable Development Goals (SDGs)
- National Biodiversity Strategies and Action Plans (NBSAPs)
