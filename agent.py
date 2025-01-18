# Grocery Management Agents System

# Step 1: Install Required Packages
# Make sure you have the necessary packages installed:

# !pip install Markdown==3.7
# !pip install crewai==0.80.0
# !pip install crewai_tools==0.14.0
# !pip install google-generativeai==0.3.2
# !pip install Pillow==10.2.0

import os
import json
from datetime import datetime
from pathlib import Path
from crewai import Agent, Task, Crew, LLM
from markdown import markdown
from crewai_tools import WebsiteSearchTool
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your environment variables")

# Initialize Gemini model
gemini_model = LLM(
    api_key=GOOGLE_API_KEY,
    model="gemini/gemini-1.5-flash",
)

# Configure Gemini Vision model for receipt processing
genai.configure(api_key=GOOGLE_API_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

def process_receipt_image(image_path):
    """
    Process a receipt image using Gemini Vision model and convert it to markdown format
    """
    try:
        # Load and process the image
        image = Image.open(image_path)
        
        # Generate prompt for receipt analysis
        prompt = """
        Analyze this receipt image and extract the following information in markdown format:
        - Store name and date
        - List of items with:
          * Item name
          * Quantity
          * Price
          * Category (Groceries/Produce/Dairy/etc.)
        Format the output as a proper markdown document.
        """
        
        # Get response from Gemini Vision
        response = vision_model.generate_content([prompt, image])
        markdown_content = response.text
        
        # Save the markdown content
        output_path = Path('data/grocery_receipt.md')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(markdown_content)
        
        print(f"Receipt processed and saved to {output_path}")
        return markdown_content
        
    except Exception as e:
        print(f"Error processing receipt image: {str(e)}")
        return None

# Initialize data directory
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# Initialize expense history file with default structure
expense_history_path = data_dir / 'expense_history.json'
default_expense_history = {
    "expenses": [],
    "categories": {},
    "monthly_summaries": {}
}

# Create expense_history.json if it doesn't exist or is empty
if not expense_history_path.exists() or expense_history_path.stat().st_size == 0:
    with open(expense_history_path, 'w') as f:
        json.dump(default_expense_history, f, indent=2)
    print("Created new expense history file with default structure")
    expense_history = default_expense_history
else:
    try:
        with open(expense_history_path, 'r') as f:
            expense_history = json.load(f)
        print("Expense history loaded successfully!")
    except json.JSONDecodeError:
        print("Error: expense_history.json is corrupted. Creating new file...")
        with open(expense_history_path, 'w') as f:
            json.dump(default_expense_history, f, indent=2)
        expense_history = default_expense_history

# Load the receipt (either from image or existing markdown)
receipt_markdown = ""
receipt_image_path = Path('data/receipt.png')  # Support common formats: jpg, png, jpeg

if receipt_image_path.exists():
    print("Found receipt image, processing...")
    receipt_markdown = process_receipt_image(receipt_image_path)
    if not receipt_markdown:
        print("Failed to process receipt image, checking for markdown file...")

if not receipt_markdown:
    try:
        markdown_path = data_dir / 'grocery_receipt.md'
        if not markdown_path.exists():
            # Create an empty markdown file if it doesn't exist
            markdown_path.write_text("")
            print("Created empty grocery_receipt.md file")
        
        with open(markdown_path, 'r') as f:
            receipt_markdown = markdown(f.read())
        if receipt_markdown.strip():
            print("Receipt loaded successfully from markdown!")
        else:
            print("Warning: grocery_receipt.md is empty")
    except Exception as e:
        print(f"Error reading markdown file: {str(e)}")
        receipt_markdown = ""


# Step 2: Set Up Your API Key
# You will need an OpenAI API key to proceed. Please store it securely and load it into your environment.
# Additionally, if you wish to test the functionality that reads real receipts and converts them into markdown files, you'll need a LLAMA OCR API key. This is optional but recommended for testing with actual receipt images. You can obtain a LLAMA OCR API key from here.
# Note: Sample receipts have already been processed and saved in the file located at: data/grocery_management_agents_system/extracted/grocery_receipt.md.


# Step 3: Extract Receipt Information from a Receipt Image (Optional)
# By default, the test extracted information has already been saved in:
# GenAI_Agents/data/grocery_management_agents_system/extracted/grocery_receipt.md.

# However, if you'd like to test using different receipt images, you can do so by following these steps:

# Add Your Receipt Image
# Place your image in the following folder:
# GenAI_Agents/data/grocery_management_agents_system/input

# Update the Script
# Open the extract_items.js file and change the filePath variable to the name of your new image.

# Run the Script
# In your terminal, navigate to the input directory and run the script:

# cd GenAI_Agents/data/grocery_management_agents_system/input
# node extract_items.js
# The newly generated markdown file will be saved in:
# `GenAI_Agents/data/grocery_management_agents_system/extracted/`
# How to Use Node.js

# To get started with Node.js, you'll first need to install NVM (Node Version Manager). This allows you to easily manage different versions of Node.js on your system.

# For macOS users, you can find a detailed guide on installing NVM here.


# Step 3: Extract Receipt Information from a Receipt Image (Optional)
# We'll start by reading a markdown file containing the grocery receipt.
from markdown import markdown

# Load the markdown receipt file
with open('data/grocery_receipt.md', 'r') as f:
    receipt_markdown = markdown(f.read())

# Today's date for reference
today = datetime.now().strftime("%Y-%m-%d")
print("Receipt loaded successfully!")

# 4. Creating the Agents
# Step 4.1: Receipt Interpreter Agent
receipt_interpreter_agent = Agent(
    role="Receipt Markdown Interpreter",
    goal=(
        "Accurately extract items, their counts, and weights with units from a given receipt in markdown format. "
        "Provide structured data to support the grocery management system."
    ),
    backstory=(
        "As a key member of the grocery management crew for the household, your mission is to meticulously extract "
        "details such as item names, quantities, and weights from receipt markdown files. Your role is vital for the "
        "grocery tracker agent, which monitors the household's inventory levels."
    ),
    personality=(
        "Diligent, detail-oriented, and efficient. The Receipt Markdown Interpreter is committed to providing accurate "
        "and structured information to support effective grocery management. It is particularly focused on clarity and precision."
    ),
    allow_delegation=False,
    verbose=True,
    llm=gemini_model
)

print("Receipt Interpreter Agent created successfully!")

# Step 4.2: Expiration Date Estimation Agent
# Use website earch tool to search the website "www.stilltasty.com"
# Initialize the tool with Google as the provider
expiration_date_search_web_tool = WebsiteSearchTool(
    website='https://www.stilltasty.com/',
    config=dict(
        llm=dict(
            provider="google",
            config=dict(
                model="gemini/gemini-1.5-flash"
            ),
        ),
        embedder=dict(
            provider="google",
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
            ),
        ),
    )
)

print("Expiration Date Search Web Tool created successfully!")

expiration_date_search_agent = Agent(
    role="Expiration Date Estimation Specialist",
    goal=(
        "Accurately estimate the expiration dates of items extracted by the Receipt Markdown Interpreter Agent. "
        "Utilize online sources to determine typical shelf life when refrigerated and add the estimated number of days to the purchase date."
    ),
    backstory=(
        "As the Expiration Date Estimation Specialist, your role is to ensure the household's groceries are consumed before expiration. "
        "You use your access to online resources to search for the best estimates on how long each item typically lasts when stored properly."
    ),
    personality=(
        "Meticulous, resourceful, and reliable. This agent ensures the household maintains a well-stocked but efficiently used inventory, minimizing waste."
    ),
    allow_delegation=False,
    verbose=True,
    tools=[expiration_date_search_web_tool],
    llm=gemini_model
)

print("Expiration Date Estimation Agent created successfully!")

# Step 4.3: Grocery Tracker Agent
grocery_tracker_agent = Agent(
    role="Grocery Inventory Tracker",
    goal=(
        "Accurately track the remaining groceries based on user consumption input. "
        "Subtract consumed items from the grocery list obtained from the Expiration Date Estimation Specialist and update the inventory. "
        "Provide the user with an updated list of what's left, along with corresponding expiration dates."
    ),
    backstory=(
        "As the household's Grocery Inventory Tracker, your responsibility is to ensure that groceries are accurately tracked based on user input. "
        "You need to understand the user's input on what they've consumed, update the inventory list, and remind them of what's left and the expiration dates. "
        "Your role is crucial in helping the household avoid waste and ensure timely consumption of perishable items."
    ),
    personality=(
        "Helpful, detail-oriented, and responsive. This agent is focused on ensuring the household has an up-to-date inventory, minimizing waste, and helping users stay organized."
    ),
    allow_delegation=False,
    verbose=True,
    llm=gemini_model
)

print("Grocery Tracker Agent created successfully!")
# Step 4.4: Recipe Recommendation Agent

recipe_web_tool = WebsiteSearchTool(
    website='https://www.americastestkitchen.com/recipes',
    config=dict(
        llm=dict(
            provider="google",
            config=dict(
                model="gemini/gemini-1.5-flash"
            ),
        ),
        embedder=dict(
            provider="google",
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
            ),
        ),
    )
)

# Optimized Grocery Recipe Recommendation Agent
rest_grocery_recipe_agent = Agent(
    role="Grocery Recipe Recommendation Specialist",
    goal=(
        "Provide recipe recommendations using the remaining groceries in the inventory. "
        "Avoid using items with a count of 0 and prioritize recipes that maximize the use of available ingredients. "
        "If ingredients are insufficient, suggest restocking recommendations."
    ),
    backstory=(
        "As a Grocery Recipe Recommendation Specialist, your mission is to help the household make the most out of their remaining groceries. "
        "Your role is to search the web for easy, delicious recipes that utilize available ingredients while minimizing waste. "
        "Ensure that the recipes are simple to follow and use as many of the remaining ingredients as possible."
    ),
    personality=(
        "Creative, resourceful, and efficient. This agent is dedicated to helping the household create enjoyable meals with what they have on hand."
    ),
    allow_delegation=False,
    verbose=True,
    tools=[recipe_web_tool],
    human_input=True,
    llm=gemini_model
)

print("Grocery Recipe Recommendation Agent created successfully!")

# Step 5.1: Task for Reading the Receipt
read_receipt_task = Task(
    agent=receipt_interpreter_agent,
    description=(
        f"Analyze the receipt markdown file provided: {receipt_markdown}. "
        "Extract information on items purchased, their counts, weights, and units. "
        f"Additionally, extract today's date information which is provided here: {today}. "
        "Ensure all item names are converted into clear, human-readable text."
    ),
    expected_output="""
    {
        "items": [
            {
                "item_name": "string - Human-readable name of the item",
                "count": "integer - Number of units purchased",
                "unit": "string - Unit of measurement (e.g., kg, lbs, pcs)"
            }
        ],
        "date_of_purchase": "string - Date in YYYY-MM-DD format"
    }
    """
)

print("Read Receipt Task created successfully!")

# Step 5.2: Task for Expiration Date Estimation
expiration_date_search_task = Task(
    agent=expiration_date_search_agent,
    description=(
        "Using the list of items extracted by the Receipt Markdown Interpreter Agent, search online to find the typical shelf life of each item when refrigerated. "
        "Add this information to the date of purchase to estimate the expiration date for each item."
        "Ensure that the output includes the item name, count, unit, and estimated expiration date."
    ),
    expected_output="""
    {
        "items": [
            {
                "item_name": "string - Human-readable name of the item",
                "count": "integer - Number of units purchased",
                "unit": "string - Unit of measurement (e.g., kg, lbs, pcs)",
                "expiration_date": "string - Estimated expiration date in YYYY-MM-DD format"
            }
        ]
    }
    """,
    context=[read_receipt_task]
)

print("Expiration Date Search Task created successfully!")

# Step 5.3: Task for Grocery Tracking
grocery_tracking_task = Task(
    agent=grocery_tracker_agent,
    description=(
        "Using the grocery list with expiration dates provided by the Expiration Date Estimation Specialist, "
        "update the inventory based on user input about items they have consumed. "
        "Subtract the consumed quantities from the inventory list and provide a summary of what items are left, including their expiration dates. "
        "Ensure that the updated list is returned in JSON format."
    ),
    expected_output="""
    {
        "items": [
            {
                "item_name": "string - Human-readable name of the item",
                "count": "integer - Updated number of units remaining",
                "unit": "string - Unit of measurement (e.g., kg, lbs, pcs)",
                "expiration_date": "string - Estimated expiration date in YYYY-MM-DD format"
            }
        ]
    }
    """,
    context=[expiration_date_search_task],
    human_input=True,
    output_file = "data/grocery_tracker.json"
)

print("Grocery Tracking Task created successfully!")

# Step 5.4: Task for Recipe Recommendation
recipe_recommendation_task = Task(
    agent=rest_grocery_recipe_agent,
    description=(
        "Using the updated grocery list provided by the Grocery Inventory Tracker, "
        "search online for recipes that utilize the available ingredients. "
        "Only include items with a count greater than zero. If no suitable recipe can be found, provide restocking recommendations. "
        "Ensure that the output includes recipe names, ingredients, instructions, and the source website."
    ),
    expected_output="""
    {
        "recipes": [
            {
                "recipe_name": "string - Name of the recipe",
                "ingredients": [
                    {
                        "item_name": "string - Ingredient name",
                        "quantity": "string - Quantity required",
                        "unit": "string - Measurement unit (e.g., kg, pcs, tbsp)"
                    }
                ],
                "steps": [
                    "string - Step-by-step instructions for the recipe"
                ],
                "source": "string - Website URL for the recipe"
            }
        ],
        "restock_recommendations": [
            {
                "item_name": "string - Name of the item to restock",
                "quantity_needed": "integer - Suggested quantity to purchase",
                "unit": "string - Measurement unit (e.g., kg, pcs)"
            }
        ]
    }
    """,
    context=[grocery_tracking_task],
    output_file = "data/recipe_recommendation.json"
)

print("Recipe Recommendation Task created successfully!")

# Step 5.5: Expense Tracking Agent
expense_tracking_agent = Agent(
    role="Grocery Expense Analyst",
    goal=(
        "Track and analyze grocery expenses, provide spending insights, and help optimize the grocery budget. "
        "Generate detailed reports on spending patterns and identify potential savings opportunities."
    ),
    backstory=(
        "As the household's Grocery Expense Analyst, you are responsible for maintaining detailed records of all grocery "
        "expenses, categorizing items, tracking price trends, and providing actionable insights for budget optimization. "
        "Your analysis helps the household make informed decisions about their grocery spending."
    ),
    personality=(
        "Analytical, detail-oriented, and proactive. This agent excels at identifying spending patterns, tracking price "
        "changes, and suggesting ways to optimize the grocery budget while maintaining quality."
    ),
    allow_delegation=False,
    verbose=True,
    llm=gemini_model
)

print("Expense Tracking Agent created successfully!")

# Step 5.6: Task for Expense Tracking
expense_tracking_task = Task(
    agent=expense_tracking_agent,
    description=(
        "Using the receipt data from the Receipt Interpreter Agent, analyze the expenses and generate a detailed report. "
        "Track spending patterns, categorize items, calculate totals, and provide insights for budget optimization. "
        "Store the expense data in the expense history file and generate a summary report."
    ),
    expected_output="""
    {
        "expense_summary": {
            "total_amount": "float - Total amount spent",
            "date": "string - Purchase date",
            "category_breakdown": {
                "category_name": "float - Amount spent in this category"
            }
        },
        "insights": [
            "string - Spending insights and recommendations"
        ],
        "price_trends": [
            {
                "item_name": "string - Name of the item",
                "current_price": "float - Current price",
                "average_price": "float - Average price from history",
                "price_trend": "string - Increasing/Decreasing/Stable"
            }
        ]
    }
    """,
    context=[read_receipt_task],
    output_file="data/expense_history.json"
)

print("Expense Tracking Task created successfully!")

# 6. Running the Crew

# Create a crew with all agents and tasks
crew = Crew(
    agents=[
        receipt_interpreter_agent,
        expiration_date_search_agent,
        grocery_tracker_agent,
        rest_grocery_recipe_agent,
        expense_tracking_agent
    ],
    tasks=[
        read_receipt_task,
        expiration_date_search_task,
        grocery_tracking_task,
        recipe_recommendation_task,
        expense_tracking_task
    ],
    verbose=True
)

# Kick off the crew
result = crew.kickoff()

print("Crew kicked off successfully!")