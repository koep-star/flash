🎯 Flashcard Learning App
A powerful Streamlit-based flashcard application with spaced repetition, image support, and progress tracking.

Features
📚 Interactive Study Sessions: Study your flashcards with a clean, intuitive interface
🖼️ Image Support: Add images to your flashcards for visual learning
⏰ Spaced Repetition: Suppress cards based on difficulty (1-14 days)
📊 Progress Tracking: Monitor your learning progress and card statistics
📥 Import/Export: Add cards manually or import from CSV files
🎲 Randomized Study: Cards are shuffled for optimal learning
Installation
Clone this repository:
bash
git clone https://github.com/yourusername/flashcard-app.git
cd flashcard-app
Install required packages:
bash
pip install -r requirements.txt
Run the application:
bash
streamlit run app.py
Usage
Adding Cards
Navigate to the "Manage Cards" tab
Use "Add New Card" to create individual flashcards
Optionally upload images for visual learning
Or import multiple cards from a CSV file
CSV Import Format
Your CSV file should have the following columns:

question: The question text
answer: The answer text
image: (optional) Path to image file
Example CSV:

csv
question,answer,image
"What is the capital of France?","Paris",
"What does this symbol mean?","Addition operator","images/plus_sign.png"
Studying
Go to the "Study" tab
Read the question and any associated image
Click "Reveal Answer" when ready
Rate your knowledge level:
Hard (1 day): Card reappears tomorrow
Medium (3 days): Card reappears in 3 days
Easy (7 days): Card reappears in a week
Perfect (14 days): Card reappears in 2 weeks
Statistics
Monitor your progress in the "Statistics" tab:

View total, available, and suppressed cards
See when each card will be available for review again
Reset your progress if needed
File Structure
flashcard-app/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── flashcards.json     # Your flashcard data (auto-generated)
├── progress.json       # Learning progress (auto-generated)
├── images/            # Directory for uploaded images
└── README.md          # This file
Data Files
The app automatically creates and manages these files:

flashcards.json: Stores all your flashcard questions, answers, and image paths
progress.json: Tracks when each card was last studied and when it should reappear
Contributing
Fork the repository
Create a feature branch
Make your changes
Submit a pull request
License
This project is licensed under the MIT License.

Troubleshooting
Images not displaying
Ensure image files are in the correct path
Supported formats: PNG, JPG, JPEG
Images are automatically saved to the images/ directory when uploaded
Cards not appearing
Check if cards are suppressed in the Statistics tab
Use "Reset All Progress" to make all cards available again
CSV import issues
Ensure your CSV has 'question' and 'answer' columns
Use proper CSV formatting with quotes around text containing commas

