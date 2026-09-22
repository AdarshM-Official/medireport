# MediReport AI

MediReport AI is a powerful, Django-based clinical intelligence application designed to analyze medical reports, track longitudinal patient health trends, and provide advanced body composition analytics.

## Features

- **AI-Powered Report Analysis**: Upload medical documents and receive structured clinical breakdowns, identifying key metrics and potential health risks using Generative AI.
- **Longitudinal Health Tracking**: Automatically aggregates historical health data from your profile to track clinical trends over time.
- **Advanced BMI Simulator**: A beautifully designed, interactive body composition calculator. 
  - **Auto Mode**: Pulls directly from your clinical profile.
  - **Interactive Mode**: Features real-time sliders to simulate different heights and weights instantly.
  - **Advanced Metrics**: Calculates Ideal Body Weight (IBW), Healthy Weight Ranges, and Ponderal Index.
- **Modern UI/UX**: Built with a custom "glassmorphic" aesthetic, enhanced by Tailwind CSS utility classes and fluid CSS animations.
- **Secure Patient Profiles**: Stores critical clinical data like age, blood type, height, weight, and chronic conditions to contextualize AI analysis.

## Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (via CDN with preflight overrides), Custom CSS (Glassmorphism)
- **Database**: SQLite (Development)
- **AI Integration**: Google Gemini API (or equivalent configured LLM for report parsing)

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
   Ensure you have a `.env` file in the root directory containing your necessary API keys (e.g., `GEMINI_API_KEY`) and Django `SECRET_KEY`.

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

## Recent Updates

- **Tailwind UI Overhaul**: The BMI calculator has been entirely redesigned using Tailwind CSS, featuring staggered fade-in animations and a two-column interactive layout.
- **Clinical Dashboard Merge**: Consolidated the patient profile grid and longitudinal health trends into a single, cohesive scrolling view.
- **Profile Context Fixes**: Enhanced profile data retrieval to prevent rendering errors when patient data is missing.

## License
Proprietary / Private codebase.
