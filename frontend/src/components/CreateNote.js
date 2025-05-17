import React, { useState } from 'react';
import { createNote } from '../services/api';

const CreateNote = () => {
    const [text, setText] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        await createNote({ content: text });
        setText('');
        window.location.reload(); // or use state to update instead
    };

    return (
        <form onSubmit={handleSubmit}>
            <input value={text} onChange={e => setText(e.target.value)} placeholder="New note" />
            <button type="submit">Add</button>
        </form>
    );
};

export default CreateNote;