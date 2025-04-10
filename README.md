
# 🧠 AI Web Content Analyzer

A powerful web content analyzer that scrapes any webpage, summarizes the key insights, and uses agentic reasoning to generate deeper analysis using LangChain agents and LLMs from OpenRouter. Built with Gradio UI.

![Screenshot]([https://i.imgur.com/x5n8B4I.png](https://github.com/deep200315/AI-Agent-/blob/main/Screenshot%202025-04-10%20201937.png))
---

## 🚀 Features

- 🔍 **Web Scraping** – Extracts content from any valid URL using `WebBaseLoader`.
- ✂️ **Chunk Splitting** – Uses `RecursiveCharacterTextSplitter` for efficient document segmentation.
- 🤖 **LLM Summarization** – Summarizes text using OpenRouter-powered LLMs (`mixtral-8x7b-instruct`).
- 🧠 **LangChain Agent** – Performs deeper insights using `TavilySearchResults` via zero-shot reasoning.
- 🧪 **Interactive UI** – Built with Gradio for easy interaction and live preview.

---

## 📦 Dependencies

Install all required libraries:

```bash
pip install -r requirements.txt
```


---

## 🔐 API Keys

Before running the app, set your API keys in `os.environ`:

```python
os.environ["OPENROUTER_API_KEY"] = "your_openrouter_key"
os.environ["TAVILY_API_KEY"] = "your_tavily_key"
```

You can get your keys from:

- [OpenRouter.ai](https://openrouter.ai/)
- [Tavily API](https://www.tavily.com/)

---

## 🧪 How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/deep200315/AI-Agent-.git/
   cd AI-Agent-
   ```

2. Launch the app:
   ```bash
   python app.py
   ```

3. Open your browser at `http://localhost:7866`.

4. Paste any URL and hit **"Analyze"** to get:
   - 🔹 A summarized **Key Info**
   - 🔹 A deeper **Concise Summary** via agent

---

## 🧠 Powered By

- **[LangChain](https://www.langchain.com/)** – Framework for LLM-powered apps
- **[OpenRouter](https://openrouter.ai/)** – Unified API for multiple open-source LLMs
- **[Tavily](https://www.tavily.com/)** – Real-time web search tool
- **[Gradio](https://www.gradio.app/)** – Quick UI for ML apps

---



## 📌 Examples

Test it with these URLs:

- `https://en.wikipedia.org/wiki/Artificial_intelligence`
- `https://en.wikipedia.org/wiki/Hello_(Adele_song)`




---

## 💡 Future Ideas

- Add PDF or DOCX support
- Add download button for summaries
- Integrate more LLM tools (e.g., Google Search, Bing, Wolfram)

---


