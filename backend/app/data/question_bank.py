from ..models.question import Question

# Real entry‑level interview questions
QUESTION_BANK = [
    # Python
    Question(
        id="PY001",
        category="Python",
        topic="Lists",
        difficulty="beginner",
        question="How do you reverse a list in Python?",
        expected_concepts=["list slicing", "reverse() method"],
        ideal_answer_points=["Using list[::-1] slicing", "Using list.reverse() method"],
        recommended_material_topics=["Python lists", "list methods"]
    ),
    Question(
        id="PY002",
        category="Python",
        topic="Dictionaries",
        difficulty="beginner",
        question="How can you merge two dictionaries in Python 3.9+?",
        expected_concepts=["dict unpacking"],
        ideal_answer_points=["Using {**dict1, **dict2}"],
        recommended_material_topics=["Python dictionaries"]
    ),
    Question(
        id="PY003",
        category="Python",
        topic="Generators",
        difficulty="intermediate",
        question="What is a generator and how do you create one?",
        expected_concepts=["yield keyword", "lazy evaluation"],
        ideal_answer_points=["Define a function with yield", "Generator expressions"],
        recommended_material_topics=["Python generators", "yield"]
    ),
    # Data Structures & Algorithms
    Question(
        id="DSA001",
        category="DSA",
        topic="Arrays",
        difficulty="beginner",
        question="Explain how to find the maximum subarray sum using Kadane's algorithm.",
        expected_concepts=["linear scan", "dynamic programming"],
        ideal_answer_points=["Maintain current and global max", "Update with max(current+num, num)"],
        recommended_material_topics=["Kadane's algorithm", "Dynamic programming"]
    ),
    Question(
        id="DSA002",
        category="DSA",
        topic="Linked List",
        difficulty="beginner",
        question="How do you detect a cycle in a singly linked list?",
        expected_concepts=["Floyd's Tortoise and Hare"],
        ideal_answer_points=["Two pointers moving at different speeds", "If they meet, a cycle exists"],
        recommended_material_topics=["Linked list cycle detection"]
    ),
    Question(
        id="DSA003",
        category="DSA",
        topic="Sorting",
        difficulty="beginner",
        question="What is the time complexity of quicksort in the average case?",
        expected_concepts=["divide and conquer"],
        ideal_answer_points=["O(n log n)"],
        recommended_material_topics=["Quicksort algorithm"]
    ),
    # DBMS
    Question(
        id="DB001",
        category="DBMS",
        topic="SQL",
        difficulty="beginner",
        question="Write a SQL query to retrieve all records where the salary is greater than 50000.",
        expected_concepts=["SELECT", "WHERE clause"],
        ideal_answer_points=["SELECT * FROM table_name WHERE salary > 50000;"],
        recommended_material_topics=["SQL basics"]
    ),
    Question(
        id="DB002",
        category="DBMS",
        topic="Normalization",
        difficulty="intermediate",
        question="What is the purpose of database normalization?",
        expected_concepts=["eliminate redundancy", "reduce anomalies"],
        ideal_answer_points=["Organize data into tables", "Maintain data integrity"],
        recommended_material_topics=["Database normalization forms"]
    ),
    # Operating Systems
    Question(
        id="OS001",
        category="Operating Systems",
        topic="Processes",
        difficulty="beginner",
        question="Explain the difference between a process and a thread.",
        expected_concepts=["independent execution", "shared memory"],
        ideal_answer_points=["Process has its own memory space", "Threads share process memory"],
        recommended_material_topics=["Process vs thread"]
    ),
    Question(
        id="OS002",
        category="Operating Systems",
        topic="Scheduling",
        difficulty="intermediate",
        question="What is round‑robin scheduling and its typical time‑slice?",
        expected_concepts=["time quantum", "fair sharing"],
        ideal_answer_points=["Each process gets a fixed time slice in circular order", "Typical quantum 10‑100 ms"],
        recommended_material_topics=["CPU scheduling algorithms"]
    ),
    # Computer Networks
    Question(
        id="CN001",
        category="Computer Networks",
        topic="TCP/IP",
        difficulty="beginner",
        question="What is the three‑way handshake in TCP?",
        expected_concepts=["SYN", "SYN‑ACK", "ACK"],
        ideal_answer_points=["Client sends SYN", "Server replies SYN‑ACK", "Client sends ACK"],
        recommended_material_topics=["TCP connection establishment"]
    ),
    Question(
        id="CN002",
        category="Computer Networks",
        topic="HTTP",
        difficulty="beginner",
        question="What is the difference between HTTP GET and POST methods?",
        expected_concepts=["safe vs unsafe", "request body"],
        ideal_answer_points=["GET retrieves data, no body", "POST submits data, includes body"],
        recommended_material_topics=["HTTP methods"]
    ),
    # AI/ML
    Question(
        id="ML001",
        category="AI/ML",
        topic="Supervised Learning",
        difficulty="beginner",
        question="What is the difference between classification and regression?",
        expected_concepts=["output type", "continuous vs categorical"],
        ideal_answer_points=["Classification predicts categories", "Regression predicts continuous values"],
        recommended_material_topics=["Supervised learning types"]
    ),
    Question(
        id="ML002",
        category="AI/ML",
        topic="Overfitting",
        difficulty="intermediate",
        question="How can you reduce overfitting in a machine learning model?",
        expected_concepts=["regularization", "cross‑validation", "more data"],
        ideal_answer_points=["Use L1/L2 regularization", "Apply dropout", "Increase training data", "Early stopping"],
        recommended_material_topics=["Model regularization"]
    ),
    # HR / Behavioral
    Question(
        id="HR001",
        category="HR",
        topic="Teamwork",
        difficulty="beginner",
        question="Tell me about a time you worked successfully in a team.",
        expected_concepts=["collaboration", "communication"],
        ideal_answer_points=["Describe the project", "Your role", "Outcome", "What you learned"],
        recommended_material_topics=["Behavioral interview techniques"]
    ),
    Question(
        id="HR002",
        category="HR",
        topic="Conflict",
        difficulty="beginner",
        question="Describe a conflict you had at work and how you resolved it.",
        expected_concepts=["conflict resolution", "communication"],
        ideal_answer_points=["Situation", "Action taken", "Result", "Reflection"],
        recommended_material_topics=["Conflict resolution"]
    ),
    Question(
        id="HR003",
        category="HR",
        topic="Motivation",
        difficulty="beginner",
        question="Why do you want to work at our company?",
        expected_concepts=["research", "alignment"],
        ideal_answer_points=["Company values", "Career growth", "Specific projects"],
        recommended_material_topics=["Company research"]
    ),
    # Additional technical questions to reach ~30
    Question(
        id="PY004",
        category="Python",
        topic="List Comprehensions",
        difficulty="beginner",
        question="How would you create a list of squares from 1 to 10 using a list comprehension?",
        expected_concepts=["list comprehension syntax"],
        ideal_answer_points=["[x*x for x in range(1,11)]"],
        recommended_material_topics=["Python list comprehensions"]
    ),
    Question(
        id="DSA004",
        category="DSA",
        topic="Binary Search",
        difficulty="intermediate",
        question="Explain the binary search algorithm and its time complexity.",
        expected_concepts=["divide and conquer", "logarithmic time"],
        ideal_answer_points=["Repeatedly split sorted array", "O(log n)"],
        recommended_material_topics=["Binary search"]
    ),
    Question(
        id="DSA005",
        category="DSA",
        topic="Stacks",
        difficulty="beginner",
        question="What is a stack and where would you use it?",
        expected_concepts=["LIFO", "push/pop"],
        ideal_answer_points=["Last‑in‑first‑out structure", "Function call recursion, expression evaluation"],
        recommended_material_topics=["Stack data structure"]
    ),
    Question(
        id="DB003",
        category="DBMS",
        topic="Indexes",
        difficulty="intermediate",
        question="How do indexes improve query performance in a relational database?",
        expected_concepts=["B‑tree", "lookup speed"],
        ideal_answer_points=["Indexes allow faster row location", "Reduce full table scans"],
        recommended_material_topics=["Database indexing"]
    ),
    Question(
        id="OS003",
        category="Operating Systems",
        topic="Deadlock",
        difficulty="intermediate",
        question="What are the four conditions necessary for a deadlock to occur?",
        expected_concepts=["mutual exclusion", "hold and wait", "no preemption", "circular wait"],
        ideal_answer_points=["List the four conditions"],
        recommended_material_topics=["Deadlock"]
    ),
    Question(
        id="CN003",
        category="Computer Networks",
        topic="OSI Model",
        difficulty="beginner",
        question="Name the seven layers of the OSI model.",
        expected_concepts=["layer names"],
        ideal_answer_points=["Physical, Data Link, Network, Transport, Session, Presentation, Application"],
        recommended_material_topics=["OSI model"]
    ),
    Question(
        id="ML003",
        category="AI/ML",
        topic="Unsupervised Learning",
        difficulty="beginner",
        question="What is clustering in unsupervised learning?",
        expected_concepts=["group similar data points"],
        ideal_answer_points=["Algorithm groups data without labels"],
        recommended_material_topics=["Clustering algorithms"]
    ),
    Question(
        id="PY005",
        category="Python",
        topic="Exception Handling",
        difficulty="beginner",
        question="How do you handle exceptions in Python?",
        expected_concepts=["try/except"],
        ideal_answer_points=["Use try block and except clauses"],
        recommended_material_topics=["Python exceptions"]
    ),
    Question(
        id="DSA006",
        category="DSA",
        topic="Hash Tables",
        difficulty="intermediate",
        question="Explain how a hash table resolves collisions.",
        expected_concepts=["chaining", "open addressing"],
        ideal_answer_points=["Separate chaining with linked lists", "Linear probing / quadratic probing"],
        recommended_material_topics=["Hash tables"]
    ),
    Question(
        id="HR004",
        category="HR",
        topic="Strengths",
        difficulty="beginner",
        question="What are your greatest strengths?",
        expected_concepts=["self‑awareness", "relevant to role"],
        ideal_answer_points=["Mention 2‑3 strengths", "Provide examples"],
        recommended_material_topics=["Interview self‑assessment"]
    ),
    Question(
        id="HR005",
        category="HR",
        topic="Weaknesses",
        difficulty="beginner",
        question="What is a weakness you are working to improve?",
        expected_concepts=["growth mindset"],
        ideal_answer_points=["Identify genuine area", "Show steps to improve"],
        recommended_material_topics=["Interview preparation"]
    ),
]
