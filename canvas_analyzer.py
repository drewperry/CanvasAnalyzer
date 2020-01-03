"""
Project 6
Canvas Analyzer
CS 1064 Introduction to Programming in Python
Fall 2019

Access the Canvas Learning Management System and process learning analytics.

Edit this file to implement the project.
To test your current solution, run the `test_my_solution.py` file.
Refer to the instructions on Canvas for more information.

"I have neither given nor received help on this assignment."
author: DREW PERRY
"""
__version__ = 7
import matplotlib.pyplot as plt
import datetime
# 1) main
def main(user_id):
    import requests
    import canvas_requests
    
    #Initializes variables
    user_info = canvas_requests.get_user(user_id)
    courses = canvas_requests.get_courses(user_id)
    courseIDs = get_course_ids(courses)
    ids = choose_course(courseIDs)
    subs = canvas_requests.get_submissions(user_id, ids)
    
    #Calls functions using variables
    print_user_info(user_info)
    filter_available_courses(courses)
    print_courses(courses)
    summarize_points(subs)
    summarize_groups(subs)
    plot_scores(subs)
    plot_grade_trends(subs)
    
    
# 2) print_user_info
def print_user_info(userDict):
    #Prints user name, title, primary email, and bio
    name = userDict["name"]
    title = userDict["title"]
    email = userDict["primary_email"]
    bio = userDict["bio"]
    print(f"""Name = {name}
Title = {title}
Primary Email = {email}
Bio = {bio}
            """)

    
# 3) filter_available_courses
def filter_available_courses(courseDicts):
    #Returns list of available courses
    available = []
    for course in courseDicts:
        if course["workflow_state"] == "available":
            available.append(course)
    return available

# 4) print_courses
def print_courses(courseDicts):
    #prints course ID followed by name
    for course in courseDicts:
        course_id = course["id"]
        courseName = course["name"]
        print(f"{course_id} : {courseName}")
# 5) get_course_ids
def get_course_ids(courseDicts):
    #returns list of ints (course IDs)
    courseIds = []
    for course in courseDicts:
        courseIds.append(course["id"])
    return courseIds
          
# 6) choose_course
def choose_course(courseIds):
    #get user input and returns ID if valid
    chosenId = int(input('Please input your course ID selection!'))
    while chosenId not in courseIds:
        chosenId = int(input('Please input your course ID selection!'))
    return chosenId
    
# 7) summarize_points
def summarize_points(submissionLists):
    #Summarizes points and prints grade
    obtained = 0
    possPoints = 0
    
    for sub in submissionLists:
        if sub["score"] != None:
            weight = sub["assignment"]["group"]["group_weight"]
            possPoints += sub["assignment"]["points_possible"] * weight
            obtained += sub["score"] * weight
    currGrade = round(obtained / possPoints * 100)
    print(f"""Points possible so far: {possPoints}
Points obtained: {obtained}
Current grade: {currGrade}
                """)                   
# 8) summarize_groups
def summarize_groups(submissions):
    #Summarizes grades by group and prints
    availablePoints = {}
    earnedPoints = {}
    
    for sub in submissions:
        if sub["score"] != None:
            groupName = sub["assignment"]["group"]["name"]
            if groupName not in earnedPoints:
                availablePoints[groupName] = sub["assignment"]["points_possible"]
                earnedPoints[groupName] = sub["score"]
            else:
                availablePoints[groupName] += sub["assignment"]["points_possible"]
                earnedPoints[groupName] += sub["score"]
            for group in availablePoints:
                unweight = str(round((earnedPoints[group]/availablePoints[group]) * 100))
                print(f"{groupName} {unweight}")
                
    
# 9) plot_scores
def plot_scores(subLists):
    #Plots distiburtion of grades
    xValues = []
    for sub in subLists:
        if (sub["score"] != None):
            if (sub["assignment"]["points_possible"] > 0):
                xVal = sub["score"] * 100 / sub["assignment"]["points_possible"]
                xValues.append(xVal)
                
    plt.xlabel("Grades")
    plt.ylabel("Number of Assignments")
    plt.title("Distribution of Grades")
    plt.hist(xValues)
    plt.show()
    
            
# 10) plot_grade_trends
def plot_grade_trends(subLists):
    #Plots grade trend
    maximum,highest,lowest = 0,0,0
    data_max,data_high,data_low,data_dates = [],[],[],[]
    
    for sub in subLists:
        dateDue = sub["assignment"]["due_at"]
        data_dates.append(datetime.datetime.strptime(dateDue, "%Y-%m-%dT%H:%M:%SZ"))
        pointsAvail = sub["assignment"]["points_possible"]
        maxAvail = pointsAvail * sub["assignment"]["group"]["group_weight"] * 100
        maximum += maxAvail
        data_max.append(maximum)
        
        score = 0
        if sub["score"] != None:
            score = sub["score"]
            low = score * sub["assignment"]["group"]["group_weight"] * 100
            high = low
        else:
            low = 0
            high = maxAvail
        lowest += low
        highest += high
        
        data_low.append(lowest)
        data_high.append(highest)
    
    data_max = [value / maximum * 100 for value in data_max]
    data_low = [value / maximum * 100 for value in data_low]
    data_high = [value / maximum * 100 for value in data_high]
    
    #Plots and labels graph
    plt.plot(data_dates, data_max, label = "Maximum")
    plt.plot(data_dates, data_low, label = "Lowest")
    plt.plot(data_dates, data_high, label = "Highest")
    
    plt.title("Grade Trend")
    plt.ylabel("Grade")
    plt.legend()
    plt.show()
    

# Keep any function tests inside this IF statement to ensure
# that your `test_my_solution.py` does not execute it.
if __name__ == "__main__":
    main('hermione')
    # main('ron')
    # main('harry')
    
    # https://community.canvaslms.com/docs/DOC-10806-4214724194
    # main('YOUR OWN CANVAS TOKEN (You know, if you want)')