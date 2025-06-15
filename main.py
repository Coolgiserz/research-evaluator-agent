from src.research_evaluator_agent.agents.master import MasterAgent
def main():
    result = MasterAgent().evaluate(text="爱心专座优先提供给老年人（年满60周岁、残疾人和孕妇使用，必要时其他读者请让座）",
                                     context="图书馆提示")
    print(result)
if __name__ == "__main__":
    main()