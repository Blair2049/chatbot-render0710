GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["stakeholder", "event"]

PROMPTS['entity_extraction'] = """-Goal-
Given the provided text, extract a relationship graph representing stakeholders and their interactions based on relevant events.
Use {language} as output language.

-Steps-
1. Identify all stakeholders, interacted stakeholders, and relevant events as entities. For each identified entity, extract the following information:
- entity_name: The stakeholder's name, or the relevant events' name.
- entity_type: One of the following types: [{entity_types}]. The entities of stakeholders should be of type "stakeholder", the entities of relevant events should be of type "event". Ignore other types.
- entity_description: Comprehensive description of the entity's attributes and activities based on the provided text.
Format each node as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
**Important Rules for Relationships**:
- A "stakeholder" and another "stakeholder" cannot be directly connected. Any relationship between a "stakeholder" and another "stakeholder" must pass through a relevant "event" entity. Specifically:
  - A "stakeholder" may be related to an "event".
  - An "event" may be related to another "stakeholder".
- Direct relationships between "stakeholder" and another "stakeholder" are not allowed.

For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [stakeholder, event]
Text:
At Beach, safety is our number one priority. The marine vessels contracted by Beach will operate in accordance with Australian Maritime Standards, regulated by the Australian Maritime Safety Authority (AMSA).

Notices to Mariners (NTM) will be issued by the Australian Hydrographic Office requesting that vessels do not approach closer than 2 nautical miles of the assessment vessel.

Joint Rescue Coordination Centre (JRCC) for promulgation of radio-navigation warnings at least 24–48 hours before operations commence.

Australian Hydrographic Office no less than four working weeks before operations, who govern Notice to Mariners.
################
Output:
("entity"{tuple_delimiter}"Australian Marine Safety Authority (AMSA)"{tuple_delimiter}"stakeholder"{tuple_delimiter}"A key organization responsible for marine safety."){record_delimiter}
("entity"{tuple_delimiter}"Joint Rescue Coordination Centre (JRCC)"{tuple_delimiter}"stakeholder"{tuple_delimiter}"Joint Rescue Coordination Centre, a coordinating body for maritime rescue."){record_delimiter}
("entity"{tuple_delimiter}"Australian Hydrographic Office"{tuple_delimiter}"stakeholder"{tuple_delimiter}"An office governing navigational charts and maritime notices."){record_delimiter}
("entity"{tuple_delimiter}"JRCC for promulgation of radio-navigation warnings at least 24–48 hours before operations commence. Australian Hydrographic Office no less than four working weeks before operations, who govern Notice to Mariners."{tuple_delimiter}"event"{tuple_delimiter}"Impact on maritime navigation and safety."){record_delimiter}
("relationship"{tuple_delimiter}"Australian Marine Safety Authority (AMSA)"{tuple_delimiter}"JRCC for promulgation of radio-navigation warnings at least 24–48 hours before operations commence. Australian Hydrographic Office no less than four working weeks before operations, who govern Notice to Mariners."{tuple_delimiter}"AMSA is responsible for coordinating maritime safety and relies on this event for timely navigation warnings and notices."{tuple_delimiter}"maritime safety, navigation standards, stakeholder coordination"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"JRCC for promulgation of radio-navigation warnings at least 24–48 hours before operations commence. Australian Hydrographic Office no less than four working weeks before operations, who govern Notice to Mariners."{tuple_delimiter}"Joint Rescue Coordination Centre (JRCC)"{tuple_delimiter}"JRCC ensures maritime safety by issuing radio-navigation warnings in coordination with the event."{tuple_delimiter}"navigation warnings, maritime rescue, safety coordination"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"JRCC for promulgation of radio-navigation warnings at least 24–48 hours before operations commence. Australian Hydrographic Office no less than four working weeks before operations, who govern Notice to Mariners."{tuple_delimiter}"Australian Hydrographic Office"{tuple_delimiter}"The Australian Hydrographic Office governs navigational notices and coordinates with the event to ensure maritime safety."{tuple_delimiter}"navigation notices, maritime safety, operational coordination"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"marine safety, navigation warnings, maritime rescue, stakeholder interaction"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [stakeholder, event]
Text:
24, 08, 2021, Department of Agriculture, Water and the Environment (DAWE) (Biosecurity) advised Santos by email Dorado Development Offshore Project Proposal is on the National Offshore Petroleum Safety and Environmental Management Authority (NOPSEMA) website for public comment. 

Consultation Summary: No objections were raised. Santos has addressed feedback received regarding consulting with relevant fisheries (Section 9.1.3). As per Section 9.1.4 Santos will continue to provide Dorado Development updates.
#############
Output:
("entity"{tuple_delimiter}"Department of Agriculture, Water and the Environment (DAWE) (Biosecurity)"{tuple_delimiter}"stakeholder"{tuple_delimiter}"Department of Agriculture, Water and the Environment (Biosecurity)."){record_delimiter}
("entity"{tuple_delimiter}"NOPSEMA"{tuple_delimiter}"stakeholder"{tuple_delimiter}"National Offshore Petroleum Safety and Environmental Management Authority"){record_delimiter}
("entity"{tuple_delimiter}"Santos"{tuple_delimiter}"stakeholder"{tuple_delimiter}"Santos WA Northwest Pty Ltd, the operator of Dorado Development Offshore Project Proposal."){record_delimiter}
("entity"{tuple_delimiter}"Public"{tuple_delimiter}"stakeholder"{tuple_delimiter}"The public comments."){record_delimiter}
("entity"{tuple_delimiter}"DAWE (Biosecurity) advised Santos by email that Dorado Development Offshore Project Proposal is on the NOPSEMA website for public comment. Consultation Summary: No objections were raised. Santos has addressed feedback received regarding consulting with relevant fisheries. Santos will continue to provide Dorado Development updates."{tuple_delimiter}"event"{tuple_delimiter}"NOPSEMA informed the public about the Dorado Development Offshore Project Proposal, receiving no objections, while Santos addressed fisheries-related feedback and committed to providing project updates."){record_delimiter}
("relationship"{tuple_delimiter}"Department of Agriculture, Water and the Environment (DAWE) (Biosecurity)"{tuple_delimiter}"DAWE (Biosecurity) advised Santos by email that Dorado Development Offshore Project Proposal is on the NOPSEMA website for public comment. Consultation Summary: No objections were raised. Santos has addressed feedback received regarding consulting with relevant fisheries. Santos will continue to provide Dorado Development updates."{tuple_delimiter}"Notified Santos about the public comment process and provided consultation oversight."{tuple_delimiter}"regulatory process, public consultation, feedback"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"DAWE (Biosecurity) advised Santos by email that Dorado Development Offshore Project Proposal is on the NOPSEMA website for public comment. Consultation Summary: No objections were raised. Santos has addressed feedback received regarding consulting with relevant fisheries. Santos will continue to provide Dorado Development updates."{tuple_delimiter}"NOPSEMA"{tuple_delimiter}"Facilitated public consultation and hosted the proposal on its website."{tuple_delimiter}"facilitation, public consultation, website hosting"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"DAWE (Biosecurity) advised Santos by email that Dorado Development Offshore Project Proposal is on the NOPSEMA website for public comment. Consultation Summary: No objections were raised. Santos has addressed feedback received regarding consulting with relevant fisheries. Santos will continue to provide Dorado Development updates."{tuple_delimiter}"Santos"{tuple_delimiter}"Addressed fisheries-related feedback and committed to providing updates."{tuple_delimiter}"feedback resolution, commitment, fisheries consultation"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"DAWE (Biosecurity) advised Santos by email that Dorado Development Offshore Project Proposal is on the NOPSEMA website for public comment. Consultation Summary: No objections were raised. Santos has addressed feedback received regarding consulting with relevant fisheries. Santos will continue to provide Dorado Development updates."{tuple_delimiter}"Public"{tuple_delimiter}"Provided feedback through public consultation."{tuple_delimiter}"public feedback, consultation process, transparency"{tuple_delimiter}6){record_delimiter}
("content_keywords"{tuple_delimiter}"public consultation, fisheries feedback, project updates, regulatory notification"){completion_delimiter}

#############################""",
    """Example 3:

Entity_types: [stakeholder, event]
Text:
CAPL engaged Department of Biodiversity, Conservation and Attractions (DBCA) as part of their ongoing relationship and to conduct engagement for the OPP. CAPL provided a formal written notice of the Gorgon Gas Development: Backfill Fields OPP via email and invited DBCA to consult on the Development.

DBCA provided a written response that identified:

- ecologically important areas within the vicinity of proposed operations, including the Barrow Island Marine Park and the Barrow Island Nature Reserve  
- the requirement to establish appropriate baseline survey data on the current state of areas supporting important ecological values and any current contamination if present within the area of potential impact of hydrocarbon releases  
- requirements for emergency management including, recommendations for information acquisition to support a before-after, control-impact (BACI) framework, notification requirement and clean-up expectations in the event of an oil spill  
- the following guidance documents for CAPL to refer to:  
   - National Light Pollution Guidelines for Wildlife Including Marine Turtles, Seabirds, and Migratory Shorebirds  
   - Offshore Petroleum Industry Guidance Note of September 2018 titled *Marine Oil Pollution: Response and Consultation Arrangements*  
   - DoT web content regarding marine pollution requirements for consultation.  

CAPL responded to DBCA indicating that the values of ecologically important areas had been considered in the development of the OPP. CAPL also confirmed that spill response and monitoring requirements would be assessed and addressed in subsequent activity-specific EPs.  
#############
Output:
("entity"{tuple_delimiter}"Department of Biodiversity, Conservation and Attractions (DBCA)"{tuple_delimiter}"stakeholder"{tuple_delimiter}"A department responsible for biodiversity, conservation, and attractions, including marine and coastal ecosystem protection."){record_delimiter}
("entity"{tuple_delimiter}"CAPL"{tuple_delimiter}"stakeholder"{tuple_delimiter}"Chevron Australia Pty Ltd (CAPL). The operator of the Gorgon Gas Development, one of Australia's largest natural gas projects located off the northwest coast of Western Australia."){record_delimiter}
("entity"{tuple_delimiter}"Barrow Island Marine Park"{tuple_delimiter}"stakeholder"{tuple_delimiter}"A marine park involved in marine and coastal ecosystem protection."){record_delimiter}
("entity"{tuple_delimiter}"Barrow Island Nature Reserve"{tuple_delimiter}"stakeholder"{tuple_delimiter}"A nature reserve contributing to ecosystem conservation."){record_delimiter}
("entity"{tuple_delimiter}"National Light Pollution Guidelines for Wildlife"{tuple_delimiter}"stakeholder"{tuple_delimiter}"Guidelines aimed at mitigating light pollution's impact on wildlife."){record_delimiter}
("entity"{tuple_delimiter}"Consultation on Marine and Coastal Ecosystem Protection."{tuple_delimiter}"event"{tuple_delimiter}"CAPL engaged with DBCA which can provide guidance through adherence to the National Light Pollution Guidelines and addressing ecological and spill response concerns in the OPP."){record_delimiter}
("entity"{tuple_delimiter}"Provided guidance on Marine and Coastal Ecosystem Protection, including identifying ecologically important areas."{tuple_delimiter}"event"{tuple_delimiter}"DBCA can provide guidance on protecting the Barrow Island Marine Park, Barrow Island Nature Reserve, and wildlife."){record_delimiter}
("entity"{tuple_delimiter}"Refer to some guidelines to address oil spill concerns and protect important ecological areas for the OPP."{tuple_delimiter}"event"{tuple_delimiter}"CAPL was recommended to protect the Barrow Island Marine Park, Barrow Island Nature Reserve, and wildlife for the OPP."){record_delimiter}
("relationship"{tuple_delimiter}"CAPL"{tuple_delimiter}"Consultation on Marine and Coastal Ecosystem Protection"{tuple_delimiter}"CAPL asked for consultation from DBCA on Marine and Coastal Ecosystem Protection."{tuple_delimiter}"consultation request, marine protection, ecosystem management"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Consultation on Marine and Coastal Ecosystem Protection"{tuple_delimiter}"Department of Biodiversity, Conservation and Attractions (DBCA)"{tuple_delimiter}"DBCA offered consultation on Marine and Coastal Ecosystem Protection."{tuple_delimiter}"consultation offer, ecosystem protection, guidance"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Department of Biodiversity, Conservation and Attractions (DBCA)"{tuple_delimiter}"Provided guidance on Marine and Coastal Ecosystem Protection, including identifying ecologically important areas."{tuple_delimiter}"Provided guidance on important areas for Marine and Coastal Ecosystem protection."{tuple_delimiter}"guidance, ecosystem identification, ecological protection"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Department of Biodiversity, Conservation and Attractions (DBCA)"{tuple_delimiter}"Provided guidance on Marine and Coastal Ecosystem Protection, including identifying ecologically important areas."{tuple_delimiter}"Provided guidance on important areas for Marine and Coastal Ecosystem protection."{tuple_delimiter}"guidance, ecological conservation, stakeholder support"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Department of Biodiversity, Conservation and Attractions (DBCA)"{tuple_delimiter}"Provided guidance on Marine and Coastal Ecosystem Protection, including offering important guidance documents."{tuple_delimiter}"Provided guidance on important guidance documents for Marine and Coastal Ecosystem protection."{tuple_delimiter}"guidance documents, consultation, ecological management"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Provided guidance on Marine and Coastal Ecosystem Protection, including identifying ecologically important areas."{tuple_delimiter}"Barrow Island Marine Park"{tuple_delimiter}"Barrow Island Marine Park was included as an ecologically important area within the vicinity of proposed operations."{tuple_delimiter}"marine protection, ecosystem significance, ecological importance"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Provided guidance on Marine and Coastal Ecosystem Protection, including identifying ecologically important areas."{tuple_delimiter}"Barrow Island Nature Reserve"{tuple_delimiter}"Barrow Island Nature Reserve was included as an ecologically important area within the vicinity of proposed operations."{tuple_delimiter}"nature reserve, ecosystem conservation, ecological importance"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Provided guidance on Marine and Coastal Ecosystem Protection, including offering important guidance documents."{tuple_delimiter}"National Light Pollution Guidelines for Wildlife"{tuple_delimiter}"National Light Pollution Guidelines for Wildlife was included as an important guidance document for the OPP."{tuple_delimiter}"light pollution, wildlife protection, guidance utilization"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"CAPL"{tuple_delimiter}"Refer to some guidelines to address oil spill concerns and protect important ecological areas for the OPP."{tuple_delimiter}"Planned protection measures in terms of guidance to protect Marine and Coastal Ecosystem while developing OPP."{tuple_delimiter}"oil spill management, ecosystem protection, planning"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"CAPL"{tuple_delimiter}"Refer to some guidelines to address oil spill concerns and protect important ecological areas for the OPP."{tuple_delimiter}"Planned protection measures in terms of guidance to protect Marine and Coastal Ecosystem while developing OPP."{tuple_delimiter}"ecological planning, environmental safety, guideline adherence"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"CAPL"{tuple_delimiter}"Refer to some guidelines to address oil spill concerns and protect important ecological areas for the OPP."{tuple_delimiter}"Planned protection measures in terms of guidance to protect Marine and Coastal Ecosystem while developing OPP."{tuple_delimiter}"spill response, marine ecosystem protection, safety planning"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Refer to some guidelines to address oil spill concerns and protect important ecological areas for the OPP."{tuple_delimiter}"Barrow Island Marine Park"{tuple_delimiter}"Barrow Island Marine Park was planned protection measures."{tuple_delimiter}"marine park, planned protection, ecological measures"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Refer to some guidelines to address oil spill concerns and protect important ecological areas for the OPP."{tuple_delimiter}"Barrow Island Nature Reserve"{tuple_delimiter}"Barrow Island Nature Reserve was planned protection measures."{tuple_delimiter}"nature reserve, planned conservation, environmental planning"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Refer to some guidelines to address oil spill concerns and protect important ecological areas for the OPP."{tuple_delimiter}"National Light Pollution Guidelines for Wildlife"{tuple_delimiter}"National Light Pollution Guidelines for Wildlife was referred to conduct protection measures."{tuple_delimiter}"wildlife guidelines, ecological adherence, conservation"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"marine ecosystem protection, ecological guidance, oil spill response, stakeholder engagement"){completion_delimiter}
#############################
""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown."""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "List all the relevant stakeholders who are involved in this Scarborough Gas Project in Australia. Identify the risk, conflict, and concerns of these stakeholders respectively."
################
Output:
{
  "high_level_keywords": [
    "Stakeholders",
    "Scarborough Gas Project",
    "Australia",
    "Risk",
    "Conflict",
    "Concerns"
  ],
  "low_level_keywords": [
    "Relevant stakeholders",
    "Project location",
    "Environmental impact",
    "Community interests",
    "Regulatory compliance",
    "Economic factors",
    "Operational challenges"
  ]
}
#############################""",
    """Example 2:

Query: "Assess the potential impacts of all stakeholders involved in Scarborough Gas Project on other projects or similar events in Australia."
################
Output:
{
  "high_level_keywords": [
    "Stakeholders",
    "Scarborough Gas Project",
    "Other projects",
    "Similar events",
    "Australia",
    "Potential impacts"
  ],
  "low_level_keywords": [
    "Relevant stakeholders",
    "Project influence",
    "Regional context",
    "Cross-project impacts",
    "Event interrelation",
    "Australian projects"
  ]
}
#############################""",
    """Example 3:

Query: "Provide short-term and long-term recommendations for Woodside Energy Limited by analyzing the stakeholders and events involved in the Scarborough Development. Focus on identifying potential future stakeholders the company may need to engage with and the types of events or challenges it might encounter when advancing similar projects in the future."
################
Output:
{
  "high_level_keywords": [
    "Short-term recommendations",
    "Long-term recommendations",
    "Woodside Energy Limited",
    "Stakeholders",
    "Events",
    "Scarborough Development",
    "Future projects",
    "Challenges"
  ],
  "low_level_keywords": [
    "Future stakeholders",
    "Potential challenges",
    "Engagement strategies",
    "Project advancement",
    "Similar projects",
    "Scarborough Gas Project context",
    "Corporate planning"
  ]
}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate the following two points and provide a similarity score between 0 and 1 directly:
1. Whether these two questions are semantically similar
2. Whether the answer to Question 2 can be used to answer Question 1
Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""

PROMPTS["mix_rag_response"] = """
---Role---

You are a professional assistant responsible for analyzing how specified **criteria dimensions** relate to stakeholders and events in a given document. Your task is to identify **stakeholders** and their associated **events (context)** based on the specified criterion, and evaluate their impact.

---Goal---

Your goal is to:
1. Dynamically locate **stakeholders** and **events (context)** in the document that are directly relevant to the specified criterion.
2. Extract the relevant **context** for each identified stakeholder and evaluate its alignment with the criterion.
3. Generate a structured, insightful table summarizing the **stakeholders**, their corresponding **events**, and the relevance of these events to the criterion.

If you cannot identify relevant information, explicitly state “Insufficient Data.”

---Response Methodology (Using Chain of Thought Reasoning)---

1. **Step 1: Criterion Understanding**
   - Read and understand the given criterion.
   - Reflect on how this criterion might manifest in the document.

2. **Step 2: Context Identification**
   - Search the document for sections (contexts) that relate to the specified criterion.
   - Identify stakeholders mentioned within these contexts and evaluate their actions or roles relative to the criterion.

3. **Step 3: Stakeholder and Event Extraction**
   - For each identified stakeholder:
     - Extract the corresponding context (event) from the document where the stakeholder’s actions align with the criterion.
     - Summarize how this context (event) reflects the stakeholder’s role or impact on the criterion.

4. **Step 4: Table Construction**
   - Construct a Markdown table with three columns:
     - **Stakeholder**: The stakeholder identified in the context.
     - **Event**: The specific context extracted where the criterion is addressed.
     - **Summary**: A concise explanation of how the criterion is reflected in the stakeholder’s actions or the event.

5. **Step 5: Validation**
   - Validate that the response includes:
     - A complete table summarizing the criterion, stakeholders, and events.
     - A "References" section listing the sources for the extracted context.

---Data Sources---

1. Knowledge Graph Data:
{kg_context}

2. Vector Data:
{vector_context}

---Response Requirements---

1. **Output Table**: The table must include:
   - **Stakeholder**: Stakeholder name or identifier.
   - **Event**: The specific context extracted from the document.
   - **Summary**: Explanation of the stakeholder’s role in the event and its relevance to the criterion.

2. **Markdown Table Format**:
   - Use `|` for column separation and `---` for headers.
   - Ensure alignment and readability.

3. **References Section**:
   - List up to 30 references with the format `[KG/VD] <Source content>`.
"""