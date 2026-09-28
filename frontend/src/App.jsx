import { useState } from 'react'

const API_URL =
  import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'

function App() {
  const [file, setFile] = useState(null)
  const [document, setDocument] = useState(null)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  // Upload PDF
  const uploadDocument = async () => {
    if (!file) {
      setMessage('Please select a PDF first.')
      return
    }

    setLoading(true)
    setMessage('Uploading and indexing document...')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(
        `${API_URL}/documents/upload/`,
        {
          method: 'POST',
          body: formData,
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.error || 'Failed to upload document.'
        )
      }

      setDocument(data)
      setAnswer('')
      setSources([])
      setMessage('Document is ready. Ask a question below.')
    } catch (error) {
      console.error('Upload error:', error)
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  // Ask question
  const askQuestion = async () => {
    if (!document) {
      setMessage('Please upload a document first.')
      return
    }

    if (!question.trim()) {
      setMessage('Please enter a question.')
      return
    }

    setLoading(true)
    setMessage('Searching the document...')

    try {
      const response = await fetch(
        `${API_URL}/ask/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            document_id: document.id,
            question: question.trim(),
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.error || 'Failed to get an answer.'
        )
      }

      setAnswer(data.answer || '')
      setSources(data.sources || [])
      setMessage('')
    } catch (error) {
      console.error('Question error:', error)
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page">
      <section className="card">

        {/* Header */}
        <header>
          <p className="eyebrow">
            RAG + LANGGRAPH
          </p>

          <h1>
            AI Research Document Assistant
          </h1>

          <p className="subtitle">
            Upload a PDF and ask questions about its content.
          </p>
        </header>

        {/* Upload Section */}
        <div className="section">
          <label className="label">
            1. Upload document
          </label>

          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={(event) => {
              setFile(event.target.files[0])
              setMessage('')
            }}
          />

          <button
            onClick={uploadDocument}
            disabled={loading}
          >
            {loading ? 'Working...' : 'Upload PDF'}
          </button>

          {document && (
            <p className="success">
              Ready: {document.name}
            </p>
          )}
        </div>

        {/* Question Section */}
        <div className="section">
          <label className="label">
            2. Ask a question
          </label>

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            placeholder="Example: What is the main conclusion of this document?"
            rows={4}
          />

          <button
            onClick={askQuestion}
            disabled={loading || !document}
          >
            {loading ? 'Searching...' : 'Ask Question'}
          </button>
        </div>

        {/* Message */}
        {message && (
          <p className="message">
            {message}
          </p>
        )}

        {/* Answer */}
        {answer && (
          <div className="answer-box">
            <h2>Answer</h2>

            <p>
              {answer}
            </p>
          </div>
        )}

        {/* Sources */}
        {sources.length > 0 && (
          <div className="sources">
            <h2>Sources</h2>

            {sources.map((source, index) => (
              <div
                className="source"
                key={`${source.page}-${index}`}
              >
                <strong>
                  Page {source.page ?? '?'}
                </strong>

                <p>
                  {source.text}
                </p>
              </div>
            ))}
          </div>
        )}

      </section>
    </main>
  )
}

export default App