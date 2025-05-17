import React from 'react';
import NoteList from '../components/NoteList';
import CreateNote from '../components/CreateNote';

const Home = () => (
    <div>
        <h1>Notes</h1>
        <CreateNote />
        <NoteList />
    </div>
);

export default Home;