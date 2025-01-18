# Grocery Tracking Agent 🛒

An intelligent AI-powered grocery management system built with CrewAI and Google's Gemini model. The system helps you track groceries, manage expiration dates, get recipe recommendations, and monitor grocery expenses through a team of specialized AI agents. Now with support for processing receipt images directly!

## Overview 🎯

The Grocery Tracking Agent uses multiple AI agents to help you:
- Process and interpret grocery receipts (now supports both images and markdown)
- Track expiration dates of food items
- Manage your grocery inventory
- Get recipe recommendations based on available ingredients
- Monitor and analyze grocery expenses
- Minimize food waste through smart tracking

## Features ✨

### Receipt Interpretation
- Automatic extraction of items, quantities, and prices from receipts
- Support for both image and markdown-formatted receipts
- Advanced image processing using Gemini Vision AI
- Intelligent text extraction and categorization
- Structured data output for inventory management

### Expiration Date Tracking
- Intelligent estimation of product shelf life using StillTasty.com data
- Automatic expiration date calculation from purchase date
- Proactive notifications for items nearing expiration

### Inventory Management
- Real-time tracking of available groceries
- Consumption tracking and inventory updates
- Automated stock level monitoring

### Recipe Recommendations
- Smart recipe suggestions based on available ingredients
- Integration with America's Test Kitchen for reliable recipes
- Prioritization of ingredients nearing expiration

### Expense Tracking
- Detailed breakdown of grocery expenses
- Category-wise spending analysis
- Monthly and weekly expense summaries
- Budget tracking and recommendations
- Price trend analysis for frequently bought items

## Prerequisites 📋

- Python 3.8+
- Google Gemini API key
- Required Python packages:
  ```
  crewai==0.80.0
  crewai_tools==0.14.0
  Markdown==3.7
  google-generativeai==0.3.2
  Pillow==10.2.0
  ```

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Grocery_Tracking_Agent.git
cd Grocery_Tracking_Agent
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory and add:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Project Structure 📁

```
Grocery_Tracking_Agent/
├── agent.py           # Core agent definitions and logic
├── data/
│   ├── grocery_tracker.json    # Inventory tracking data
│   ├── grocery_receipt.md      # Processed receipt data
│   ├── receipt_image.jpg       # Input receipt image (optional)
│   └── expense_history.json    # Expense tracking data
├── .env              # Environment variables
└── README.md         # Project documentation
```

## Running the Application 🚀

1. Prepare your receipt (two options):
   
   a. Using an image receipt:
   - Place your receipt image in `data/receipt_image.jpg` (supports jpg, png, jpeg)
   - The system will automatically process the image and convert it to markdown
   
   b. Using a markdown receipt:
   - Place your receipt in markdown format in `data/grocery_receipt.md`

2. Run the agent system:
```bash
python agent.py
```

The system will:
- Process your receipt (image or markdown)
- Extract items and prices
- Calculate expiration dates
- Update inventory
- Suggest recipes
- Track and analyze expenses

3. View the outputs:
- Inventory tracking: Check `data/grocery_tracker.json`
- Recipe recommendations: See terminal output
- Expense analysis: View `data/expense_history.json`
- Processed receipt: View `data/grocery_receipt.md`

## Agents System 🤖

The project uses five specialized AI agents:

1. **Receipt Interpreter Agent**
   - Processes receipt data from images or markdown
   - Uses Gemini Vision AI for image processing
   - Extracts item names, quantities, and prices
   - Provides structured data for inventory tracking

2. **Expiration Date Estimation Agent**
   - Connects to StillTasty.com for shelf life data
   - Calculates expiration dates based on purchase date
   - Provides accurate storage recommendations

3. **Grocery Tracker Agent**
   - Maintains real-time inventory
   - Updates stock levels based on consumption
   - Tracks remaining quantities and expiration dates

4. **Recipe Recommendation Agent**
   - Searches America's Test Kitchen for recipes
   - Suggests dishes based on available ingredients
   - Helps reduce food waste through smart recipe planning

5. **Expense Tracking Agent**
   - Analyzes receipt data for spending patterns
   - Categorizes expenses by product type
   - Generates spending reports and summaries
   - Tracks price changes over time
   - Provides budget insights and recommendations
   - Identifies potential savings opportunities

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 