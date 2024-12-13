## langchain create agent helper, with RAG-compatiable chain inside agent.
## used for our langGraph-based agent system.
import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

import os
from langchain_chroma import Chroma

from config import *
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# from pydantic import BaseModel, Field

def chain_for_model(model: ChatOpenAI,
                      prompt: ChatPromptTemplate | PromptTemplate, 
                      embedding: OpenAIEmbeddings = None, 
                      db_dir = None,
                      include_rag: bool = False):
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    if include_rag:
        # 加载已经存在的向量存储
        if os.path.exists(db_dir):
            vectorstore = Chroma(
                embedding_function=embedding,
                persist_directory=db_dir
            )
            print(f"Loaded vectorstore from: {db_dir}")
        else:
            raise FileNotFoundError(f"Database not found at {db_dir}")

        # 设置检索器
        retriever = vectorstore.as_retriever()

        # string should be used for input and output if using PromptTemplate instead of ChatPromptTemplate. 
        # refer to https://python.langchain.ac.cn/v0.2/docs/tutorials/rag/
        # refer to https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/#llms for solution.

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )

        # rag_chain.invoke("What is Task Decomposition?")
    else:
        chain = prompt | model

    return chain

# this is a general create_agent tool.
# refer to https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/#create-agents.
def create_agent(tools=[],
                 chat_model=chat_model,
                 embedding_model=embedding_model,
                 system_msg: str = "",
                 llm: ChatOpenAI = None,
                 temperature: float = None,
                 database_dir: str = "",
                 embedding: OpenAIEmbeddings = None,
                 system_msg_is_dir: bool = True,
                 include_rag: bool = False, 
                 include_tools: bool = False
                ) -> ChatOpenAI: 
    """ 
        tools: A list containing all possible tool functions. By default is a void list.
        chat_model: the base model to build the agent.
                    alternatives:
                    (calling gpt keys)
                    "gpt-3.5-turbo-0125"
                    "gpt-4"
                    "gpt-4o"
                    (calling deepseek keys)
                    "deepseek-chat"
                    "deepseek-coder "
        system_message: System message in the format of string.
        system_msg_dir: Dir for system message should be provided here.
        llm: the llm model to be modified if input a void 
             By default support ChatOpenAI-type api.
    """
    
    if llm == None:
        if chat_model in ["gpt-3.5-turbo-0125", "gpt-4", "gpt-4o"]:
            base_agent_model = ChatOpenAI(model=chat_model, 
                                        api_key=openai_api_key,
                                        base_url=openai_base_url)
        elif chat_model in ["deepseek-chat", "deepseek-coder"]:
            base_agent_model = ChatOpenAI(model=chat_model, 
                                        api_key=deepseek_api_key,
                                        base_url=deepseek_base_url)
        else:       # potential other open apis & local open-source llm in openai-key-format
            base_agent_model = ChatOpenAI(model=chat_model, 
                                        api_key=api_key,
                                        base_url=base_url)     
    else:
        base_agent_model = llm  
    
    if embedding == None and include_rag:
        embedding = OpenAIEmbeddings(
                            model=embedding_model,
                            api_key=openai_api_key,
                            base_url=openai_base_url
                        )
    else:
        include_rag = False
        
    if temperature != None:
        base_agent_model.temperature = temperature
        
    if tools == None:
        tools = []
        
    if system_msg_is_dir:
        with open(system_msg, 'r') as file:
            system_message = file.read()
    else:
        system_message = system_msg
    
    
    if not include_rag:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    " {system_message}\nYou have access to the following tools: {tool_names}.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
    else:
        prompt = PromptTemplate.from_template(
            """
                {system_message}\n
                You have access to the following tools: \n {tool_names}\n \
                Helpful message from retrieval tool: \n{context} \n
                Your task is: \n {question} \n
            """
    )
    
    prompt = prompt.partial(system_message=system_message)
    if include_tools and len(tools)>0:
        tool_names=", ".join([tool.name for tool in tools])
        prompt = prompt.partial(tool_names=tool_names)
        model = base_agent_model.bind_tools(tools)
    else:
        tool_names=""
        prompt = prompt.partial(tool_names=tool_names)
        model =  base_agent_model
        
    return chain_for_model(model=model, prompt=prompt, include_rag=include_rag,
                           embedding=embedding, db_dir=database_dir)
    
