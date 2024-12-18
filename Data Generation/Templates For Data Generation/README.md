# Data Generation Templates for Announcement and Document Queries

## Overview
This repository contains templates for generating queries related to **Announcements** and **Documents** for university-related data systems. These templates are designed to create dynamic questions by substituting placeholders with various options, making it easier to generate diverse queries for different contexts.

## Announcement Data Template

The **Announcement** template focuses on generating queries related to university events, deadlines, and activities, such as registration periods, application deadlines, and availability of different programs or services.

### Structure:
- **Placeholders**: Use `\\g<1>`, `\\g<2>`, etc., to represent different entities (e.g., course registration, internship application).
- **Categories**: The queries are structured around common questions about semesters, deadlines, and availability of programs.

### Example Queries:
- "Is \\g<1> open for this semester?"  
  Possible values for `\\g<1>`: course registration, student survey, internship application, etc.
  
- "What is the \\g<1> deadline?"  
  Possible values for `\\g<1>`: add/drop period, internship application deadline, scholarship submission, etc.
  
- "When can I register for \\g<1>, \\g<2>, and \\g<3>?"  
  Possible values for `\\g<1>`, `\\g<2>`, and `\\g<3>`: final exam schedule, course enrollment, TA recruitment, etc.

- "Are \\g<1> and \\g<2> available for this semester?"  
  Possible values for `\\g<1>` and `\\g<2>`: spring semester courses, summer internships, peer mentoring program, etc.

This template is focused on generating queries relevant to specific academic events or administrative tasks tied to a semester schedule or student needs.

## Document Data Template

The **Document** template focuses on generating queries related to university documents, resources, and services for students, faculty, and staff. It aims to create questions regarding how to access, apply for, or submit various documents.

### Structure:
- **Placeholders**: Use `\\g<1>`, `\\g<2>`, etc., to represent different actions, entities, or audiences (e.g., find, apply, students, faculty).
- **Categories**: The queries cover topics like document access, submission, and application processes across multiple user roles.

### Example Queries:
- "How can I \\g<1> \\g<2> for \\g<3> \\g<4>?"  
  Possible values for `\\g<1>`: find, access, apply, etc.  
  Possible values for `\\g<2>`: job listings, internship opportunities, etc.  
  Possible values for `\\g<3>`: students, faculty, staff, etc.  
  Possible values for `\\g<4>`: via the portal, online, in person, etc.

- "What \\g<1> can I \\g<2> in \\g<3>?"  
  Possible values for `\\g<1>`: documents, resources, procedures, etc.  
  Possible values for `\\g<2>`: apply, submit, download, etc.  
  Possible values for `\\g<3>`: the student information system, the internship platform, etc.

This template is aimed at generating queries about how users can interact with documents and systems, based on different user roles and access methods.

## Key Differences

- **Announcement Template**: Focuses on generating queries related to specific university activities or services with time-sensitive relevance (e.g., registration periods, deadlines).
- **Document Template**: Focuses on creating queries related to university documents and the actions users can perform with them (e.g., applying, submitting, accessing).

Both templates use dynamic placeholders (`\\g<1>`, `\\g<2>`, etc.) to generate diverse query variations, helping simulate a wide range of possible user questions based on real university operations.
