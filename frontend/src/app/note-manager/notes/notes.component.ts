import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Note, Tag } from '../models/note.model';
import { NotesService } from '../notes.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-notes',
  imports: [CommonModule, FormsModule],
  templateUrl: './notes.component.html',
  styleUrl: './notes.component.css'
})
export class NotesComponent implements OnInit {
  notes: Note[] = [];
  showArchived: boolean = false;
  loading = false;
  error: string | null = null;
  editingNoteId: number | null = null;
  editContent: string = '';
  editTitle: string = '';
  editTags: Tag[] = [];
  editArchived: boolean = false;
  newNoteTitle: string = '';
  newNoteContent: string = '';

  constructor(private notesService: NotesService) { }

  ngOnInit(): void {
    this.fetchNotes();
  }

  fetchNotes(): void {
    this.loading = true;
    this.notesService.getNotes(this.showArchived).subscribe({
      next: (data) => {
        this.notes = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load notes';
        this.loading = false;
        console.error(err);
      }
    });
  }

  createNote() {
    const note = {
      title: this.newNoteTitle,
      content: this.newNoteContent,
      tags: [],
      is_archived: false
    };
    this.notesService.createNote(note).subscribe({
      next: createdNote => {
        this.notes.push(createdNote);
        this.newNoteTitle = '';
        this.newNoteContent = '';
      },
      error: err => console.error(err)
    });
  }

  toggleArchived(): void {
    this.showArchived = !this.showArchived;
    this.fetchNotes();
  }

  toggleArchive(note: Note) {
    const updated = {
      title: note.title,
      content: note.content,
      tags: note.tags,
      is_archived: !note.is_archived
    };
    this.notesService.updateNote(note.id, updated).subscribe({
      next: updatedNote => {
        note.is_archived = updatedNote.is_archived;
      },
      error: err => console.error(err)
    });
  }

  startEditing(note: Note) {
    this.editingNoteId = note.id;
    this.editTitle = note.title;
    this.editContent = note.content;
    this.editTags = note.tags;
    this.editArchived = note.is_archived;
  }

  cancelEditing() {
    this.editingNoteId = null;
    this.editContent = '';
    this.editTitle = '';
    this.editTags = [];
    this.editArchived = false;
  }

  saveNote(note: Note) {
    this.notesService.updateNote(note.id, { content: this.editContent, title: this.editTitle, is_archived: this.editArchived, tags: this.editTags }).subscribe({
      next: updatedNote => {
        note.title = updatedNote.title;
        note.content = updatedNote.content;
        note.is_archived = updatedNote.is_archived;
        note.tags = updatedNote.tags;
        this.cancelEditing();
      },
      error: err => console.error(err)
    });
  }

  deleteNote(id: number) {
    if (confirm('Are you sure you want to delete this note?')) {
      this.notesService.deleteNote(id).subscribe({
        next: () => {
          this.notes = this.notes.filter(n => n.id !== id);
        },
        error: err => console.error(err)
      });
    }
  }
}
