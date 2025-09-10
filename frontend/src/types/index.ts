export interface User {
  uuid: string;
  email: string;
  username: string;
  phone?: string;
  role: 'BUYER' | 'SELLER' | 'AGENT' | 'ADMIN' | 'VERIFIER' | 'SYSTEM';
  is_verified: boolean;
  created_at: string;
  profile?: UserProfile;
}

export interface UserProfile {
  full_name: string;
  photo_url?: string;
  kyc_status: 'PENDING' | 'VERIFIED' | 'REJECTED';
  address?: string;
  city?: string;
  state?: string;
  country: string;
  pincode?: string;
  date_of_birth?: string;
}

export interface Property {
  uuid: string;
  title: string;
  description: string;
  price: number;
  currency: string;
  property_type: 'APARTMENT' | 'HOUSE' | 'VILLA' | 'PLOT' | 'COMMERCIAL' | 'WAREHOUSE';
  status: 'DRAFT' | 'PUBLISHED' | 'UNDER_REVIEW' | 'ARCHIVED' | 'SOLD';
  address: string;
  city: string;
  state: string;
  pincode: string;
  latitude?: number;
  longitude?: number;
  bedrooms: number;
  bathrooms: number;
  area_sqft?: number;
  parking_spaces: number;
  ribl_score?: number;
  urgent_sale_value?: number;
  created_at: string;
  updated_at: string;
  media?: PropertyMedia[];
  amenities?: PropertyAmenity[];
  owner_name?: string;
  agent_name?: string;
  primary_image?: string;
}

export interface PropertyMedia {
  id: number;
  media_url: string;
  media_type: 'IMAGE' | 'VIDEO' | 'VIRTUAL_TOUR';
  is_primary: boolean;
  caption?: string;
  created_at: string;
}

export interface PropertyAmenity {
  id: number;
  name: string;
  icon?: string;
  category?: string;
}

export interface Document {
  uuid: string;
  title: string;
  doc_type: 'TITLE_DEED' | 'ENCUMBRANCE' | 'TAX_RECEIPT' | 'IDENTITY' | 'NOC' | 'SURVEY' | 'APPROVAL';
  status: 'UPLOADED' | 'PROCESSING' | 'VERIFIED' | 'PENDING' | 'REJECTED';
  file_size: number;
  mime_type: string;
  verification_result?: any;
  processed_text?: string;
  download_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Booking {
  uuid: string;
  property: {
    uuid: string;
    title: string;
    address: string;
  };
  booking_type: 'SITE_VISIT' | 'VIRTUAL_TOUR' | 'CONSULTATION';
  booking_date: string;
  booking_time: string;
  duration_minutes: number;
  status: 'PENDING' | 'CONFIRMED' | 'COMPLETED' | 'CANCELLED' | 'NO_SHOW';
  contact_name: string;
  contact_phone: string;
  virtual_tour_link?: string;
  notes?: string;
  created_at: string;
}

export interface Transaction {
  uuid: string;
  amount: number;
  currency: string;
  transaction_type: 'BOOKING_FEE' | 'SECURITY_DEPOSIT' | 'COMMISSION' | 'REFUND';
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED' | 'CANCELLED' | 'REFUNDED';
  description?: string;
  gateway_transaction_id?: string;
  created_at: string;
  completed_at?: string;
}

export interface SearchFilters {
  q?: string;
  city?: string;
  property_type?: string;
  min_price?: number;
  max_price?: number;
  bedrooms?: number;
  lat?: number;
  lng?: number;
  radius?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  errors?: string[];
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: {
    results: T[];
    pagination: {
      page: number;
      pages: number;
      count: number;
      has_next: boolean;
      has_previous: boolean;
    };
  };
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
  device_id?: string;
  device_type?: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  phone?: string;
  role: string;
}