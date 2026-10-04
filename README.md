# 🚗 Car Insurance Multi-Agent AI System

An AI-powered multi-agent insurance claims assessment platform that combines **Generative AI, Computer Vision, Retrieval-Augmented Generation (RAG), LangGraph and FastAPI** to automate the initial assessment of motor insurance claims.

The system analyses claim information, insurance policy documentation and accident photographs, then produces a structured assessment while identifying cases that require human review.

> **Important:** This system provides an AI-assisted assessment and does not make legally binding insurance or claims decisions.

---

## 🎯 Project Overview

Traditional insurance claims processing can involve manual document review, image inspection and repetitive assessment tasks.

This project demonstrates how an **agentic AI architecture** can support claims handlers by coordinating specialised AI agents.

The platform accepts:

- Customer information
- Policy information
- Vehicle registration
- Accident description
- Accident photograph

The information is then processed through multiple specialised AI agents before producing a consolidated assessment.

---

## 🧠 Multi-Agent Architecture

```text
                         CUSTOMER
                            │
                            ▼
                    ┌───────────────┐
                    │   FastAPI     │
                    │    Gateway    │
                    └───────┬───────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ LangGraph Supervisor│
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   ┌────────────┐    ┌────────────┐    ┌────────────┐
   │   Policy   │    │   Vision   │    │   Claims   │
   │   Agent    │    │   Agent    │    │   Agent    │
   └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
         │                 │                 │
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                           ▼
                    ┌────────────┐
                    │ RAG Agent  │
                    │ ChromaDB   │
                    └─────┬──────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Decision Agent │
                  └───────┬────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Structured AI    │
                 │ Assessment       │
                 └──────────────────┘
                          │
                          ▼
                   HUMAN REVIEW

🤖 AI Agents
1. Supervisor Agent
Coordinates the overall workflow and manages the interaction between specialised agents.
Responsibilities:
- Orchestrate the claim assessment workflow
- Coordinate specialised agents
- Manage information flow
- Support consistent processing

2. Policy Agent
Analyses the relevant insurance policy information.
Responsibilities:
- Identify applicable coverage
- Examine policy conditions
- Identify exclusions and limitations
- Provide policy context to the assessment

3. Vision Agent
Uses multimodal AI to analyse accident photographs.
Responsibilities:
- Identify visible vehicle damage
- Identify damaged components
- Assess apparent damage severity
- Identify visible safety concerns
- Highlight uncertainty
- Recommend human inspection when necessary
The Vision Agent is intentionally designed to report observable evidence rather than inventing hidden damage.

4. Claims Agent
Processes the claimant's accident description and claim information.
Responsibilities:
- Structure claim information
- Extract relevant incident details
- Compare reported information with other assessment signals
- Support downstream decision-making

5. RAG Agent
Uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from insurance policy documentation.
Technology:
- ChromaDB
- Vector search
- Document retrieval
- LLM-based reasoning
This allows the system to ground its assessment in policy information rather than relying solely on the language model's general knowledge.

6. Decision Agent
Combines outputs from the other agents.
Responsibilities:
- Consolidate policy assessment
- Consider visual damage assessment
- Evaluate claim information
- Identify uncertainty
- Determine whether human review is required
- Produce the final structured assessment


🔄 End-to-End Workflow
1. Customer submits claim
          ↓
2. Accident image uploaded
          ↓
3. FastAPI receives request
          ↓
4. Claim information validated
          ↓
5. LangGraph starts workflow
          ↓
6. Policy information analysed
          ↓
7. Accident image analysed
          ↓
8. Claim information processed
          ↓
9. Relevant policy information retrieved
          ↓
10. Decision Agent consolidates evidence
          ↓
11. Human-review requirement determined
          ↓
12. Structured assessment returned
          ↓
13. Dashboard displays results

🖥️ Application Dashboard
The project includes a browser-based dashboard where users can submit an insurance claim.
Claim submission
Users can provide:
- Customer name
- Policy number
- Vehicle registration
- Claim description
- Accident photograph
The dashboard supports:
- JPG
- PNG
- WEBP

📊 AI Assessment Dashboard
After processing, the system displays:
- Assessment status
- Claim ID
- Assessment timestamp
- Human review status
- Policy assessment
- Vehicle damage assessment
- Final decision
The interface is designed to provide a clear operational view of the AI assessment pipeline.

👁️ Computer Vision
The Vision Agent analyses uploaded accident photographs using multimodal AI.
Example observations can include:
Visible damage:
- Front bumper deformation
- Bonnet damage
- Front-end impact damage

Severity:
- Moderate to significant visible damage

Safety concerns:
- Possible damage to front-end components

Limitations:
- Hidden mechanical and structural damage cannot
  be confirmed from the photograph.

Recommendation:
- Human inspection recommended.
The system does not claim to determine hidden damage from a photograph when that evidence is unavailable.

📚 Retrieval-Augmented Generation
The RAG component uses ChromaDB as the vector database.
Policy documents can be converted into searchable knowledge and retrieved during assessment.
Policy Documents
       ↓
Document Processing
       ↓
Chunking
       ↓
Embeddings
       ↓
ChromaDB
       ↓
Similarity Search
       ↓
Relevant Policy Context
       ↓
Decision Agent
This architecture helps ground AI-generated assessments in the organisation's policy documentation.

⚡ Backend API
The system uses FastAPI as the application gateway.

Main endpoint
POST /assess-claim

The endpoint accepts:
customer_name
policy_number
vehicle_registration
claim_description
image
The request is then passed into the LangGraph insurance assessment workflow.

🧩 Technology Stack
| Technology | Purpose |
|---|---|
| Python | Core development |
| FastAPI | REST API |
| LangGraph | Agent orchestration |
| LangChain | AI application framework |
| OpenAI | LLM and multimodal AI |
| ChromaDB | Vector database |
| RAG | Policy knowledge retrieval |
| Pydantic | Data validation |
| Uvicorn | Application server |
| HTML/CSS/JavaScript | Frontend dashboard |
| Git/GitHub | Version control |

📁 Project Structure
car-insurance-ai/
│
├── app/
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── policy_agent.py
│   │   ├── vision_agent.py
│   │   ├── claims_agent.py
│   │   ├── rag_agent.py
│   │   └── decision_agent.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── graph/
│   │   └── insurance_graph.py
│   │
│   ├── models/
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── embeddings.py
│   │   └── retriever.py
│   │
│   ├── config.py
│   └── main.py
│
├── dashboard/
│   └── index.html
│
├── data/
│   ├── policies/
│   ├── claims/
│   └── sample_images/
│
├── chroma_db/
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md

🚀 Running the Project
1. Clone the repository
git clone <YOUR-GITHUB-REPOSITORY>
cd car-insurance-ai

2. Create virtual environment
python3.11 -m venv .venv

3. Activate environment
source .venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Configure environment variables
Create a .env file:
OPENAI_API_KEY=your_api_key_here

Never commit .env to GitHub.
6. Start FastAPI
uvicorn app.main:app --reload

The API will be available at:
http://127.0.0.1:8000

Interactive API documentation:
http://127.0.0.1:8000/docs

🧪 Testing
The project includes automated testing for core application components.
Run:
pytest

Python syntax checks can be performed with:
python -m py_compile app/api/routes.py

🛡️ Human-in-the-Loop AI
Insurance claims can have significant financial and customer consequences.
Therefore, this system follows a human-in-the-loop approach.
The AI can recommend:
Potentially covered
Potentially not covered
Insufficient evidence
Human review required

The system does not replace an authorised claims professional.
Human review can be triggered when:
- Evidence is insufficient
- Image quality is poor
- Damage cannot be confidently assessed
- Policy interpretation is uncertain
- Potentially significant damage is detected
- The AI identifies conflicting information

🔐 Responsible AI Considerations
The system was designed with several responsible AI principles:
Transparency
The system provides supporting assessment information rather than presenting an unexplained decision.
Human Oversight
High-impact or uncertain assessments can be escalated to human reviewers.
Evidence Grounding
Policy-related assessments are supported using retrieved policy information.
Uncertainty Awareness
The Vision Agent explicitly identifies limitations when information cannot be determined from the image.
Data Protection
Sensitive configuration such as API credentials is stored in environment variables rather than source code.

💼 Business Value
A production version of this architecture could help insurance organisations:
- Reduce repetitive manual claim-processing tasks
- Accelerate initial claim triage
- Improve access to policy information
- Assist claims handlers with image analysis
- Standardise initial assessments
- Identify claims requiring additional investigation
- Improve operational efficiency
The system is designed as an AI decision-support platform, not an autonomous claims approval system.

2. Create virtual environment
python3.11 -m venv .venv

3. Activate environment
source .venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Configure environment variables
Create a .env file:
OPENAI_API_KEY=your_api_key_here

Never commit .env to GitHub.
6. Start FastAPI
uvicorn app.main:app --reload

The API will be available at:
http://127.0.0.1:8000

Interactive API documentation:
http://127.0.0.1:8000/docs

🧪 Testing
The project includes automated testing for core application components.
Run:
pytest

Python syntax checks can be performed with:
python -m py_compile app/api/routes.py

🛡️ Human-in-the-Loop AI
Insurance claims can have significant financial and customer consequences.
Therefore, this system follows a human-in-the-loop approach.
The AI can recommend:
Potentially covered
Potentially not covered
Insufficient evidence
Human review required

The system does not replace an authorised claims professional.
Human review can be triggered when:
- Evidence is insufficient
- Image quality is poor
- Damage cannot be confidently assessed
- Policy interpretation is uncertain
- Potentially significant damage is detected
- The AI identifies conflicting information

🔐 Responsible AI Considerations
The system was designed with several responsible AI principles:
Transparency
The system provides supporting assessment information rather than presenting an unexplained decision.

Human Oversight
High-impact or uncertain assessments can be escalated to human reviewers.
Evidence Grounding
Policy-related assessments are supported using retrieved policy information.
Uncertainty Awareness
The Vision Agent explicitly identifies limitations when information cannot be determined from the image.

Data Protection
Sensitive configuration such as API credentials is stored in environment variables rather than source code.

💼 Business Value
A production version of this architecture could help insurance organisations:
- Reduce repetitive manual claim-processing tasks
- Accelerate initial claim triage
- Improve access to policy information
- Assist claims handlers with image analysis
- Standardise initial assessments
- Identify claims requiring additional investigation
- Improve operational efficiency

The system is designed as an AI decision-support platform, not an autonomous claims approval system.

📈 Future Improvements
Potential production enhancements include:
- Authentication and role-based access control
- Secure cloud deployment
- PostgreSQL claim database
- Enterprise document management integration
- Advanced fraud detection
- OCR for accident documents
- Damage severity scoring
- Repair-cost estimation
- Claims history analysis
- Audit logging
- Human reviewer workflow
- Monitoring and observability
- Automated evaluation of agent performance
- CI/CD pipeline
- Docker containerisation
- AWS deployment
🎓 Skills Demonstrated
This project demonstrates practical experience in:
- Generative AI
- Agentic AI
- Multi-agent systems
- LangGraph
- LangChain
- Retrieval-Augmented Generation
- Vector databases
- ChromaDB
- Computer Vision
- Multimodal AI
- FastAPI
- REST APIs
- Python
- Prompt engineering
- AI workflow orchestration
- Human-in-the-loop systems
- Responsible AI
- Full-stack AI application development
📸 Project Screenshots
Add project screenshots here:
screenshots/
├── claim-submission.png
├── ai-assessment.png
├── damage-analysis.png
└── architecture.png

Example:
![Claim Submission Dashboard](screenshots/claim-submission.png)

![AI Assessment Dashboard](screenshots/ai-assessment.png)

👨‍💻 Project Author
YONGA. B F (BENTECH)
AI / Machine Learning Program Graduate.
Interested in building practical AI systems using:
Generative AI • Agentic AI • Machine Learning • Computer Vision • RAG • Cloud AI

⭐ Project Status
Status: Portfolio Demonstration / Prototype
The current system demonstrates an end-to-end AI-assisted insurance claims assessment workflow.
Further security, governance, validation, monitoring and regulatory controls would be required before production deployment in a real insurance environment.

⭐ If you find this project interesting
Feel free to explore the architecture, experiment with the agents and build on the workflow.

Generative AI + Multi-Agent Systems + RAG + Computer Vision
                         ↓
              Practical Business AI