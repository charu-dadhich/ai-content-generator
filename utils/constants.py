class Constant:
    response_messages = {
        500: "Internal server error.",
        501: "The requested API endpoint is not valid.",
        502: "The provided data is not in a valid JSON format.",
        503: "The 'Content-Type' header should be set to 'application/json'.",
        504: "User authentication failed.",
        505: "The requested HTTP method is not allowed.",
        506: "Sorry, you are not authorized to perform this action.",
        507: "Invalid parameter value provided.",
        508: "Required parameter or value is missing.",
        509: "User access token is expired or invalid.",
        510: "Your daily quota has been exhausted. Please try again later.",

        100: "Done sucessfully!",
        101: "Email does not exists!",
        102: "Login Successfull!",
        103: "Password is incorrect!",
        104: "Password changed successfully",
        105: "New Password cannot be same as the old password",
        106: "New password and confirm password do not match!",
        107: "Password should contain minimum 8 characters",
        108: "Password should contain at least a digit",
        109: "Password should contain at least an uppercase character",
        110: "Password should contain at least a lowercase character",
        111: "Password should contain at least on special character like [ ()[\]{}|\\`~!@#$%^&*_\-+=;:\"',<>./?]",
        112: "Old Password is not correct!",

        151: "Below is the list of all services.",
        152: "The standard id is invalid",
        153: "The subject id is invalid",
        154: "Below is the list of all chapters.",
        155: "The board id is invalid",
        156: "Below is the list of boards.",
        157: "Below is the list of all grades.",
        158: "Below is the list of all subjects in the mentioned grade.",
        159: "The question paper with this id does not exists.",
        160: "The question with this id does not exists.",
        161: "The prompt with this id does not exists.",
        162: "The questions are regenerated successfully.",
        163: "The regeneration data is missing.",
        164: "The chapter id is invalid",
        165: "Got some missing values",
        166: "The file input is missing.",
        167: "Try it after sometime",
        168: "The service type id is invalid",
        169: "The service type id sent is not correct according to service",
        170: "Please try again",

        171: "Learning Objective created successfully!",
        172: "Please enter number_of_lo key, if generating custom type LO.",
        173: "Number of learning objectives should be greater than 0 and less than 11",
        174: "Learning Objective with this id is not found.",
        175: "Learning Objective updated successfully!",

        181: "The activity is created successfully!",
        182: "The activity is changed successfully!",
        183: "The activity id is not found.",
        184: "Please send activity_time_in_mins, if generating for custom type.",
        185: "Activity time should be greater than 4 and less than 61.",

        191: "Something went wrong. Try again.",
        192: "Questions created successfully!",
        193: "Below is the list of question types.",
        194: "File content is not correct"
    }

    GENERAL_QUESTIONS_FORMAT=  ''' * For Assertion and Reason 

        There are two statements marked as Assertion (A) and Reason (R). Mark your answer as per the codes provided below:  

        Assertion (A): an assertion (a statement or claim) 

        Reason(R): a reason (an explanation or justification) 

        a) Both (A) and (R) are true and (R) is the correct explanation of (A). 

        b) Both (A) and (R) are true, but (R) is not the correct explanation of (A).  

        c) (A) is true but (R) is false.  

        d) (A) is false but (R) is true. 

        

        * For Case-based Questions 

        Case-based or case studies or scenario-based questions, are open-ended inquiry-based questions that present a real-world or hypothetical situation for students to analyse, interpret, and solve. These questions require students to apply their knowledge, think critically, and make informed decisions based on the given context. They are designed to assess a student's ability to connect theory to practice and to develop problem-solving and analytical skills.  

        

        Source for paragraphs of Case Study:  

        - Direct paragraphs from the textbook to be avoided (or needs to be paraphrased) 

        - Paragraphs related to the concept but taken from external sources can be used 

        - Language to be kept grade appropriate 

        

        Real-world or hypothetical scenarios: 

        They present situations that students might encounter in real life or within a specific field of study.  

        Open-ended and complex: 

        They require students to go beyond simple recall and apply their knowledge to solve a problem or involve decision making.  

        Focus on application and analysis: 

        They assess a student's ability to analyze information, identify key issues, develop solutions, and justify their reasoning.  

        Emphasis on critical thinking: 

        They encourage students to evaluate different perspectives, consider multiple factors, and make informed judgments.  

        Development of problem-solving skills: 

        They provide opportunities for students to practice their problem-solving abilities in a practical context.  

        

        * For Source-based Question 

        Source-based questions are questions that require you to analyse and interpret information presented in a specific source, such as a text, image, or document, to answer the question. These questions test your ability to understand the source, place it in its historical context, and potentially identify bias or reliability.  

        Focus on the source: 
        The core of the question lies in understanding the provided source, whether it's a written passage, image, or other material.  

        Interpretation and analysis: 
        You need to go beyond simply understanding the literal meaning of the source and analyse its content, message, and potential biases.  

        Contextualization: 
        It's crucial to understand the historical or social context in which the source was created to fully grasp its meaning.  

        Critical evaluation: 
        You may need to assess the reliability and usefulness of the source, potentially comparing it with other sources or your own knowledge.  

        Higher-order thinking: 
        Source-based questions often require you to move beyond basic recall and engage in critical thinking, analysis, and evaluation.  

        

        * For Statement-based Questions (Objective) 

        Statement I: Often introduces a fact or a general idea. 

        Statement II: Expands on Statement I, providing reasoning, evidence, or contrasting perspectives. 

        

        Answer Choices: 

        (A) Statement I is correct, and Statement II is incorrect. 

        (B) Statement I is incorrect, and Statement II is correct. 

        (C) Both statements are incorrect. 

        (D) Both statements are correct. 

        

        Skills Assessed: 

        Knowledge: Understanding of the facts presented. 

        Analysis: Judging whether the two statements support or contradict each other. 

        Evaluation: Determining the correctness and relationship between statements. 

        

        Statement and Conclusion: 

        These questions present a statement and ask you to determine which conclusion logically follows from it.  

        Statement and Assumption: 

        A statement is given, and you must identify the underlying assumption(s) that the statement relies on.  

        Statement and Argument: 

        A statement is presented, followed by arguments for or against it. You must assess the strength or validity of these arguments.  

        Statement and Course of Action: 

        A situation is described as a statement, and you need to determine the appropriate course of action to address it.  

        

        * For Paragraph-based Questions 

        Paragraph-based questions are questions that require you to understand and interpret information presented in a given paragraph to answer them. These questions assess your reading comprehension, ability to extract specific information, and potentially your ability to infer, summarise, or evaluate information from the text.  

        

        Based on a Passage: 

        The questions are directly linked to a specific paragraph or passage of text.  

        Requires Comprehension: 

        You need to understand the meaning of the paragraph to answer the questions correctly.  

        May Involve Inference: 

        Some questions may require you to go beyond what's explicitly stated and draw conclusions based on the text.  

        Can Test Different Skills: 

        They can test your ability to identify the main idea, find specific details, understand vocabulary in context, or summarize the paragraph.  

        

        

        * For Fill-in the blanks 

        A fill-in-the-blank question is a type of assessment question where a statement, sentence, or paragraph is presented with a blank space where the learner must supply the missing word or phrase. It tests the learner's ability to recall and apply specific knowledge, often focusing on vocabulary, concepts, or factual information.  

        

        Structure: 

        A fill-in-the-blank question consists of a sentence, paragraph, or other text with one or more blanks.  

        Purpose: 

        It assesses the learner's understanding and recall of information by requiring them to fill in the missing words or phrases.  

        

        

        *For Application-based Questions 

        Application-based questions, also known as practical or situational questions, assess a person's ability to apply knowledge and skills to real-world scenarios. Instead of testing recall of facts, these questions require analyzing information, solving problems, and demonstrating practical understanding. They are used to evaluate how well individuals can use concepts in context.  

        

        Focus on Application: 

        They emphasise using learned information to address specific situations or problems, rather than just reciting facts.  

        Real World Scenarios: 

        Application-based questions often present scenarios that mirror situations encountered in practical settings, like a business problem or a medical case.  

        Problem-Solving Skills: 

        They require critical thinking, analysis, and the ability to devise solutions based on the information given.  

        Higher-Order Thinking: 

        They encourage deeper understanding and application of knowledge beyond rote memorisation.  

        

        * For Short-Answer Questions 

        A short answer question is a type of question that requires a concise, focused response, typically one or a few sentences, demonstrating a specific understanding of a topic. These questions assess recall of facts, definitions, or key points, and are commonly used in assessments to test basic knowledge.  

        

        Concise and Focused: 

        Short answer questions demand a direct and to-the-point answer, avoiding unnecessary elaboration or irrelevant information.  

        Assessment Type: 

        They are frequently used in examinations and assessments to gauge a student's understanding of specific concepts or information.  

        Knowledge Recall: 

        Short answer questions primarily test the ability to recall and articulate specific facts, definitions, or key points from course material.  

        Not for Complex Reasoning: 

        While useful for assessing basic knowledge, short answer questions are generally not suitable for measuring complex analytical or reasoning abilities.  

        

        * For Long Answer Questions 

        Long answer questions, also known as written response/ subjective questions, are open-ended questions that require detailed, multi-sentence or paragraph-length answers. They differ from short answer questions or multiple-choice questions, which typically have concise, factual answers. Long answer questions are designed to assess a student's understanding of a topic, their ability to formulate arguments, and their capacity to express themselves in writing.  

        

        Open-ended: 

        They don't have a single, correct answer, allowing for different interpretations and perspectives.  

        Requires detailed responses: 

        Answers should be well-developed and may involve explanations, analysis, or arguments.  

        Focus on understanding and expression: 

        They assess not only knowledge but also the ability to communicate that knowledge effectively.  

        Often essay-style: 

        Many long answer questions require students to write an essay-like response, potentially with an introduction, body paragraphs, and conclusion.  

        May involve calculations or analysis: 

        Some long answer questions may require mathematical calculations or in-depth analysis to arrive at a solution.  

        

        

        Writing-Skill Questions 

        1. Extend or reinterpret a theme, character, or idea from a literary text.   

        2. Express differing viewpoints using a creative or structured format (different writing formats e.g., dialogue, letter, article, diary, debate).   

        3. Include reasoned opinions, emotional depth, or moral reflection. 

        4.  Follow a real-world or literary situation relevant to the story or poem. 

        

        To keep in mind: 

        1. Realistic Context: The question builds on a literary concept and extends it into a real-life, relatable discussion format, promoting engagement. 

        2. Divergent Thinking & Perspective-Taking: Encourages students to explore opposing viewpoints, which is essential for building empathy and critical reasoning. 

        3. Skill Integration: Various All kinds of writing skills to be covered 

        - Dialogue Writing   

        - Argumentative Writing   

        - Perspective Shifting   

        - Theme Exploration   

        - Emotional Expression   

        - Literary Integration   

        4. Balanced Tone & Length: The conversation is age-appropriate and reflective of Grade group comprehension and language levels. 

        5. Emotional and Thematic Depth: It explores psychological and social themes, aligning with CBSE’s emphasis on value-based learning. 

        

        * For Parallel-based Question 

        Strengths of the Question Format 

        1. Higher-Order Thinking: The question goes beyond simple comprehension, prompting students to compare and contrast themes, tone, and symbolism across two poems. This aligns with Bloom’s Taxonomy levels: Analysis & Evaluation. 

        2. Intertextual Engagement: By connecting two different chapters, students are encouraged to explore the author’s recurring themes and literary choices, improving literary appreciation and synthesis skills. 

        3. Emphasis on Emotional and Thematic Understanding: The model answer highlights how the poet uses emotions and nature as metaphors to reflect human experience. This strengthens moral reasoning and emotional intelligence, key aspects of CBSE’s competency-based learning. 

        4. Clarity and Language: The vocabulary and sentence structure are age-appropriate, modelling clarity, coherence, and structured argumentation for Grade 10 students. 

        5. Balanced Tone and Insight: The answer reflects thoughtful interpretation, drawing clear parallels while also respecting the distinct mood and message of each poem. 

        

        Parallel Question Requirement 

        1. Analyse two related texts (poems, prose pieces, characters, or themes). 

        2. Identify common threads, such as emotions, symbols, messages, or the author’s use of nature, society, or conflict. 

        3. Explore contrasts in tone, message, or perspective between the two texts. 

        4. Reflect on the author's purpose, and how these similarities or differences deepen understanding. 

        5. Use age-appropriate vocabulary and literary terms (e.g., tone, metaphor, theme, symbolism). 

        

        * For Reference to Context  

        Reference to context questions ask you to analyze a specific part of a text and explain its meaning or significance within the larger work. These questions typically involve identifying the speaker, the audience, the situation, and the impact of the passage on the characters or the overall narrative.  

        

        Format of RTC Questions 

        i. A quoted excerpt or passage from the text. 

        ii. A set of questions related to the passage, such as: 

        - Who is the speaker/author? 

        - What is the context of these lines? 

        - What do these lines mean or imply? 

        - Which literary devices are used, and what effect do they have? 

        - How does this passage contribute to the overall theme or message of the text? 

        

        * For Statement-based Question (Subjective) 

        Question Structure: 

        1. Start with a quoted line or excerpt from the text. 

        2. Ask the student to: 

        3. Interpret the line in their own words. 

        4. Identify and explain any figurative language or literary device. 

        5. Connect it to themes, character development, or the author's intent. 

        6. Relate the idea to broader human experiences or emotions, where relevant. 

        

        Competency Targets: 

        1. Interpretation 

        2. Evaluation 

        3. Critical Thinking 

        4. Literary Analysis 

        5. Emotional and Thematic Insight 
        
        
        Distribute Bloom’s taxonomy levels across the question types as follows:
        - Multiple Choice and Fill in the Blanks: Remember / Understand / Apply
        - Short Answer: Apply / Analyse
        - Long Answer: Apply / Analyse / Evaluate

        Important:
        Keep the questions level considerably higher for grades like 9, 10, 11, 12 than the lower grades.
    '''

    K5_SKILL_ASSESSMENT_PROMPTS = '''
        For K-5 (All subjects) 

        - Here is a list of Skill on which questions are to be created. 
            The assessment skills and thinking skills under Bloom’s Taxonomy. 
            a. Remembering, 
            b. Understanding 
            c. Applying 
            d. Analysing 
            e. Evaluating 
        - DO NOT take any reference for the scenario or the type of question directly from the book 
    '''

    SKILL_ASSESSMENT_HINDI = '''
        - Always appropriately mark the blooms taxonomy parameters against each question as per the Hindi subject along with their English names. 

        - Each question should be in Hindi. Follow the Hindi Manak rules and Chandrabindu/Anusvar rules for Hindi writing. 
    '''

    SKILL_ASSESSMENT_ACCOUNTS = '''
        - Use only rupee symbol strictly 

        - To solve the problem, use proper accounting table format for grade XI and XII (when required) 

        - While solving the problem, use the formula for better understanding. 
    '''


class Choice:
    GENDER_TYPE = [
        ('F', "Female"),
        ('M', "Male"),
    ]

    PAPER_TYPE = [
        ("S", "Subjective"),
        ("O", "Objective"),
        ("SO", "Hybrid"),
    ]

    QUESTION_TYPE = [
        ("objective 1 mark", "Objective one mark"),
        ("subjective 1 mark", "Subjective one mark"),
        ("subjective 2 mark", "Subjective two mark"),
        ("subjective 4 mark", "Subjective four mark"),
        ("case based", "Case Based")
    ]

    DIFFICULTY_LEVEL = [
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("difficult", "Difficult"),
        ("very challenging", "Very Challenging")
    ]

    GENERATION_TYPE = [
        ("auto", "Auto"),
        ("custom", "Custom"),
    ]

    ACTIVITY_TYPE = [
        ("classroom", "Classroom"),
        ("meta_cognitive", "Meta Cognitive")
    ]

    # PROMPT_TYPE = [
    #     ("Learning Objectives"),
    #     ("Diagnostic Assessement"),
    #     ("Progressive Practice Section")
    #     ("Practice Interactives")
    #     ("Assignments")
    #     ("Worksheets")
    #     ("NCERT Solutions")
    #     ("Mutiple Choice Questions")
    #     ("Subjective Questions")
    #     ("Higher Order Thinking Skills")
    #     ("Case Study/ Case based")
    #     ("Competency based Questions")
    #     ("Chapter End Test")
    #     ("NCERT Assessments")
    # ]