import psycopg2
import json
from datetime import date

# الاتصال بقاعدة البيانات
conn = psycopg2.connect(
    host="localhost",
    database="blog",
    user="blog",
    password="youssef2009"
)
cursor = conn.cursor()

# بيانات JSON التي تحتوي على البوستات
posts = [
  {
    "title": "The Future of Technology",
    "slug": "future-of-technology",
    "body": "Technology is rapidly advancing, and the future holds many exciting possibilities. From artificial intelligence to quantum computing, we are witnessing innovations that will change the world forever.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "Understanding Artificial Intelligence",
    "slug": "understanding-artificial-intelligence",
    "body": "Artificial Intelligence (AI) has already begun to reshape our daily lives. From voice assistants to self-driving cars, AI is becoming an integral part of modern technology.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "The Impact of Climate Change",
    "slug": "impact-of-climate-change",
    "body": "Climate change is one of the most pressing issues facing our planet. Rising temperatures, melting glaciers, and extreme weather events are just a few of the consequences we face.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "The Importance of Mental Health",
    "slug": "importance-of-mental-health",
    "body": "Mental health is just as important as physical health. It’s crucial to take care of your mind, as it affects your overall well-being and quality of life.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "How to Build a Successful Startup",
    "slug": "how-to-build-a-successful-startup",
    "body": "Building a startup is challenging but rewarding. From identifying the right market to scaling your business, here are key steps for creating a successful startup.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "The Evolution of Social Media",
    "slug": "evolution-of-social-media",
    "body": "Social media has transformed the way we communicate, share information, and consume content. Let's explore how it has evolved and its impact on society.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "The Role of Education in Shaping Society",
    "slug": "role-of-education-in-shaping-society",
    "body": "Education plays a vital role in shaping society by providing knowledge, fostering critical thinking, and preparing individuals for the challenges of the future.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "Exploring Space: The Final Frontier",
    "slug": "exploring-space-the-final-frontier",
    "body": "Space exploration has always fascinated humanity. With new advancements, we are venturing further into space to uncover the mysteries of our universe.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "The Rise of Remote Work",
    "slug": "rise-of-remote-work",
    "body": "Remote work has seen a massive rise, especially during the pandemic. Companies are increasingly adopting flexible work arrangements, offering employees more freedom and work-life balance.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "The Art of Mindfulness",
    "slug": "art-of-mindfulness",
    "body": "Mindfulness is the practice of being present in the moment. It has proven benefits for reducing stress, improving focus, and enhancing overall well-being.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "The Power of Positive Thinking",
    "slug": "power-of-positive-thinking",
    "body": "Positive thinking can lead to better health, increased happiness, and success. Learn how cultivating a positive mindset can transform your life.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "The History of the Internet",
    "slug": "history-of-the-internet",
    "body": "The internet has changed the world in ways we never imagined. From its humble beginnings as a military project to the global network we rely on today, let's look at the history of the internet.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "How to Stay Productive While Working from Home",
    "slug": "how-to-stay-productive-working-from-home",
    "body": "Working from home presents its own set of challenges. Here are some tips to help you stay focused, organized, and productive while working remotely.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "Exploring the World of Cryptocurrencies",
    "slug": "exploring-world-of-cryptocurrencies",
    "body": "Cryptocurrencies have gained tremendous popularity in recent years. In this post, we will explore what they are, how they work, and their potential to change the financial landscape.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  },
  {
    "title": "How to Build a Personal Brand",
    "slug": "how-to-build-personal-brand",
    "body": "In today’s digital age, building a personal brand is crucial for standing out. Here’s how to develop and promote a personal brand that resonates with your audience.",
    "auther_id": 1,
    "publish": "2024-12-28",
    "status": "Published",
    "created": date.today(),
    "updated": date.today()
  }
]

# استعلام SQL لإدخال البيانات
insert_query = """
INSERT INTO home_post (title, slug, body, auther_id, publish, status, created, updated)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

# جمع البيانات من JSON
values = [(post["title"], post["slug"], post["body"], post["auther_id"], post["publish"], post["status"], post["created"], post["updated"]) for post in posts]

# إدخال البيانات دفعة واحدة
cursor.executemany(insert_query, values)

# التأكيد على الإدخال
conn.commit()

# إغلاق الاتصال
cursor.close()
conn.close()

print(" successfully inserted data into the database.")
