import React, { useEffect, useState } from "react";
import "./Notes.css";

function Notes() {
  const [notes, setNotes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [viewingNoteId, setViewingNoteId] = useState(null);
  const [editingNoteId, setEditingNoteId] = useState(null);

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [category, setCategory] = useState("General");

  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");
  const [editCategory, setEditCategory] = useState("");

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/notes?page=${page}&per_page=5`)
      .then((r) => {
        if (r.ok) {
          return r.json();
        }

        throw new Error("Failed to load notes.");
      })
      .then((data) => {
        setNotes(data.notes);
        setTotalPages(data.pagination.pages);
        setIsLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setIsLoading(false);
      });
  }, [page]);

  function handleSubmit(e) {
    e.preventDefault();
    setError("");

    fetch(`${process.env.REACT_APP_API_URL}/notes`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        content,
        category,
      }),
    })
      .then((r) => {
        if (r.ok) {
          return r.json();
        }

        return r.json().then((data) => {
          throw new Error(data.error || "Failed to create note.");
        });
      })
      .then((newNote) => {
        setNotes((currentNotes) => [...currentNotes, newNote]);
        setTitle("");
        setContent("");
        setCategory("General");
      })
      .catch((error) => {
        setError(error.message);
      });
  }

  function handleDelete(id) {
    setError("");

   fetch(`${process.env.REACT_APP_API_URL}/notes/${id}`, {
      method: "DELETE",
    })
      .then((r) => {
        if (r.ok) {
          return r.json();
        }

        return r.json().then((data) => {
          throw new Error(data.error || "Failed to delete note.");
        });
      })
      .then(() => {
        setNotes((currentNotes) =>
          currentNotes.filter((note) => note.id !== id)
        );
      })
      .catch((error) => {
        setError(error.message);
      });
  }

  function handleView(id) {
    if (viewingNoteId === id) {
      setViewingNoteId(null);
    } else {
      setViewingNoteId(id);
      setEditingNoteId(null);
    }
  }

  function handleEdit(note) {
    setEditingNoteId(note.id);
    setEditTitle(note.title);
    setEditContent(note.content);
    setEditCategory(note.category);
    setViewingNoteId(note.id);
  }

  function handleUpdate(e, id) {
    e.preventDefault();
    setError("");

   fetch(`${process.env.REACT_APP_API_URL}/notes/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: editTitle,
        content: editContent,
        category: editCategory,
      }),
    })
      .then((r) => {
        if (r.ok) {
          return r.json();
        }

        return r.json().then((data) => {
          throw new Error(data.error || "Failed to update note.");
        });
      })
      .then((updatedNote) => {
        setNotes((currentNotes) =>
          currentNotes.map((note) =>
            note.id === id ? updatedNote : note
          )
        );
        setEditingNoteId(null);
      })
      .catch((error) => {
        setError(error.message);
      });
  }

  if (isLoading) {
    return <p>Loading notes...</p>;
  }

  return (
    <div className="notes-container">
      <h2>My Notes</h2>

      {error && <p>{error}</p>}

      <form className="note-form" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor="category">Category</label>
          <input
            type="text"
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />
        </div>

        <button type="submit">Add Note</button>
      </form>

      {notes.length === 0 ? (
        <p>You don't have any notes yet.</p>
      ) : (
        notes.map((note) => (
          <div className="note" key={note.id}>
            <h3>{note.title}</h3>

            <button onClick={() => handleView(note.id)}>
              {viewingNoteId === note.id ? "Hide" : "View"}
            </button>

            <button onClick={() => handleEdit(note)}>
              Edit
            </button>

            <button onClick={() => handleDelete(note.id)}>
              Delete
            </button>

            {viewingNoteId === note.id && (
              <div>
                {editingNoteId === note.id ? (
                  <form onSubmit={(e) => handleUpdate(e, note.id)}>
                    <div>
                      <label htmlFor={`edit-title-${note.id}`}>
                        Title
                      </label>

                      <input
                        type="text"
                        id={`edit-title-${note.id}`}
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                      />
                    </div>

                    <div>
                      <label htmlFor={`edit-content-${note.id}`}>
                        Content
                      </label>

                      <textarea
                        id={`edit-content-${note.id}`}
                        value={editContent}
                        onChange={(e) => setEditContent(e.target.value)}
                      />
                    </div>

                    <div>
                      <label htmlFor={`edit-category-${note.id}`}>
                        Category
                      </label>

                      <input
                        type="text"
                        id={`edit-category-${note.id}`}
                        value={editCategory}
                        onChange={(e) =>
                          setEditCategory(e.target.value)
                        }
                      />
                    </div>

                    <button type="submit">Save Changes</button>

                    <button
                      type="button"
                      onClick={() => setEditingNoteId(null)}
                    >
                      Cancel
                    </button>
                  </form>
                ) : (
                  <div>
                    <p>{note.content}</p>
                    <p>Category: {note.category}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        ))
      )}

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setPage(page - 1)}
            disabled={page === 1}
          >
            Previous
          </button>

          <span>
            Page {page} of {totalPages}
          </span>

          <button
            onClick={() => setPage(page + 1)}
            disabled={page === totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

export default Notes;