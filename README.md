# Food Recommendation & Nutrition Tracker

A comprehensive web application for tracking nutrition, getting food recommendations, and receiving AI-powered nutrition advice. Built with Flask, Python, and modern web technologies.

## Features

### Nutrition Tracking
- Log daily food consumption
- Track calories, protein, carbs, and fat
- View detailed nutrition breakdowns
- Set and monitor daily calorie goals

### AI Nutrition Assistant
- Intelligent chatbot for nutrition questions
- Personalized food recommendations
- Health benefit explanations for various foods
- Diet planning and meal prep advice

### Dashboard & Analytics
- Real-time nutrition statistics
- BMI calculation and tracking
- Water intake monitoring
- Weekly goal setting and tracking

### Food Database
- Searchable database of 100+ foods
- Add custom food entries
- Database cleaning and maintenance tools
- CSV export functionality

### User Management
- Secure registration and login
- Personalized user profiles
- Goal tracking (weight loss/gain/maintenance)
- Activity level-based calorie calculations

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/kennou-js/food-recommendation-nutrition-tracker.git
cd food-recommendation-nutrition-tracker
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up the database**
```bash
python app.py
```
This will automatically create the necessary directories and sample food database.

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
Open your browser and navigate to: `http://localhost:5000`

## Project Structure

```
food-recommendation-nutrition-tracker/
├── app.py                    # Main Flask application
├── models/
│   ├── food.py              # Food database model
│   └── user.py              # User management model
├── utils/
│   ├── chatbot.py           # AI nutrition assistant
│   └── calculator.py        # Nutrition calculations
├── data/                    # Data storage directory
├── templates/               # HTML templates
├── static/
│   ├── css/                # Stylesheets
│   └── js/                 # JavaScript files
└── requirements.txt         # Python dependencies
```

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Food Management
- `GET /api/search?q=<query>` - Search food database
- `POST /api/log_food` - Log food consumption
- `GET /api/recommend?food=<name>` - Get food recommendations
- `POST /api/add_food` - Add custom food to database

### User Management
- `POST /api/create_user` - Create user profile
- `POST /api/update_profile` - Update user profile
- `GET /api/daily_summary` - Get daily nutrition summary

### Nutrition Assistant
- `POST /api/chat` - Chat with AI nutrition assistant
- `POST /api/calculate_nutrition` - Calculate nutrition for food list

## Core Components

### 1. Nutrition Chatbot
- Natural language processing for food questions
- Comprehensive knowledge base of 100+ foods
- Context-aware conversations
- Personalized recommendations based on user profile

### 2. Food Database
- CSV-based food database with nutritional information
- Search functionality with fuzzy matching
- Category-based organization
- Custom food entry support

### 3. Nutrition Calculator
- BMI calculation
- TDEE (Total Daily Energy Expenditure) estimation
- Macro nutrient distribution
- Water intake recommendations

### 4. User Management
- Session-based authentication
- Profile management with health metrics
- Goal tracking
- Daily food logging

## Usage Examples

### 1. Logging Food
1. Navigate to "Food Log" page
2. Search for a food item
3. Enter quantity and meal type
4. Click "Log Food"

### 2. Getting Nutrition Advice
1. Go to "Assistant" page
2. Ask questions like:
   - "What are the benefits of salmon?"
   - "How much protein should I eat daily?"
   - "Compare chicken and beef nutrition"

### 3. Setting Up Profile
1. Complete registration
2. Enter personal details (age, weight, height)
3. Select activity level and goal
4. View personalized calorie targets

## Dependencies

### Python Packages
- Flask (Web framework)
- pandas (Data manipulation)
- numpy (Numerical operations)

### Frontend Libraries
- Font Awesome (Icons)
- Vanilla JavaScript (Client-side functionality)
- CSS3 (Styling)

## Configuration

### Environment Setup
1. The application uses a development secret key by default
2. Data is stored in the `data/` directory
3. Templates are in the `templates/` directory
4. Static files are in the `static/` directory

### Security Notes
- Uses Flask sessions for authentication
- Development secret key should be changed for production
- No password hashing in current implementation (for demo purposes)

## Features in Detail

### Dashboard
- Real-time calorie tracking
- Nutrition breakdown by meal
- Water intake tracker
- Quick actions for common tasks

### Food Database Management
- Add new foods with custom nutrition values
- Clean database of unrealistic entries
- Export database as CSV
- Search and filter functionality

### AI Assistant Capabilities
- Food comparison
- Health benefit explanations
- Meal planning suggestions
- Diet-specific advice (Keto, Vegan, Mediterranean)
- Weight management strategies

## Troubleshooting

### Common Issues

1. **Database not created**
   - Ensure `data/` directory has write permissions
   - Check if `food_database.csv` exists in `data/` directory

2. **Port already in use**
   - Change port in `app.py` line: `app.run(debug=True, port=5000)`
   - Ensure no other applications are using port 5000

3. **Import errors**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **CSS/JS not loading**
   - Clear browser cache
   - Check if static files are in correct location
   - Verify Flask static file configuration

## Development

### Adding New Features
1. Create new route in `app.py`
2. Add corresponding template in `templates/`
3. Update navigation in `base.html`
4. Add any required CSS/JS files

### Extending Food Database
1. Add entries to `data/food_database.csv`
2. Format: `id,name,category,calories,protein,fat,carbs,fiber,sugar`
3. Restart application to reload database

### Customizing Chatbot
1. Edit `knowledge_base` in `utils/chatbot.py`
2. Add new food entries with benefits and nutrition info
3. Extend pattern matching for new question types

## Limitations

### Current Version
- Local storage only (no cloud sync)
- Single-user focus (easily extendable to multi-user)
- Basic authentication (no password hashing)
- CSV-based database (consider SQL for production)

### Planned Improvements
- User photo upload for progress tracking
- Mobile app version
- Social features (share progress, challenges)
- Integration with fitness APIs
- Advanced analytics and reporting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available for educational and personal use.

## Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed description

## Acknowledgments

- Built with Flask web framework
- Uses Font Awesome for icons
- Inspired by modern nutrition tracking applications

---

**Note**: This is a demonstration application for educational purposes. For production use, consider implementing proper security measures, database systems, and user authentication.
