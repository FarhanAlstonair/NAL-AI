import React from 'react';
import { Helmet } from 'react-helmet-async';
import Hero from './Hero';
import FeaturedProperties from './FeaturedProperties';

const HomePage: React.FC = () => {
  return (
    <>
      <Helmet>
        <title>NAL India - Premium Real Estate Marketplace | Luxury Properties</title>
        <meta
          name="description"
          content="Discover luxury properties across India with NAL India. Verified listings, expert agents, and seamless property transactions in Mumbai, Delhi, Bangalore & more."
        />
        <meta
          name="keywords"
          content="real estate India, luxury properties, apartments Mumbai, houses Delhi, property investment, NAL India"
        />
        <meta property="og:title" content="NAL India - Premium Real Estate Marketplace" />
        <meta
          property="og:description"
          content="Find your dream home with India's most trusted real estate platform"
        />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://nalindia.com" />
        <link rel="canonical" href="https://nalindia.com" />
        
        {/* Schema.org structured data */}
        <script type="application/ld+json">
          {JSON.stringify({
            "@context": "https://schema.org",
            "@type": "RealEstateAgent",
            "name": "NAL India",
            "description": "Premium real estate marketplace in India",
            "url": "https://nalindia.com",
            "logo": "https://nalindia.com/logo.png",
            "address": {
              "@type": "PostalAddress",
              "addressCountry": "IN"
            },
            "areaServed": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"],
            "serviceType": ["Property Sales", "Property Rental", "Property Investment"]
          })}
        </script>
      </Helmet>

      <div className="pt-16">
        <Hero />
        <FeaturedProperties />
      </div>
    </>
  );
};

export default HomePage;