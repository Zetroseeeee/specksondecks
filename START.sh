#!/bin/bash

echo "=========================================="
echo "    SPECKS ON DECKS - BOOKING SYSTEM     "
echo "=========================================="
echo ""
echo "Starting the booking system..."
echo ""
echo "📋 Booking Form: http://localhost:5000/book"
echo "📊 Dashboard: http://localhost:5000/dashboard"
echo ""
echo "Press CTRL+C to stop"
echo ""
echo "=========================================="
echo ""

# Check if dependencies are installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Start the application
python3 app.py
