import React, { useEffect, useState } from 'react';
import { fetchNotes } from '../services/api';

const NoteList = () => {
    const [notes, setNotes] = useState([]);

    useEffect(() => {
        fetchNotes().then(res => setNotes(res.data));
    }, []);

    return (
        <ul>
            {notes.map(note => (
                <li key={note.id}>{note.content}</li>
            ))}
        </ul>
    );
};

export default NoteList;