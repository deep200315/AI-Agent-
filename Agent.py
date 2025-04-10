import os
import gradio as gr
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from validators import url as validate_url

os.environ["OPENROUTER_API_KEY"]
os.environ["TAVILY_API_KEY"]
llm_chat = ChatOpenAI(
    model="mistralai/mixtral-8x7b-instruct", 
    base_url="https://openrouter.ai/api/v1", 
    api_key=os.environ["OPENROUTER_API_KEY"],
    temperature=0.3
)

def safe_text(text: str) -> str:
    return text.encode('utf-8', 'ignore').decode('utf-8')

def web_scraper(url: str) -> str:
    if not validate_url(url):
        return "Error: Invalid URL format."

    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        return "\n\n".join([doc.page_content for doc in chunks[:5]])
    except Exception as e:
        return f"Error scraping content: {str(e)}"

def generate_summary(text: str) -> str:
    prompt = ChatPromptTemplate.from_template(
        "Provide a clear, concise, and informative key insights of the following text:\n\n{text}"
    )
    chain = prompt | llm_chat
    return chain.invoke({"text": text}).content

from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults

# Define tool explicitly with correct name
tavily_tool = Tool(
    name="tavily_search_results_json",
    func=TavilySearchResults(max_results=1).run,
    description="Useful for answering questions about current events or web data."
)

tools = [tavily_tool]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm_chat,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
)

def process_url(url):
    if not url or not isinstance(url, str):
        return "No URL provided", "No analysis (missing URL)"
    
    if not validate_url(url):
        return "Invalid URL", "No analysis (invalid URL)"
    
    content = web_scraper(url)
    if content.startswith("Error"):
        return content, content

    truncated = content[:6000]

    try:
        summary = generate_summary(truncated)
        summary = safe_text(summary)
    except Exception as e:
        summary = f"Summary generation failed: {str(e)}"

    try:
        analysis = agent_executor.invoke({
            "input": f"Analyze this content and give deep insights as summary of 10-12 lines strictly: {truncated}"
        })["output"]
        analysis = safe_text(analysis)
    except Exception as e:
        analysis = f"Agentic analysis failed: {str(e)}"

    return summary, analysis

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# AI Web Content Analyzer")  

    with gr.Row():
        url_input = gr.Textbox(label="Enter URL", placeholder="https://example.com")
        submit_btn = gr.Button("Analyze")
    
    with gr.Accordion("Results", open=True):
        summary_out = gr.Textbox(label="Key Info")
        analysis_out = gr.Textbox(label="Concise Summary")
    
    submit_btn.click(
        fn=process_url,
        inputs=url_input,
        outputs=[summary_out, analysis_out]
    )
    
    gr.Examples(
        examples=[
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "https://en.wikipedia.org/wiki/Hello_(Adele_song)"
        ],
        inputs=url_input
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7866, debug=True)
