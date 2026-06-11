from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader
)


class PDFLoader:

    def load_directory(
        self,
        pdf_dir: str
    ):

        documents = []

        for pdf_file in Path(pdf_dir).glob("*.pdf"):

            loader = PyPDFLoader(
                str(pdf_file)
            )

            docs = loader.load()

            for doc in docs:

                doc.metadata["source"] = (
                    pdf_file.name
                )

            documents.extend(docs)

        return documents