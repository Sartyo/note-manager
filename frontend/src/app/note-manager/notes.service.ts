import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Note } from './models/note.model'

@Injectable({
  providedIn: 'root'
})
export class NotesService {
  private apiUrl = 'http://localhost:8000/api/notes/';

  constructor(private http: HttpClient) { }

  getNotes(includeArchived: boolean): Observable<Note[]> {
    let params = new HttpParams().set('is_archived', includeArchived);
    return this.http.get<Note[]>(this.apiUrl, { params });
  }

  getNote(id: number): Observable<Note> {
    return this.http.get<Note>(`${this.apiUrl}${id}/`);
  }

  createNote(note: Partial<Note>): Observable<Note> {
    return this.http.post<Note>(this.apiUrl, note);
  }

  updateNote(id: number, note: Partial<Note>): Observable<Note> {
    return this.http.put<Note>(`${this.apiUrl}${id}/`, note);
  }

  deleteNote(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/`);
  }
}
