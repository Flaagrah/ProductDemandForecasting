import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

# Load environment variables from .env
load_dotenv()

# Get the API key from .env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file")
    exit(1)

print("Checking OpenAI API usage...")
print("=" * 50)

# Set up headers for API requests
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

try:
    # Get current date and calculate date range
    today = datetime.now()
    start_date = today.replace(day=1).strftime('%Y-%m-%d')  # First day of current month
    end_date = today.strftime('%Y-%m-%d')  # Today
    
    print(f"Checking usage from {start_date} to {end_date}")
    print("-" * 30)
    
    # Get usage information using the billing API
    response = requests.get(
        'https://api.openai.com/v1/usage',
        headers=headers,
        params={
            'date': start_date
        }
    )
    
    if response.status_code == 200:
        usage_data = response.json()
        
        if 'data' in usage_data and usage_data['data']:
            total_usage = usage_data['total_usage']
            print(f"✅ Total usage this month: {total_usage}")
            
            # Show daily breakdown
            print("\nDaily usage breakdown:")
            for day_data in usage_data['data']:
                date = day_data['date']
                usage = day_data['total_usage']
                print(f"  {date}: {usage} tokens")
        else:
            print("No usage data found for this period")
            
    elif response.status_code == 401:
        print("❌ Authentication failed - please check your API key")
    elif response.status_code == 403:
        print("❌ Access forbidden - your API key may not have billing access")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
    # Try to get account information
    print("\n" + "=" * 50)
    print("Checking account information...")
    
    account_response = requests.get(
        'https://api.openai.com/v1/models',
        headers=headers
    )
    
    if account_response.status_code == 200:
        models = account_response.json()
        print(f"✅ Account is active - {len(models['data'])} models available")
        print("Available models include:")
        for model in models['data'][:5]:  # Show first 5 models
            print(f"  - {model['id']}")
        if len(models['data']) > 5:
            print(f"  ... and {len(models['data']) - 5} more")
    else:
        print(f"❌ Could not verify account: {account_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print(f"\nChecked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
