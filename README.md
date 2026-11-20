# 🛡️ PromptShield
### AI-Powered Prompt Safety Tester & Red-Team Kit

**Break the Prompt. Find the Weakness. Build a Safer AI.**

PromptShield is an AI-powered red-teaming toolkit designed to evaluate the security and reliability of Large Language Model (LLM) based chatbots.

The platform aims to identify vulnerabilities in chatbot system prompts by generating adversarial test cases, evaluating chatbot responses, and recommending improvements to strengthen prompt-level security.

This project is being developed as part of the **Prompt Engineering Mini-Project (C23)** at Bennett University.

---

## 🎯 Problem Statement

LLM-based chatbots are increasingly used in customer support, education, business automation, and other applications. However, these systems can be vulnerable to prompt injection, instruction manipulation, role spoofing, and attempts to bypass established safety rules.

Manually testing chatbots against different adversarial prompts is time-consuming and may fail to cover important vulnerabilities.

**PromptShield aims to automate and organize this testing process**, helping developers identify weaknesses, understand failure cases, and improve their chatbot's system prompts.

## 💡 Proposed Solution

PromptShield is designed to provide a structured red-teaming workflow:

1. **System Prompt Input:** Developers provide the system instructions of a chatbot they own or are authorized to test.
2. **Adversarial Prompt Generation:** An LLM generates categorized attack prompts targeting potential instruction-following weaknesses.
3. **Chatbot Testing:** The generated prompts are executed against a sandboxed target chatbot.
4. **Safety Evaluation:** Responses are assessed against predefined rules and expected safe behaviors.
5. **Guardrail Recommendations:** The system suggests improvements to the original prompt.
6. **Comparative Analysis:** Baseline and improved system prompts are evaluated using comparable test cases.

## ✨ Planned Features

- AI-powered adversarial prompt generation
- Multiple attack categories, including role spoofing, instruction override, prompt extraction, and indirect prompt injection
- Structured JSON attack generation
- Automated chatbot testing
- Safety evaluation and failure analysis
- Prompt guardrail recommendations
- Baseline versus improved prompt comparison
- Interactive results dashboard
- Exportable evaluation results

## 🏗️ Proposed System Architecture

```text
          Developer / Tester
                  |
                  v
         System Prompt Input
                  |
                  v
        AI Attack Generator
                  |
                  v
       Generated Attack Cases
                  |
                  v
       Target Chatbot (Sandbox)
                  |
                  v
          Chatbot Responses
                  |
                  v
          Safety Evaluator
                  |
          +-------+-------+
          |               |
          v               v
    Test Results    Failure Analysis
          |               |
          +-------+-------+
                  |
                  v
       Guardrail Recommendations
                  |
                  v
        Improved System Prompt
                  |
                  v
        Retesting & Comparison
```

## 🧰 Proposed Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| LLM Integration | OpenAI API / compatible LLM |
| Frontend | Streamlit |
| Data Processing | Pandas |
| Visualization | Plotly |
| Data Storage | JSON, CSV |
| Version Control | Git & GitHub |

## 🔍 Prompt Engineering Techniques

This project focuses on the practical application of:

- Role-based prompting
- Few-shot prompting
- Constraint-based prompting
- Structured JSON outputs
- Prompt chaining
- Adversarial prompt generation
- Prompt iteration and A/B testing
- Guardrail design
- Rubric-based evaluation
- Error analysis and responsible AI testing

## 📊 Evaluation Strategy

The toolkit will evaluate chatbot behavior across different adversarial attack categories.

Planned evaluation criteria include:

- **Attack Success Rate (ASR):** Percentage of valid attacks that cause a defined safety or instruction-following failure.
- **Category Coverage:** Number of targeted attack categories represented in the test set.
- **Output Validity:** Percentage of generated test cases that follow the required JSON schema.
- **Guardrail Effectiveness:** Change in attack success rate after applying prompt improvements.
- **False Refusal Rate:** Percentage of legitimate requests incorrectly rejected by the chatbot.

Evaluation results will be documented using reproducible test cases and recorded model responses.

## 👥 Team Contributions

| Team Member | Responsibility |
|---|---|
| Member 1 | AI Attack Generator & Prompt Engineering |
| Member 2 | Target Chatbot, Testing & Safety Evaluation |
| Member 3 | Frontend & Results Dashboard |
| Member 4 | Guardrail Recommendations, Research & Experimentation |

All members will contribute to testing, documentation, and the final presentation.

## 📁 Planned Repository Structure

```text
promptshield-redteam-kit/
├── src/
│   ├── attack_generator.py
│   ├── target_chatbot.py
│   ├── test_runner.py
│   ├── evaluator.py
│   ├── guardrail_recommender.py
│   └── dashboard.py
├── prompts/
│   ├── attack_generator_v1.txt
│   ├── attack_generator_v2.txt
│   └── attack_generator_v3.txt
├── data/
├── experiments/
├── tests/
├── docs/
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

*The repository structure may evolve during implementation.*

## 🚀 Getting Started

Setup and execution instructions will be added as the implementation progresses.

The project will use environment variables for API credentials. API keys and other secrets must not be committed to the repository.

## 🔐 Responsible AI & Testing Scope

PromptShield is intended for educational research and authorized chatbot security evaluation.

- Testing will be limited to owned or explicitly authorized chatbot environments.
- No real credentials, confidential information, or personal user data will be used in attack-generation experiments.
- Model-generated evaluations will be checked against defined criteria and reviewed where necessary.
- Generated attacks will not be used to access unauthorized systems.
- Prompt-level guardrails will be treated as one component of security, not a replacement for application-level access controls.

## 📈 Project Status

**Status:** In Development

**Course:** Prompt Engineering — B.Tech 5th Semester  
**Problem Statement:** C23 — Prompt Safety Tester (Red-Team Kit)  
**Institution:** Bennett University  
**Final Submission Deadline:** December 1, 2026

## 🔮 Future Scope

- Support for multiple LLM providers
- Multi-turn adversarial testing
- Automated regression testing
- CI/CD integration for chatbot safety checks
- Advanced prompt injection detection
- Expanded attack datasets and evaluation benchmarks

---

### Academic Project

Developed as part of the Prompt Engineering Mini-Project at Bennett University.

**Project:** PromptShield — AI-Powered Prompt Safety Tester & Red-Team Kit
