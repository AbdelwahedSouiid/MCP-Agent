export interface ProductSearchResult {
  _id: string;
  name: string;
  description: string;
  price: number;
  brand: string;
  costPrice: number;
  discountPrice: number;
  stock: number;
  sku: number;
  stockStatus?: string;
  mainImgUrl?: string;
  slug?: string;
}
