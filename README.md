# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

I choose the domain of "Professor and Class reviews for UIUC under the Computer Science major", specifically since I would struggle to research all the information neccessary to make a decision on which courses to take. This knowledge is valuable since it consolidates many student experiences into a searchable system the model can interpret and weigh on. This information is difficult to find since official channels only provides course descriptions and instructor pages highlighting the coursework rather than feedback on teaching style or student satisfaction shown on resources like Reddit, Rate My Professor, and community discussion boards.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | cs225_brad_solomon_rate_my_professor.txt | collection of reviews from rate my professor regarding instructor brad solomon within CS225 | documents/cs225_brad_solomon_rate_my_professor.txt |
| 2 | cs225_graham_evans_rate_my_professor.txt | collection of reviews from rate my professor about the instructor Graham Evans within CS225  | documents/cs225_graham_evans_rate_my_professor.txt |
| 3 | cs341_lawrence_angrave_rate_my_professor.txt | collection of reviews from students on rate my professor about instructor Lawrence Angrave who teaches CS231 | documents/cs341_lawrence_angrave_rate_my_professor.txt |
| 4 | cs374_chandra_chekuri_rate_my_professor.txt | collection of reviews from students on rate my professor regarding the teachings of Chandra Chekuri in CS374| documents/cs374_chandra_chekuri_rate_my_professor.txt |
| 5 | cs374_jeff_erickson_rate_my_professor.txt | collection of reviews on rate my professor regarding the teachings of Jeff Erickson from CS374 | documents/cs374_jeff_erickson_rate_my_professor.txt |
| 6 |cs374_tips_reddit_thread.txt | tips on how to succeed in CS374 with many insights only available to a past/current student within a reddit thread | documents/cs374_tips_reddit_thread.txt |
| 7 | cs421_else_gunter_rate_my_professor.txt | collection of reviews on rate my professor regarding the teachings of Elsa Gunter from the CS421 class | documents/cs421_else_gunter_rate_my_professor.txt |
| 8 | cs421_issues_with_class_reddit_thread.txt | A reddit thread speaking on the issues and upsides regarding the teaching within the CS421 course | documents/cs421_issues_with_class_reddit_thread.txt |
| 9 | cs425_distributed_systems_reddit_thread.txt | A reddit thread speaking on the quality of teaching and the benefits from the CS425 course | documents/cs425_distributed_systems_reddit_thread.txt |
| 10 | cs425_distributed_systems_uiucmcs.txt| A UIUC specific community board from the MCS program speaking on the quality of the CS425 course | documents/cs425_distributed_systems_uiucmcs.txt |
|11| cs425_indranil_gupta_rate_my_professor.txt | A collection of reviews from rate my professor regarding the teachings of Indranil Gupta from the CS425 course| documents/ cs425_indranil_gupta_rate_my_professor.txt|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
400 characters

**Overlap:**
20

**Why these choices fit your documents:**
The chunk size is represented as characters since I can take advantage of the average character count from review posts which has an upper range of 300 characters. There are some discrepencies like longer posts or the source url and source type that has to be taken into consideration by making the chunk a bit longer. The overlap isn't too big since most entries in documents types like rate my professor where out of context information like scores can bleed into other chunks and will mislead the model. But larger entries like reddit posts or the MCS discussion still needs some overlap to ensure continuity between sentences within the same paragraph.

**Final chunk count:**
138

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
Largely due to the nature of subjective interpretation within the writing between the different reviews in the documentation, I would prioritize semantic understanding above everything else and get a embedding model that reflects this priority. For this, I would choose text-embedding-3-large from OpenAi since the main focus of this model is prioritizing retrieval quality and since cost is not a constraint, I don't have to choose a cheaper model like the small. In addition to this, multilingual support wouldn't be neccessary since most writing concerning CS courses at UIUC are usually written in english.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
Some structural choices that really helped with accurate chunk retrieval was implimenting the bm25 and semantic hybrid scoring where chunks with keywords located inside the prompt have higher scores in comparison to those who don't. Ensuring that the most accurate and best context chunks were provided to the model. In addition to that, I gave the model a terrible consequence that would befall the user if it didn't strictly use only what is found from the retrieved documents. Since the models' best interest is making the user happy, we essentially give it a core instruction that cannot be measured in hopes for a trade-off and  it cannot ignore due to its' core instruction.

**How source attribution is surfaced in the response:**
In addition to the model strictly relying on the retrieved context and providing support references for its conclusion since otherwise the user would suffer consequences it cannot realistically measure. Clear formatting was utilized where each chunk was listed under the context label meant for generation, so as to avoid any confusion for the model.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the expected weekly committment for the CS425 course at UIUC?| 8-12 hours| Student reviews support the fact that an average of 8.04hrs weekly is best |Partially Relevant  | Accurate |
| 2 | What strengths and weaknesses do students report about the Distributed Systems course?| The course is one of the best courses to take for professional development, it is generally high quality but it has some downsides like exams being too difficult | It is a good introduction to the topic, the professor puts effort into teaching and the course is tough but rewarding, which is both a downside and upside |Relevant | Partially Accurate |
| 3 | What do students say about taking CS421 with Elsa Gunter?| The course is very challenging but there are resources to take advantage, this course will be worth it for those who have a genuine interest in the topic | The course is a tragedy, it is very difficult but Elsa is always helpful and patient to those who want to learn |Relevant | Accurate |
| 4 | Which professor have students had the best learning experiences in CS374 with? | students largely prefer the teaching style of Jeff Erickson and his lectures are the most engaging| students have had the best learning experience with Jeff Erickson |Inaccurate | Accurate |
| 5 | How do student reviews compare between Brad Solomon and Graham Evans? | Student reviews are the most favorable for Brad Solomon | Brad Solomon is known for having enjoyable lecture and having engagine material while Graham is known for being fair with scoring |Relevant | Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professor have students had the best learning experiences in CS374 with? the top chunks returned are not related to the query at all, meanwhile, there are many chunks in the vector database that are better suited for this prompt.


**What the system returned:**
( "Professor: Jeff Erickson\nCourse: CS374\n\nReview Date: Dec 9th, 2020\nQuality: 5.0\nDifficulty: 4.0\nWould Take Again: Yes\nAttendance: Not Mandatory\n\nReview:\n(Fall 2019) Easily the best CS prof at UIUC. His lectures are by far the clearest among all of the theory CS professors. I also love his teaching style of writing scribbles simultaneously while he is teaching instead of just pointing at PowerPoints, this makes note taking and focus during class so much easier. Homework and exams are also reasonable.\n\nTags:\nRespected\nSkip class? You won't pass.\nAmazing lectures", {'source_file': 'cs374_jeff_erickson_rate_my_professor.txt', 'source_url': 'https://www.ratemyprofessors.com/professor/180296', 'source_type': 'RateMyProfessor', 'course': 'CS374'})
--------------------------------------------------------------------------------
( 'Professor: Lawrence Angrave\nCourse: CS241/CS341\n\nReview Date: Dec 27th, 2024\nQuality: 5.0\nDifficulty: 4.0\nAttendance: Mandatory\nWould Take Again: Yes\nGrade: A-\n\n\nReview:\nGreat professor who makes a tough class engaging. Lectures are worth attending, and the free textbook is helpful. Use resources like Unstuck AI and past lectures to stay on top of the material. Overall, a rewarding experience.', {'source_file': 'cs341_lawrence_angrave_rate_my_professor.txt', 'source_url': 'https://www.ratemyprofessors.com/professor/1117293', 'source_type': 'RateMyProfessor', 'course': 'CS341'})
--------------------------------------------------------------------------------
( 'Professor: Lawrence Angrave\nCourse: CS241/CS341\n\nReview Date: Mar 11th, 2025\nQuality: 5.0\nDifficulty: 3.0\nAttendance: Not Mandatory\nWould Take Again: Yes\nGrade: A-\n\n\nReview:\nExtremely passionate professor who clearly loves what he teaches. Dr. Angrave makes lectures very engaging and there are ample resources to learn in the way you want. The MPs can be quite long but office hours are very helpful in getting through them and if you put in the effort to learn you can excel in this class.\n\nTags:\nAmazing lectures\nLots of homework\nAccessible outside class', {'source_file': 'cs341_lawrence_angrave_rate_my_professor.txt', 'source_url': 'https://www.ratemyprofessors.com/professor/1117293', 'source_type': 'RateMyProfessor', 'course': 'CS341'})
--------------------------------------------------------------------------------

According to the provided source, `cs374_jeff_erickson_rate_my_professor.txt`, students have had the best learning experiences in CS374 with Professor Jeff Erickson. The review states: "Easily the best CS prof at UIUC. His lectures are by far the clearest among all of the theory CS professors." (Source: `cs374_jeff_erickson_rate_my_professor.txt`, Review Date: Dec 9th, 2020, https://www.ratemyprofessors.com/professor/180296). This suggests that Professor Jeff Erickson is highly regarded by students for his teaching style and ability to convey complex concepts clearly.

**Root cause (tied to a specific pipeline stage):**
Chunking and Embedding

**What you would change to fix it:**
I've tried to fine tune the model and alter chunking strategies many times so that embedding can be get the semantic context to generate it's best understanding of the chunks, but I haven't had much success. What would greatly help is tying keywords within the chunk to the metadata, this metadata persists even after embedding. When a query happens, the model can then get keywords from the query and retrieval can use said key words to get the best chunk. I've tested a similar approach in another situation and this helped greatly.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec helped me be grounded in my approach while completing the project, where it forced me to evaluate the success of each step along the way and the pipeline.

**One way your implementation diverged from the spec, and why:**
I had to use contact-based chunking which isn't really supported in the spec, but there was a lot of issues with the recursive chunking method and it cutting off information at neccessary times or producing chunks with little information. When the chunking step started to take the format of the Rate My Professor documents into account, it produced chunks with a higher quality and success in embedding.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**
Chatgpt was used for all of these questions

- *What I gave the AI:*
Could you write me a regex so I can locate the source: within the files? I have it how some of the files looked as an example and the diagram to show it that it's a RAG program
- *What it produced:* r"\[source:\s*.*?\]
- *What I changed or overrode:*
Added the parenthesis to add another capture "r"\[source:\s*(.*?)\]" that I can then access using group(1)

**Instance 2**

- *What I gave the AI:* Could you make me a regex that locates "Professor:" within this document? I gave it the a Rate My Professor file as an example.
- *What it produced:* r"Professor:"
- *What I changed or overrode:* r"(?=Professor:)" uses a positive lookahead to avoid consuming the text found, in other words, Professor:


# Sample Chunks

Source: cs225_graham_evans_rate_my_professor.txt

Professor: Graham Evans
Course: CS225

Review Date: Jan 25th, 2025
Quality: 1.0
Difficulty: 3.0
Attendance: Not Mandatory
Grade: Not sure yet

Review:
I took his CS173 and CS225. He canceled the drop for a quiz, added a tutorial section in CS173, and increased the percentage of exams in CS225. In short, he sucks. Btw, he cannot give good lectures. His explanation to CS225 lacks logistics. He cannot even defend his own proof when some students ask questions in CS173.

Tags:
Tough grader
Test heavy
----------------------------------------0----------------------------------------
source: cs425_distributed_systems_uiucmcs.txt

Class: CS 425 - Distributed Systems (Cloud Computing Concepts)
Date: 12/16/2025, 11:34 PM
Estimated Time: 11 hrs/wk

Final Grade: None

This is my favorite class I've taken in the program.
----------------------------------------1----------------------------------------
source: cs421_else_gunter_rate_my_professor.txt

Professor: Elsa Gunter
Course: CS421

Review Date: Dec 8th, 2025
Quality: 1.0
Difficulty: 5.0
Attendance: Not Mandatory
Grade: C

Review:
tests are literal memorization only unless you are an OCAML expert. The lectures cover actual course content abstractly at best. Worst part is that this course content has few viable alternatives to learn from.

Tags:
Test heavy
----------------------------------------2----------------------------------------
source: cs421_else_gunter_rate_my_professor.txt

Professor: Elsa Gunter
Course: CS421

Review Date: Dec 19th, 2025
Quality: 1.0
Difficulty: 4.0
Attendance: Not Mandatory
Grade: B

Review:
I usually only read reviews here, but my experience in this class was frustrating enough to share. The instructor often raised her voice at students, creating an uncomfortable environment. I also felt the material focused on concepts that were not very useful. I did not find this class to be a positive learning experience. Avoid at all costs

Tags:
----------------------------------------3----------------------------------------
source: cs425_indranil_gupta_rate_my_professor.txt

Professor: Indranil Gupta
Course: CS425

Review Date: Aug 27th, 2024
Quality: 5.0
Difficulty: 3.0
Attendance: Not Mandatory
Would Take Again: Yes
Grade: A


Review:
The material and structure of this class was very different from any CS/ECE class here. Full of interesting concepts, Indy is very funny and knowledgeable & teaches clearly. Only downside tests are VERY memorization heavy, just SO many concepts gone over in class. Everyone bombed the final but got curved very generously.

Tags:
Clear grading criteria
Hilarious
Test heavy
----------------------------------------4----------------------------------------

# Retrieved Sample Results

'Conclusion:\nThe course is a good introduction to various topics in Distributed Systems. Indy puts effort into teaching the course and has time for Coursera students on top of the on-campus students he teaches. You will get out of the course what you put into it.', {'source_file': 'cs425_distributed_systems_uiucmcs.txt', 'source_url': 'http://uiucmcs.org/courses/CS-425-Distributed-Systems-(Cloud-Computing-Concepts)', 'source_type': 'UIUC_MCS_Reviews', 'course': 'CS425'}
--------------------------------------------------------------------------------
"All in all a great course, with both tough and rewarding components. If you're in the Online MCS, this class is a must-take.\n\n\n\n\nClass: CS 425 - Distributed Systems (Cloud Computing Concepts)\nDate: 1/20/2025, 7:27 PM\nEstimated Time: 12 hrs/wk\n\nFinal Grade: None", {'source_file': 'cs425_distributed_systems_uiucmcs.txt', 'source_url': 'http://uiucmcs.org/courses/CS-425-Distributed-Systems-(Cloud-Computing-Concepts)', 'source_type': 'UIUC_MCS_Reviews', 'course': 'CS425'}
--------------------------------------------------------------------------------
"Pros: Overall I found this course to be an excellent learning opportunity and addressed a wide range of topics in distributed systems. My sentiments echo what other reviews have stated, mainly that professor Indy was very knowledgeable and had engaging lectures. All of the exams were open-note and unproctored, which was appreciated given the range of topics that the course covered. I can't decide", {'source_file': 'cs425_distributed_systems_uiucmcs.txt', 'source_url': 'http://uiucmcs.org/courses/CS-425-Distributed-Systems-(Cloud-Computing-Concepts)', 'source_type': 'UIUC_MCS_Reviews', 'course': 'CS425'}
--------------------------------------------------------------------------------

Prompt: What strengths and weaknesses do students report about the Distributed Systems course?"

The exact wording asks about the Distributed Systems course and the RAG accurately found some chunks with the necessary semantic knowledge needed to answer the question and also finding chunks strictly about the course. Every chunk here speaks on a students experience within the course and their perceived benefits or struggles regarding the course.

[--------------------------------------------1----------------------------------------------------]


('Professor: Elsa Gunter\nCourse: CS421\n\nReview Date: Oct 11th, 2024\nQuality: 5.0\nDifficulty: 3.0\nWould Take Again: Yes\nAttendance: Not Mandatory\nGrade: A+\n\nReview:\nThe lectures may feel challenging at the start, but it becomes easier once you engage with the material. Elsa is always helpful and patient in answering any questions\n\nTags:\nInspirational', {'source_file': 'cs421_else_gunter_rate_my_professor.txt', 'source_url': 'https://www.ratemyprofessors.com/professor/986195', 'source_type': 'RateMyProfessor', 'course': 'CS421'})
--------------------------------------------------------------------------------
('Professor: Elsa Gunter\nCourse: CS421\n\nReview Date: Nov 18th, 2025\nQuality: 1.0\nDifficulty: 1.0\nAttendance: Not Mandatory\nGrade: A\n\nReview:\nTOTALLY TRAGEDY\n\nTags:', {'source_file': 'cs421_else_gunter_rate_my_professor.txt', 'source_url': 'https://www.ratemyprofessors.com/professor/986195', 'source_type': 'RateMyProfessor', 'course': 'CS421'})
--------------------------------------------------------------------------------
('Professor: Elsa Gunter\nCourse: CS421\n\nReview Date: Nov 13th, 2024\nQuality: 1.0\nDifficulty: 4.0\nAttendance: Not Mandatory\nGrade: B+\n\nReview:\nJust the worst honestly. Makes your try to memorize everything and gives little to no help.\n\nTags:', {'source_file': 'cs421_else_gunter_rate_my_professor.txt', 'source_url': 'https://www.ratemyprofessors.com/professor/986195', 'source_type': 'RateMyProfessor', 'course': 'CS421'})
--------------------------------------------------------------------------------

What do students say about taking CS421 with Elsa Gunter?

Every chunk highlights the students opinion or their experience regarding the course and specifically with aspects aligned with the course instructor, this can be seen easily in the first chunk where compliments towards Elsa Gunter specifically are mentioned. The chunks all look like they would assist the model semantically when answering the prompt from the user.

[-------------------------------------------------2-----------------------------------------------]

(np.float64(0.718169009366783), 'Professor: Graham Evans\nCourse: CS225\n\nReview Date: Jan 25th, 2024\nQuality: 1.0\nDifficulty: 5.0\nAttendance: Not Mandatory\nGrade: Not sure yet\n\nReview:\nlectures are literally awful. how do you lecture with BLANK SLIDES to 900+ people. this impedes my learning heavily and he does not have clear talking points whatsoever. better use of my time to self study out of class, disappointing for such a good cs program at uiuc.\n\nTags:\nExtra Credit\nClear grading criteria\nLots of homework', {'source_file': 'cs225_graham_evans_rate_my_professor.txt', 'source_url': 'https://www.ratemyprofessors.com/professor/2254924', 'source_type': 'RateMyProfessor', 'course': 'CS225'})
--------------------------------------------------------------------------------
(np.float64(0.609501374692823), "Professor: Brad Solomon\nCourse: CS225\n\nReview Date: Dec 25th, 2025\nQuality: 5.0\nDifficulty: 2.0\nWould Take Again: Yes\nGrade: A+\n\nReview:\nI really enjoy Brad's lectures, they're quite engaging and he teaches the material well. The course itself isn't too hard, I think with work you can get through it quite well, especially with 7% extra credit.\n\nTags:\nExtra Credit\nHilarious\nBeware of pop quizzes", {'source_file': 'cs225_brad_solomon_rate_my_professor.txt', 'source_url': 'https://www.ratemyprofessors.com/professor/2873724', 'source_type': 'RateMyProfessor', 'course': 'CS225'})
--------------------------------------------------------------------------------
(np.float64(0.5347355422639952), 'Professor: Graham Evans\nCourse: CS225\n\nReview Date: Mar 9th, 2026\nQuality: 4.0\nDifficulty: 4.0\nAttendance: Not Mandatory\nWould Take Again: Yes\nGrade: A\n\nReview:\nMPs and exams need a lot of effort, but grading is fair.\n\nTags:\nLots of homework\nExtra Credit', {'source_file': 'cs225_graham_evans_rate_my_professor.txt', 'source_url': 'https://www.ratemyprofessors.com/professor/2254924', 'source_type': 'RateMyProfessor', 'course': 'CS225'})
--------------------------------------------------------------------------------

#Example Response

Query: How do student reviews compare between Brad Solomon and Graham Evans?

According to the provided reviews, student feedback on Brad Solomon and Graham Evans for CS225 is vastly different. 

Brad Solomon has a 5.0 quality rating with one reviewer stating, "I really enjoy Brad's lectures, they're quite engaging and he teaches the material well" (source: cs225_brad_solomon_rate_my_professor.txt, source_url: https://www.ratemyprofessors.com/professor/2873724). In contrast, Graham Evans has a 1.0 quality rating with a reviewer stating, "lectures are literally awful. how do you lecture with BLANK SLIDES to 900+ people. this impedes my learning heavily and he does not have clear talking points whatsoever" (source: cs225_graham_evans_rate_my_professor.txt, source_url: https://www.ratemyprofessors.com/professor/2254924).

Additionally, another review for Graham Evans has a 4.0 quality rating, with the reviewer stating, "MPs and exams need a lot of effort, but grading is fair" (source: cs225_graham_evans_rate_my_professor.txt, source_url: https://www.ratemyprofessors.com/professor/2254924). 

In terms of difficulty, Brad Solomon's CS225 has a 2.0 difficulty rating, while Graham Evans' has a 5.0 difficulty rating in one review and a 4.0 difficulty rating in another (source: cs225_brad_solomon_rate_my_professor.txt and cs225_graham_evans_rate_my_professor.txt).

It is worth noting that both instructors offer extra credit, but only Brad Solomon is described as "Hilarious" (source: cs225_brad_solomon_rate_my_professor.txt). Graham Evans' course is described as having "Lots of homework" in both reviews (source: cs225_graham_evans_rate_my_professor.txt).

References:
- cs225_brad_solomon_rate_my_professor.txt
- cs225_graham_evans_rate_my_professor.txt
- https://www.ratemyprofessors.com/professor/2873724
- https://www.ratemyprofessors.com/professor/2254924

#Query: What do students say about the quality of the course of CS425?

According to the provided text from the source "cs425_distributed_systems_uiucmcs.txt" and source_url "http://uiucmcs.org/courses/CS-425-Distributed-Systems-(Cloud-Computing-Concepts)", students report the following strengths about the Distributed Systems course:

* The course is a "good introduction to various topics in Distributed Systems" (source: cs425_distributed_systems_uiucmcs.txt)
* The instructor, Indy, "puts effort into teaching the course" and is "very knowledgeable" with "engaging lectures" (source: cs425_distributed_systems_uiucmcs.txt)
* The exams are "open-note and unproctored", which is appreciated given the range of topics covered (source: cs425_distributed_systems_uiucmcs.txt)
* The course has both "tough and rewarding components" (source: cs425_distributed_systems_uiucmcs.txt)

As for weaknesses, the text does not explicitly mention any significant weaknesses. However, it does mention that "You will get out of the course what you put into it" (source: cs425_distributed_systems_uiucmcs.txt), implying that the course may require a significant amount of effort and dedication from the student.

Textual evidence:
* "The course is a good introduction to various topics in Distributed Systems." (source: cs425_distributed_systems_uiucmcs.txt)
* "Indy puts effort into teaching the course and has time for Coursera students on top of the on-campus students he teaches." (source: cs425_distributed_systems_uiucmcs.txt)
* "All of the exams were open-note and unproctored, which was appreciated given the range of topics that the course covered." (source: cs425_distributed_systems_uiucmcs.txt)
* "You will get out of the course what you put into it." (source: cs425_distributed_systems_uiucmcs.txt)

Reference: cs425_distributed_systems_uiucmcs.txt, http://uiucmcs.org/courses/CS-425-Distributed-Systems-(Cloud-Computing-Concepts)

#Query: Which professors are known among students for their ability to skateboard? 

I do not know which professor is known for their skateboarding ability among students. The provided sources (cs425_distributed_systems_uiucmcs.txt, cs374_jeff_erickson_rate_my_professor.txt, cs425_indranil_gupta_rate_my_professor.txt) do not mention any information about professors' skateboarding abilities. 

Reference:
- cs425_distributed_systems_uiucmcs.txt
- cs374_jeff_erickson_rate_my_professor.txt
- cs425_indranil_gupta_rate_my_professor.txt 

Source URL:
- http://uiucmcs.org/courses/CS-425-Distributed-Systems-(Cloud-Computing-Concepts)
- https://www.ratemyprofessors.com/professor/180296
- https://www.ratemyprofessors.com/professor/831224 

Note: The provided sources only contain information about professors' teaching styles, course difficulty, and student reviews, but do not mention any information about their personal interests or skills, such as skateboarding.