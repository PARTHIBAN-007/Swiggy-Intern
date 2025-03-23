import sqlite3

conn = sqlite3.connect("feedback.db")
cursor = conn.cursor()

feedback_data = [
    ("The delivery was very late, and the food was cold.", "Late delivery with cold food.", 3, "Delivery Experience"),
    ("Fast delivery, but the packaging was damaged.", "Quick delivery but bad packaging.", 6, "Delivery Experience"),
    ("The delivery person was very polite and professional.", "Polite and professional delivery.", 9, "Delivery Experience"),
    ("The food arrived on time and well packed.", "Timely delivery with good packaging.", 8, "Delivery Experience"),
    ("Delivery took way longer than expected, very frustrating.", "Very delayed delivery.", 2, "Delivery Experience"),
    ("The delivery guy called ahead and made sure everything was correct.", "Good service and communication.", 9, "Delivery Experience"),
    ("They delivered to the wrong address first, causing a delay.", "Delivery mix-up, caused delay.", 4, "Delivery Experience"),
    ("The driver was rude and unhelpful.", "Rude delivery driver.", 3, "Delivery Experience"),
    ("Great experience, they followed all instructions carefully.", "Delivery followed all instructions.", 10, "Delivery Experience"),
    ("Took too long but at least the food was warm.", "Late but warm food.", 5, "Delivery Experience"),
    
    # Food Quality
    ("The pizza was undercooked and tasteless.", "Undercooked and bland pizza.", 3, "Food Quality"),
    ("Very fresh and tasty ingredients, loved it!", "Fresh and delicious food.", 9, "Food Quality"),
    ("The portion size was too small for the price.", "Small portions for price.", 5, "Food Quality"),
    ("The food was cold and stale.", "Cold and stale food.", 2, "Food Quality"),
    ("Great flavors and well-seasoned!", "Tasty and well-seasoned.", 8, "Food Quality"),
    ("The food was oily and heavy.", "Too oily and heavy.", 4, "Food Quality"),
    ("Amazing quality, would order again!", "High-quality food.", 10, "Food Quality"),
    ("The meat was overcooked and chewy.", "Overcooked and chewy meat.", 3, "Food Quality"),
    ("Good taste but too salty.", "Tasty but overly salty.", 6, "Food Quality"),
    ("Super fresh sushi, really impressed!", "Fresh and great sushi.", 9, "Food Quality"),
    
    # Customer Service
    ("Customer service was very unhelpful and rude.", "Rude customer service.", 2, "Customer Service"),
    ("They resolved my issue quickly and efficiently.", "Quick and efficient service.", 9, "Customer Service"),
    ("Waited too long to get a response from support.", "Slow customer support.", 4, "Customer Service"),
    ("The agent was very friendly and helpful.", "Friendly and helpful service.", 8, "Customer Service"),
    ("They refused to offer a refund even though my order was wrong.", "Refused refund for incorrect order.", 3, "Customer Service"),
    ("Very professional and understanding staff.", "Professional and understanding.", 10, "Customer Service"),
    ("They kept transferring me to different departments.", "Unorganized support system.", 5, "Customer Service"),
    ("Polite staff but slow response time.", "Polite but slow service.", 6, "Customer Service"),
    ("Excellent service, they really care about customers.", "Excellent customer service.", 10, "Customer Service"),
    ("Support team was clueless about my issue.", "Uninformed support team.", 3, "Customer Service"),
    
    # App Usability
    ("The app crashes frequently, making it hard to use.", "Frequent app crashes.", 2, "App Usability"),
    ("Very smooth experience, easy to navigate.", "Smooth and user-friendly.", 9, "App Usability"),
    ("Ordering is confusing and not intuitive.", "Confusing ordering process.", 4, "App Usability"),
    ("The UI is clean and modern.", "Clean and modern UI.", 8, "App Usability"),
    ("Too many bugs, needs improvement.", "Buggy and needs fixes.", 3, "App Usability"),
    ("Great performance and fast loading times.", "Fast and efficient app.", 10, "App Usability"),
    ("Hard to find certain options in the menu.", "Difficult navigation.", 5, "App Usability"),
    ("The checkout process is too slow.", "Slow checkout process.", 6, "App Usability"),
    ("Best food ordering app I've used!", "Top-notch app usability.", 10, "App Usability"),
    ("Search function does not work properly.", "Broken search function.", 4, "App Usability"),
    
    # Other
    ("Would be nice to have more payment options.", "Limited payment options.", 5, "Other"),
    ("The referral program is great!", "Great referral program.", 9, "Other"),
    ("Their ads are very misleading.", "Misleading advertisements.", 3, "Other"),
    ("Good experience overall, no major complaints.", "Overall positive experience.", 7, "Other"),
    ("Their social media presence is very engaging.", "Engaging social media.", 8, "Other"),
    ("I had trouble finding their contact info.", "Difficult to find contact info.", 4, "Other"),
    ("The company gives back to the community, which I love!", "Strong community involvement.", 10, "Other"),
    ("They need better promotions and discounts.", "Lack of promotions.", 5, "Other"),
    ("Nice rewards program, but needs improvements.", "Decent rewards program.", 6, "Other"),
    ("Their packaging is very eco-friendly, which I appreciate!", "Eco-friendly packaging.", 9, "Other"),
]

# Insert data into the feedback table
cursor.executemany(
    "INSERT INTO feedback (text, summary, rating, domain, resolved) VALUES (?, ?, ?, ?, 0)", 
    feedback_data
)

# Commit and close the connection
conn.commit()
conn.close()

print("Database populated with sample feedback data successfully!")
