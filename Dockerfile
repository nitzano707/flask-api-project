# השתמש בבסיס Python
FROM python:3.9-slim

# הגדר ספריית עבודה
WORKDIR /app

# העתק את כל הקבצים לתוך המיכל
COPY . /app

# התקנת התלויות
RUN pip install --no-cache-dir -r requirements.txt

# חשוף את הפורט
EXPOSE 8080

# הפעל את האפליקציה
CMD ["python", "main.py"]
