import os, re, requests
from dotenv import load_dotenv
load_dotenv()

class ProjectAdvisor:
    def __init__(self):
        self.model_name = "gemini-2.0-flash"
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.base_url = (
            "https://generativelanguage.googleapis.com/v1beta"
            f"/models/{self.model_name}:generateContent"
        )

        self.prompts = {
            "overview": (
                "You are an AI advisor. Provide a concise project overview in English based on the uploaded document: {input}. "
                "Return 1-2 short paragraphs, no explanations, instructions, or Markdown formatting."
            ),
            "business_requirements": (
                "You are an AI advisor. Identify business requirements (goals, objectives, business rules) in English based on the uploaded document: {input}. "
                "Return a numbered list of concise requirements as full sentences using 'must' or 'shall' where appropriate, with priority (High/Medium/Low) and dependencies (e.g., 'Dependency: Functional 1'), no labels like 'Requirement:' or Markdown."
            ),
            "functional_requirements": (
                "You are an AI advisor. Identify functional requirements (specific features and functionalities) in English based on the uploaded document: {input}. "
                "Return a numbered list of concise requirements as full sentences using 'must' or 'shall' where appropriate, with priority (High/Medium/Low) and dependencies, no labels like 'Requirement:' or Markdown."
            ),
            "non_functional_requirements": (
                "You are an AI advisor. Identify non-functional requirements (performance, security, usability, etc.) in English based on the uploaded document: {input}. "
                "Return a numbered list of concise requirements as full sentences using 'must' or 'shall' where appropriate, with priority (High/Medium/Low) and dependencies, no labels like 'Requirement:' or Markdown."
            ),
            "technical_requirements": (
                "You are an AI advisor. Identify technical requirements (technologies, frameworks, databases, deployment, etc.) in English based on the uploaded document: {input}. "
                "Return a numbered list of concise requirements as full sentences using 'must' or 'shall' where appropriate, with priority (High/Medium/Low) and dependencies, no labels like 'Requirement:' or Markdown."
            ),
            "functional_analysis": (
                "You are an AI advisor. For each functional requirement in the uploaded document: {input}, provide a concise analysis including: "
                "1. Feasibility (Feasible/Partially Feasible/Not Feasible), "
                "2. Implementation Complexity (Low/Medium/High), "
                "3. System Impact (Low/Medium/High), "
                "4. Suggested Implementation Approach. "
                "Return a numbered list, each item formatted as: '[Text]; Feasibility: [Value]; Complexity: [Value]; Impact: [Value]; Approach: [Text]', no additional explanations or Markdown."
            ),
            "technical_analysis": (
                "You are an AI advisor. For each requirement in the uploaded document: {input}, provide a concise technical analysis including: "
                "1. Technical Constraints, "
                "2. Architectural Implications, "
                "3. Technology Stack Compatibility, "
                "4. Performance Considerations. "
                "Return a numbered list, each item formatted as: '[Text]; Constraints: [Text]; Architecture: [Text]; Compatibility: [Text]; Performance: [Text]', no additional explanations or Markdown."
            ),
            "impact_analysis": (
                "You are an AI advisor. Provide a concise impact analysis for the requirements in the uploaded document: {input}, including: "
                "1. Cross-Requirement Impacts, "
                "2. System-Wide Implications, "
                "3. Business Process Impacts, "
                "4. Integration Points with Existing Systems. "
                "Return a numbered list with each item clearly addressing one of these points, no additional explanations or Markdown."
            ),

            "uml": (
                "You are an AI advisor. Provide detailed UML diagrams in English based on the uploaded document: {input}. "
                "Generate the following diagrams in valid Mermaid.js syntax (version 10.9.3, no extra characters or invalid syntax). "
                "Clearly separate each diagram with the following explicit headings:\n"
                "1. 'Class Diagram': Define key classes with attributes, methods, and relationships (use --> for association, --|> for inheritance, *-- for composition), apply design patterns (e.g., Singleton).\n"
                "2. 'Use Case Diagram': Use 'graph TD' instead of 'flowchart'. Do NOT use the 'actor' keyword. Define actors and use cases using shapes like User([User]), UC1((UseCase1)), and connect with --> arrows."
                "3. 'Activity Diagram': Clearly define the workflow, including start/end points, decision points, and parallel processes.\n"
                "4. 'Sequence Diagram': Define objects, interactions, messages, and sequence flows clearly.\n"
                "Do not use generic headings like 'Diagram X', instead use exactly the headings given above. "
                "Return only these headings followed by Mermaid.js diagrams, no additional explanations or Markdown formatting."
                "Ensure all Mermaid code is syntactically valid and renders without errors in Mermaid.js v10.9.3. Do not generate malformed diagrams."

            ),


        }

    def analyze_project(self, document_text):
        return {
            "overview": self._clean_paragraphs(self._query("overview", document_text)),
            "requirements": {
                "business": self._clean_list(self._query("business_requirements", document_text)),
                "functional": self._clean_list(self._query("functional_requirements", document_text)),
                "non_functional": self._clean_list(self._query("non_functional_requirements", document_text)),
                "technical": self._clean_list(self._query("technical_requirements", document_text))
            },
            "analysis": {
                "functional": self._clean_list(self._query("functional_analysis", document_text)),
                "technical": self._clean_list(self._query("technical_analysis", document_text)),
                "impact": self._clean_list(self._query("impact_analysis", document_text))
            },
            "uml": self._clean_uml(self._query("uml", document_text))
        }

    def _query(self, key, document_text):
        prompt = self.prompts[key].format(input=document_text)
        url = f"{self.base_url}?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        res = requests.post(url, headers={"Content-Type":"application/json"}, json=payload, timeout=45)
        if not res.ok:
            raise RuntimeError(f"HTTP {res.status_code}: {res.text}")
        candidates = res.json().get("candidates", [])
        text = "".join(p.get("text","") for p in candidates[0].get("content",{}).get("parts",[]))
        return text

    def _clean_paragraphs(self, text):
        clean = re.sub(r'[*#]+|\[.*?\]', '', text, flags=re.DOTALL)
        return [p.strip() for p in re.split(r'\n\s*\n', clean) if p.strip()][:2]

    def _clean_list(self, text):
        clean = re.sub(r'[*#]+|Requirement:|\[.*?\]', '', text, flags=re.DOTALL)
        items = re.findall(r'^\d+\.\s*(.+)', clean, re.MULTILINE)
        return items or [line.strip() for line in clean.splitlines() if line.strip() and line[0].isdigit()]

    def _clean_uml(self, text):
        blocks = []
        current_block = []
        in_code_block = False
        for line in text.splitlines():
            line = line.strip()
            if line.startswith('```mermaid'):
                in_code_block = True
                current_block = [line]
            elif line == '```' and in_code_block:
                in_code_block = False
                current_block.append(line)
                blocks.append('\n'.join(current_block))
                current_block = []
            elif in_code_block:
                current_block.append(line)
            elif line and not in_code_block:
                blocks.append(line)
        return '\n\n'.join(blocks)