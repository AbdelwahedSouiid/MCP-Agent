// model/product.model.ts
export interface Product {
  url: string;
  title: string;
  price: string;
  description: string;
  images: string[];
  // Nouveaux champs
  category: string | null;
  availability: boolean;
}


export interface ProductSuggestion {
  name: string;
  brand: string;
  price: string;
  description: string;
  link: string;
}