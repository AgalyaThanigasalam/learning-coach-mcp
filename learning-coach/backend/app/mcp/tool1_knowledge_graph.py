"""MCP Tool 1: Knowledge Graph Engine — AI & Engineering domains"""
import networkx as nx
from typing import List, Dict, Optional

GRAPH_DATA = {
    # AI Core
    "Machine Learning":       {"prereqs": [], "difficulty": 2},
    "Supervised Learning":    {"prereqs": ["Machine Learning"], "difficulty": 2},
    "Unsupervised Learning":  {"prereqs": ["Machine Learning"], "difficulty": 3},
    "Reinforcement Learning": {"prereqs": ["Machine Learning"], "difficulty": 4},
    "Deep Learning":          {"prereqs": ["Machine Learning", "Neural Networks"], "difficulty": 3},
    "Neural Networks":        {"prereqs": ["Machine Learning"], "difficulty": 3},
    "CNN":                    {"prereqs": ["Deep Learning"], "difficulty": 4},
    "RNN":                    {"prereqs": ["Deep Learning"], "difficulty": 4},
    "Transformers":           {"prereqs": ["Deep Learning", "NLP"], "difficulty": 5},
    "NLP":                    {"prereqs": ["Machine Learning"], "difficulty": 3},
    "Computer Vision":        {"prereqs": ["Deep Learning", "CNN"], "difficulty": 4},
    "Generative AI":          {"prereqs": ["Deep Learning", "Transformers"], "difficulty": 5},
    "LLMs":                   {"prereqs": ["Transformers", "NLP"], "difficulty": 5},
    # GenAI & Agentic AI
    "Prompt Engineering":     {"prereqs": ["LLMs"], "difficulty": 3},
    "Fine-tuning":            {"prereqs": ["LLMs", "Deep Learning"], "difficulty": 4},
    "RAG":                    {"prereqs": ["LLMs", "Prompt Engineering"], "difficulty": 4},
    "AI Agents":              {"prereqs": ["LLMs", "Prompt Engineering"], "difficulty": 4},
    "Agentic AI":             {"prereqs": ["AI Agents"], "difficulty": 5},
    "Multi-Agent Systems":    {"prereqs": ["AI Agents"], "difficulty": 5},
    "Tool Use":               {"prereqs": ["AI Agents"], "difficulty": 4},
    "MCP Concepts":           {"prereqs": ["AI Agents", "Tool Use"], "difficulty": 4},
    # Data Science
    "Data Science":           {"prereqs": [], "difficulty": 2},
    "Data Preprocessing":     {"prereqs": ["Data Science"], "difficulty": 2},
    "Feature Engineering":    {"prereqs": ["Data Science", "Machine Learning"], "difficulty": 3},
    "Model Evaluation":       {"prereqs": ["Machine Learning"], "difficulty": 3},
    "Ensemble Methods":       {"prereqs": ["Supervised Learning"], "difficulty": 4},
    # Math
    "Linear Algebra":         {"prereqs": [], "difficulty": 2},
    "Probability":            {"prereqs": [], "difficulty": 2},
    "Statistics":             {"prereqs": ["Probability"], "difficulty": 2},
    "Calculus":               {"prereqs": [], "difficulty": 3},
    "Optimization":           {"prereqs": ["Calculus", "Linear Algebra"], "difficulty": 4},
    # Programming
    "Python":                 {"prereqs": [], "difficulty": 1},
    "Data Structures":        {"prereqs": ["Python"], "difficulty": 2},
    "Algorithms":             {"prereqs": ["Data Structures"], "difficulty": 3},
    "Dynamic Programming":    {"prereqs": ["Algorithms"], "difficulty": 5},
    # CS Fundamentals
    "Databases":              {"prereqs": [], "difficulty": 2},
    "Operating Systems":      {"prereqs": [], "difficulty": 3},
    "Networking":             {"prereqs": [], "difficulty": 2},
}

class KnowledgeGraphEngine:
    def __init__(self):
        self.graph = nx.DiGraph()
        for topic, data in GRAPH_DATA.items():
            self.graph.add_node(topic, difficulty=data["difficulty"])
            for p in data["prereqs"]:
                self.graph.add_edge(p, topic, relation="prerequisite")

    def get_learning_path(self, target: str, known: List[str] = []) -> List[str]:
        if target not in self.graph:
            return [target]
        try:
            ancestors = nx.ancestors(self.graph, target)
            nodes = list(ancestors) + [target]
            sub = self.graph.subgraph(nodes)
            return [t for t in nx.topological_sort(sub) if t not in known]
        except Exception:
            return [target]

    def get_next_topics(self, completed: List[str]) -> List[str]:
        result = []
        for node in self.graph.nodes():
            if node in completed:
                continue
            prereqs = list(self.graph.predecessors(node))
            if all(p in completed for p in prereqs):
                result.append(node)
        return result[:6]

    def get_all_topics(self) -> List[Dict]:
        return [{"name": n, "difficulty": d.get("difficulty", 2)}
                for n, d in self.graph.nodes(data=True)]

    def get_topic_info(self, topic: str) -> Optional[Dict]:
        if topic not in self.graph:
            return None
        return {
            "name": topic,
            "difficulty": self.graph.nodes[topic].get("difficulty", 2),
            "prerequisites": list(self.graph.predecessors(topic)),
            "leads_to": list(self.graph.successors(topic)),
        }

knowledge_graph = KnowledgeGraphEngine()
