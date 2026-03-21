# Workshop 02 - Systems Design  
## Local Business Recovery Support System - Titan Plaza Case Study  


## Members
- Sara Sofia Socha Gil  
- Daniel Eduardo Rincon Vivas  
- Diego Alejandro Yañez Zabala  
- Sebastian Zambrano Hurtado  

<br>

## Project Description

This workshop focuses on the **design of a system solution** based on the findings obtained in Workshop 01.  

The proposed system, *Local Business Recovery Support System*, aims to support small businesses in shopping malls by improving customer engagement, data analysis, and decision-making processes.

Using the results from the system analysis, a structured **system architecture** was designed to address the identified challenges such as uneven customer flow, dependency on external factors (weather, day), and changing post-pandemic behaviors.

<br>

## Design Methodology

The system design was developed following a structured engineering approach:

### 1. Analysis Review

---

Key findings from Workshop 01 were analyzed to identify:
- High variability in customer flow
- External factors affecting behavior (weather, day, time)
- New customer habits after the pandemic
- Business needs for better decision-making tools

These insights were translated into **system requirements**.

<br>

### 2. System Architecture Design

---

A **layered architecture** was defined, composed of:

- **Frontend (Presentation Layer):**
  User interface for customers and business owners

- **Backend (Application Layer):**
  Core system logic and processing

- **Database (Data Layer):**
  Storage of system data (users, businesses, activity)

- **External Services (Integration Layer):**
  APIs for notifications and external integrations

<br>

### 3. System Modules

---

The system was divided into key functional modules:

- User Management  
- Business Management  
- Analytics Module  
- Recommendation System  

Each module was designed to handle specific responsibilities and interact through the backend.

<br>

### 4. Interface and Integration Design

---

A detailed diagram was created to show how system components interact:

- Frontend communicates with backend via HTTP requests  
- Backend processes logic and connects to internal modules  
- Modules interact with the database for data storage  
- Backend integrates with external services (notifications, APIs)

<br>

### 5. Risk and Complexity Management

---

Several system challenges were considered:

- Variability in customer behavior  
- Dependence on environmental factors  
- Data inconsistency risks  

To address these, the system includes:

- Data validation mechanisms  
- Modular architecture for flexibility  
- Scalable design for future growth  

<br>

### 6. Implementation Strategy
---

The system was designed with a clear technical approach:

- Backend: API-based architecture  
- Frontend: Web-based interface  
- Database: Relational database system  
- Integration: External APIs for notifications  

The implementation is planned in phases to ensure scalability and maintainability.

<br>

### 7. Performance and Optimization
---

The system includes strategies to improve performance:

- Monitoring customer activity patterns  
- Data-driven recommendations for businesses  
- Optimization of resource usage  

Performance metrics considered:
- User interaction rates  
- System response time  
- Data processing efficiency  

<br>

## Deliverables

- System Design Document (PDF)  
- Architecture Diagrams  
- Interface and Integration Diagrams  
- Updated Repository Documentation  

<br>

## Key Outcomes

- Transformation of analysis into a structured system design  
- Definition of system architecture and modules  
- Identification of technical strategies and implementation approach  
- Preparation for future development and system implementation  

<br>

## Course Information

**Course:** Systems Analysis and Design  
**Program:** Computer Engineering  
**University:** Universidad Distrital Francisco José de Caldas  
**Semester:** 2026-I  

<br>

## Notes

This workshop represents the transition from **system analysis to system design**, establishing the foundation for future implementation, simulation, and validation phases of the project.
