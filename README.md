# MediReport AI

MediReport AI is a powerful, Django-based clinical intelligence application designed to analyze medical reports, track longitudinal patient health trends, and provide advanced body composition analytics.

<p align="left">
  <img src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="TailwindCSS" />
  <img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E" alt="JavaScript" />
  <img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini" />
</p>

## System Architecture & Technical Implementation

The application is built on a monolithic Django architecture, utilizing a hybrid frontend approach that combines traditional Django templates with modern utility-first CSS and Vanilla JS for high interactivity.

### App Structure
- **`analyser` App**: The core engine of the platform. Handles the patient dashboard, routing for medical report uploads, the logic for the Interactive BMI Simulator, and server-side PDF generation.
- **`ai` App / Module**: Encapsulates the logic for communicating with external Large Language Models (LLMs). Handles prompt engineering, image/PDF processing, and structured data extraction.

### AI Integration & Parsing
- **Generative AI Parsing**: Unstructured medical documents (PDFs, images) are parsed using the Google Gemini API. 
- **Prompt Engineering Guards**: System prompts are explicitly configured to enforce strict medical adherence and prevent hallucinations (e.g., refusing to generate clinical data from non-medical images).
- **Structured Output**: The AI is instructed to return structured JSON data, which is then parsed by Python and rendered into Django templates.

### Database & Data Modeling
- **Profile Contextualization**: Uses Django's built-in `User` model linked via a `OneToOneField` to a custom `UserProfile` model. This profile stores critical clinical data (DOB, Blood Type, Height, Weight, Chronic Conditions).
- **Exception Handling**: The architecture safely handles missing reverse relations (e.g., when a user hasn't set up a profile yet) by utilizing robust `hasattr(request.user, 'profile')` checks in views rather than relying on generic exception catching, preventing `RelatedObjectDoesNotExist` crashes.

### Frontend Architecture
- **Hybrid Styling**: The global layout (`base.html`) uses custom CSS to establish a "Glassmorphism" aesthetic (translucent backgrounds, heavy blur filters, gradients). 
- **Tailwind CSS Injection**: For highly complex, interactive views (like the BMI Simulator), Tailwind CSS is injected via CDN. To prevent Tailwind's base reset from destroying the global Django layout, `preflight: false` is configured in the Tailwind config script block.
- **Vanilla JavaScript**: Real-time interactions, such as the two-way data binding in the custom BMI sliders and the dynamic visual BMI scale, are handled entirely client-side using lightweight Vanilla JavaScript, avoiding the overhead of heavy SPA frameworks like React.
- **PDF Generation**: Medical reports are exported client-to-server and generated using the `reportlab` library, ensuring the downloaded PDF exactly matches the structured AI analysis.

## Core Features

- **AI-Powered Report Analysis**: Upload medical documents and receive structured clinical breakdowns, identifying key metrics and potential health risks.
- **Longitudinal Health Tracking**: Automatically aggregates historical health data from your profile to track clinical trends over time.
- **Advanced BMI Simulator**: A beautifully designed, interactive body composition calculator. 
  - **Auto Mode**: Pulls directly from your clinical `UserProfile`.
  - **Interactive Mode**: Features real-time sliders to simulate different heights and weights instantly.
  - **Advanced Metrics**: Calculates Ideal Body Weight (IBW) using the Devine formula, Healthy Weight Ranges, and Ponderal (Corpulence) Index.

## Installation & Setup

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd medireport
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Environment Variables**:
   Create a `.env` file in the root directory. You must supply your secret keys for the application to function:
   ```env
   SECRET_KEY=your_django_secret_key
   GEMINI_API_KEY=your_google_gemini_api_key
   DEBUG=True
   ```

6. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## Recent Technical Updates

- **Tailwind UI Overhaul**: The BMI calculator was rebuilt utilizing Tailwind CSS grid systems and custom keyframe animations (`animate-fade-in-up`, `animate-pulse-slow`).
- **Dashboard View Consolidation**: Removed legacy JavaScript tab wrappers on the dashboard, merging the patient profile grid and longitudinal health trends into a continuous server-rendered view.

## License
Proprietary / Private codebase.
