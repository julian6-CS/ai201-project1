# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
I choose the domain of "Professor and Class reviews for UIUC under the Computer Science major", specifically since I would struggle to research all the information neccessary to make a decision on which courses to take. This knowledge is valuable since it consolidates many student experiences into a searchable system the model can interpret and weigh on. This information is difficult to find since official channels only provides course descriptions and instructor pages highlighting the coursework rather than feedback on teaching style or student satisfaction shown on resources like Reddit, Rate My Professor, and community discussion boards.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
400 characters

**Overlap:**
20

**Reasoning:**
The chunk size is represented as characters since I can take advantage of the average character count from review posts which has an upper range of 300 characters. There are some discrepencies like longer posts or the source url and source type that has to be taken into consideration by making the chunk a bit longer. The overlap isn't too big since most entries in documents types like rate my professor where out of context information like scores can bleed into other chunks and will mislead the model. But larger entries like reddit posts or the MCS discussion still needs some overlap to ensure continuity between sentences within the same paragraph.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2 via sentence-transformers

**Top-k:**
Top three chunks per query

**Production tradeoff reflection:**
Largely due to the nature of subjective interpretation within the writing between the different reviews in the documentation, I would prioritize semantic understanding above everything else and get a embedding model that reflects this priority. For this, I would choose text-embedding-3-large from OpenAi since the main focus of this model is prioritizing retrieval quality and since cost is not a constraint, I don't have to choose a cheaper model like the small. In addition to this, multilingual support wouldn't be neccessary since most writing concerning CS courses at UIUC are usually written in english.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What is the expected weekly committment for the CS425 course at UIUC?| 8-12 hours|
| 2 | What strengths and weaknesses do students report about the Distributed Systems course?| The course is one of the best courses to take for professional development, it is generally high quality but it has some downsides like exams being too difficult |
| 3 | What do students say about taking CS421 with Elsa Gunter?|  The course is very challenging but there are resources to take advantage, this course will be worth it for those who have a genuine interest in the topic |
| 4 | Which professor have students had the best learning experiences in CS374 with? | students largely prefer the teaching style of Jeff Erickson and his lectures are the most engaging|
| 5 | How do student reviews compare between Brad Solomon and Graham Evans? | Student reviews are the most favourable for Brad Solomon |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. There is some inconsistency where the rate my professor reviews are much shorter in comparison to longer discussions like reddit threads or the MCS community board, making chunking a bit more difficult to fine tune so there is an equal amount of tradeoff between the different documents.

2. There might be some more issues regarding embedding since document types like the Rate My Professor documents have keywords and scorings that could influence the embedding model too much. For example, the inclusion of entries like "Tags" which due to its' strong wording can influence how the chunk is interpreted semantically.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
