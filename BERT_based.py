# import numpy as np
# import pandas as pd
# import faiss
# from sentence_transformers import SentenceTransformer
#
# # Load your dataset
# df = pd.read_csv(r"C:\Users\lenovo\Projects\CourseAdvisorChat\Model\Dataset.csv",encoding='latin-1')  # Change this to your actual file
#
# # Load pre-trained BERT model
# model = SentenceTransformer('all-MiniLM-L6-v2')
#
# # Convert all questions to embeddings
# question_texts = df['Question'].tolist()
# question_embeddings = model.encode(question_texts, convert_to_numpy=True)
#
# # Store embeddings in FAISS index
# dimension = question_embeddings.shape[1]
# index = faiss.IndexFlatL2(dimension)
# index.add(question_embeddings)
#
# # Save the FAISS index and questions
# faiss.write_index(index, "Question_embeddings.index")
# np.save("Question_texts.npy", np.array(question_texts))
#
# print("Model training completed! Saved embeddings for fast retrieval.")

# -----------------------
from flask import Flask, request, jsonify
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pandas as pd
import re
from Controller.KnowledgeBaseController import get_all_knowledgebase


# Load the dataset
df = pd.read_csv(r"C:\Users\lenovo\Projects\CourseAdvisorChat\Model\Dataset.csv", encoding='latin-1')

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load stored FAISS index and question texts
index = faiss.read_index(r"C:\Users\lenovo\Projects\CourseAdvisorChat\Model\BERT-based retrieval model\question_embeddings.index")
question_texts = np.load(r"C:\Users\lenovo\Projects\CourseAdvisorChat\Model\BERT-based retrieval model\Question_texts.npy", allow_pickle=True)

app = Flask(__name__)


def get_answer():
    data = request.json
    query = data.get("question")

    if not query:
        return jsonify({"error": "Question is required!"}), 400

    # Convert query into an embedding
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Search for the most similar question
    _, indices = index.search(query_embedding, k=1)
    best_match = question_texts[indices[0][0]]

    # Retrieve corresponding answer
    answer = df[df['Question'] == best_match]['Answer'].values[0]

    # Find tags in the answer text (e.g., <tag>)
    tags = re.findall(r'<(.*?)>', answer)

    # Get the knowledge base data from the controller response.
    kb_response, status_code = get_all_knowledgebase()
    kb_json = kb_response.get_json()  # Extract the JSON payload
    kb_data = kb_json.get("data", [])

    # Replace each tag with the corresponding value from the knowledge base.
    for tag in tags:
        for kb in kb_data:
            if kb["key_name"] == tag and kb["Type"] == 1:
                answer = answer.replace("<" + tag + ">", kb["value"])

    return jsonify({
        "query": query,
        "best_matched_question": best_match,
        "answer": answer
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
