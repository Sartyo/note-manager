export interface Tag {
  id: number;
  name: string;
}

export interface Note {
  id: number;
  title: string;
  content: string;
  is_archived: boolean;
  tags: Tag[];
  created_at: string;
}
