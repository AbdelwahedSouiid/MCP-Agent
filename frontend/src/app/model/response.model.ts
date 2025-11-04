import { ProductSearchResult } from "./productSearchResult.model";


export interface SearchResponse {
  text_response: string;
  products: ProductSearchResult[];
  response_type: 'search_response';
}

export interface TextResponse {
  text_response: string;
  response_type: 'text_response';
}

