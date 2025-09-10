# NAL India Frontend

A modern, luxury real estate platform built with React, TypeScript, and Vite.

## 🚀 Features

- **Modern Tech Stack**: React 18 + TypeScript + Vite
- **Luxury Design**: Glassmorphism + Neumorphism with dark/light themes
- **Performance**: Optimized with React Query, lazy loading, and code splitting
- **SEO Ready**: Meta tags, Open Graph, Schema.org structured data
- **Responsive**: Mobile-first design with desktop luxury experience
- **Accessibility**: WCAG 2.1 compliant with keyboard navigation
- **Animations**: Framer Motion micro-interactions and page transitions

## 🛠️ Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with custom luxury theme
- **State Management**: React Query + Context API
- **Forms**: React Hook Form + Zod validation
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **API Client**: Axios with interceptors

## 📦 Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🏗️ Project Structure

```
src/
├── api/           # API client and endpoints
├── assets/        # Static assets (images, icons)
├── components/    # Reusable UI components
│   └── ui/        # Base UI components (Button, Input, Card)
├── context/       # React contexts (Auth, Theme)
├── hooks/         # Custom React hooks
├── layouts/       # Layout components (Navbar, Footer)
├── pages/         # Page components
│   ├── Home/      # Landing page
│   ├── Auth/      # Authentication pages
│   ├── Properties/# Property listings
│   └── Dashboards/# Role-based dashboards
├── types/         # TypeScript type definitions
└── utils/         # Utility functions
```

## 🎨 Design System

### Colors
- **Primary**: Blue gradient (#0ea5e9 to #0369a1)
- **Luxury**: Gold (#d4af37) and Platinum (#e5e4e2)
- **Glass**: Semi-transparent overlays with backdrop blur

### Typography
- **Display**: Playfair Display (headings)
- **Body**: Inter (content)

### Components
- **Glassmorphism**: Transparent cards with backdrop blur
- **Luxury Gradients**: Premium color combinations
- **Micro-interactions**: Hover effects and smooth transitions

## 🔧 Environment Variables

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_GOOGLE_MAPS_API_KEY=your_api_key
VITE_GA_TRACKING_ID=your_tracking_id
```

## 📱 Responsive Design

- **Mobile**: 320px - 768px (Touch-optimized)
- **Tablet**: 768px - 1024px (Hybrid experience)
- **Desktop**: 1024px+ (Luxury experience)

## ♿ Accessibility

- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader optimized
- High contrast mode
- Focus management

## 🌐 SEO Optimization

- Server-side rendering ready
- Meta tags and Open Graph
- Schema.org structured data
- Semantic HTML structure
- Core Web Vitals optimized

## 🚀 Performance

- Code splitting with React.lazy
- Image optimization and lazy loading
- React Query caching
- Bundle size optimization
- Tree shaking enabled

## 🔒 Security

- XSS protection
- CSRF tokens
- Secure API communication
- Input validation and sanitization

## 📊 Analytics

- Google Analytics integration
- User behavior tracking
- Performance monitoring
- Error tracking with Sentry

## 🌍 Internationalization

- English (default)
- Extensible for Hindi, Arabic
- RTL support ready
- Currency and date formatting

## 🧪 Testing

```bash
# Run tests
npm run test

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## 📈 Deployment

### Vercel (Recommended)
```bash
npm run build
vercel --prod
```

### Netlify
```bash
npm run build
netlify deploy --prod --dir=dist
```

### AWS S3 + CloudFront
```bash
npm run build
aws s3 sync dist/ s3://your-bucket --delete
```

## 🔄 CI/CD

GitHub Actions workflow included for:
- Automated testing
- Build optimization
- Deployment to staging/production
- Performance audits

## 📝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- Documentation: [docs.nalindia.com](https://docs.nalindia.com)
- Issues: [GitHub Issues](https://github.com/nal-india/frontend/issues)
- Email: support@nalindia.com