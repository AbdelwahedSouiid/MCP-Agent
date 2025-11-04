export interface TranscriptionResponse {
    language: string;
    language_probability: number;
    segments: Segment[];
  }

export interface Segment{
  start: number;
  end: number;
  text: string;
}
  