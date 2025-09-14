
export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface TraceNode {
  name: string;
  input: any;
  output: any;
  status: string;
}
